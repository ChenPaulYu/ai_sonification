import gradio as gr
from typing import Optional

# === Customized Module ===

from image_caption     import caption_image_with_gpt4o
from opencage_api      import location_text_to_latlon
from openweather_api   import get_weather_by_lat_lon, get_weather_by_ip
from weather_to_prompt import interpret_weather_to_music_prompt
from stableaudio_api   import text2audio, audio2audio

# === Wrap Core Functionality ===
def generate_prompt_from_inputs(
    location_text: str,
    journal_text: str,
    image_file: str,
    reference_audio_file: str,
    audio_duration: int
):
    try:
        latlon_str = "N/A"
        image_caption = ""

        # === Get weather ===
        if location_text.strip():
            latlon = location_text_to_latlon(location_text)
            if not latlon:
                return "❌ Could not find coordinates.", "", "", "", "", "", None, ""
            lat, lon = latlon
            latlon_str = f"{lat:.4f}, {lon:.4f}"
            weather = get_weather_by_lat_lon(lat, lon)
        else:
            weather = get_weather_by_ip()
            latlon_str = "Detected via IP"
            if not weather:
                return "❌ Failed to fetch weather.", "", "", "", "", "", None, ""

        # === Image caption ===
        if image_file:
            image_caption = caption_image_with_gpt4o(image_file)

        # === Prompt generation ===
        result = interpret_weather_to_music_prompt(
            weather=weather,
            journal=journal_text or "",
            image_caption=image_caption or ""
        )

        weather_summary = (
            f"{weather['city']} | {weather['temperature']}°C | "
            f"{weather['weather_desc']} | Humidity {weather['humidity']}% | "
            f"Wind {weather['wind_speed']} m/s"
        )

        # === Safe duration cap (max 180 sec) ===
        duration = min(audio_duration, 180)

        # === Audio generation ===
        if reference_audio_file:
            audio_path = audio2audio(
                prompt=result.suggested_prompt,
                audio_path=reference_audio_file,
                duration=duration,
            )
            gen_mode = f"audio2audio (with reference, {duration}s)"
        else:
            audio_path = text2audio(
                prompt=result.suggested_prompt,
                duration=duration,
            )
            gen_mode = f"text2audio (no reference, {duration}s)"

        return (
            latlon_str,
            image_caption or "(no image uploaded)",
            weather_summary,
            ", ".join(result.mood_keywords),
            result.summary,
            result.suggested_prompt,
            audio_path,
            gen_mode
        )

    except Exception as e:
        return f"❌ Error: {str(e)}", "", "", "", "", "", None, ""


    
# === Gradio UI ===
with gr.Blocks(title="🎵 MoodSound: A Multimodal Music Generator from Weather, Journals, and Images") as demo:
    gr.Markdown("## 🎵 AI sonifies your daily life—from the weather to your snapshots and personal writing")
    gr.Markdown("Enter a location (or leave blank to auto-detect), write a journal entry, and optionally upload an image. The AI will craft a music generation prompt.")

    with gr.Row():
        location_input = gr.Text(label="📍 Location (optional)", placeholder="e.g., Taipei 101")
        journal_input = gr.Textbox(label="📝 Journal Entry (optional)", lines=3)

    with gr.Row():
        image_input = gr.Image(label="🖼️ Upload Image (optional)", type="filepath")
        reference_audio_input = gr.Audio(label="🎧 Reference Audio (optional)", type="filepath")

    audio_duration_input = gr.Slider(
        label="⏱️ Audio Duration (seconds)",
        minimum=5,
        maximum=180,
        value=20,
        step=5
    )

    generate_btn = gr.Button("🎶 Generate Music")

    with gr.Row():
        latlon_output = gr.Textbox(label="🌍 Lat / Lon", interactive=False)
        image_caption_output = gr.Textbox(label="🖼️ Image Caption", interactive=False)
        weather_output = gr.Textbox(label="🌤️ Weather Summary", interactive=False)

    with gr.Row():
        mood_output = gr.Textbox(label="🎼 Mood Keywords", interactive=False)
        summary_output = gr.Textbox(label="🧠 LLM Summary", interactive=False)
        prompt_output = gr.Textbox(label="🎧 Music Prompt (Stable Audio-style)", lines=3, interactive=False)

    audio_output = gr.Audio(label="🔊 Generated Audio", interactive=False)
    mode_output = gr.Textbox(label="⚙️ Generation Mode", interactive=False)

    generate_btn.click(
        fn=generate_prompt_from_inputs,
        inputs=[
            location_input,
            journal_input,
            image_input,
            reference_audio_input,
            audio_duration_input
        ],
        outputs=[
            latlon_output,
            image_caption_output,
            weather_output,
            mood_output,
            summary_output,
            prompt_output,
            audio_output,
            mode_output
        ]
    )

    

demo.launch(share=True)

