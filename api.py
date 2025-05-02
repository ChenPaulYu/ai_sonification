import os
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse

# === Import core logic ===
from image_caption     import caption_image_with_gpt4o
from opencage_api      import location_text_to_latlon
from openweather_api   import get_weather_by_lat_lon, get_weather_by_ip
from weather_to_prompt import interpret_weather_to_music_prompt
from stableaudio_api   import text2audio, audio2audio

import asyncio
import nest_asyncio

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

nest_asyncio.apply()

app = FastAPI(title="AI Sonification API")

@app.post("/generate")
async def generate_music_prompt(
    location: Optional[str] = Form(None),
    journal: Optional[str] = Form(None),
    duration: Optional[int] = Form(20),  #
    image: Optional[UploadFile] = File(None),
    reference_audio: Optional[UploadFile] = File(None)
):
    try:
        # === Get weather ===
        if location:
            latlon = location_text_to_latlon(location)
            if not latlon:
                return JSONResponse(status_code=400, content={"error": "Invalid location"})
            lat, lon = latlon
            weather = get_weather_by_lat_lon(lat, lon)
            latlon_str = f"{lat:.4f}, {lon:.4f}"
        else:
            weather = get_weather_by_ip()
            if not weather:
                return JSONResponse(status_code=500, content={"error": "Weather fetch failed"})
            latlon_str = "Detected via IP"

        print(lat, lon)
        # === Handle image upload ===
        image_caption = ""
        image_path = None
        if image:
            image_path = f"temp_{image.filename}"
            with open(image_path, "wb") as f:
                f.write(await image.read())
            image_caption = caption_image_with_gpt4o(image_path)
        # === Generate prompt ===
        result = interpret_weather_to_music_prompt(
            weather=weather,
            journal=journal or "",
            image_caption=image_caption or ""
        )
        

        # === Handle audio generation ===
        reference_path = None
        audio_filename = "./audio/generated_music.mp3"
        duration = min(duration, 180)

        if reference_audio:
            reference_path = f"temp_{reference_audio.filename}"
            with open(reference_path, "wb") as f:
                f.write(await reference_audio.read())

            audio2audio(
                prompt=result.suggested_prompt,
                audio_path=reference_path,
                duration=duration,
                filename=audio_filename
            )
            gen_mode = "audio2audio"
        else:
            text2audio(
                prompt=result.suggested_prompt,
                duration=duration,
                filename=audio_filename
            )
            gen_mode = "text2audio"

        # === Clean up temp files ===
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        if reference_path and os.path.exists(reference_path):
            os.remove(reference_path)

        return {
            "location": latlon_str,
            "image_caption": image_caption,
            "weather_summary": f"{weather['city']} | {weather['temperature']}C | {weather['weather_desc']}",
            "mood_keywords": result.mood_keywords,
            "summary": result.summary,
            "prompt": result.suggested_prompt,
            "mode": gen_mode,
            "audio_url": f"/audio/{audio_filename}"
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/audio/{filename}")
def serve_audio(filename: str):
    path = f"./{filename}"
    if not os.path.exists(path):
        return JSONResponse(status_code=404, content={"error": "File not found"})
    return FileResponse(path, media_type="audio/mpeg")


