import os
import argparse
import requests

from config import STABILITY_API_KEY

def text2audio(
    prompt: str,
    duration: int = 10,
    filename: str = "./audio/text2audio.mp3",
    seed: int = 0,
    steps: int = 50,
    cfg_scale: float = 7.0,
    output_format: str = "mp3",
    stability_key: str = STABILITY_KEY,
) -> str:
    """
    Generate audio from a text prompt using Stability AI's Text-to-Audio API.

    Args:
        prompt (str): Descriptive prompt for generation.
        duration (int): Desired length of the output audio (in seconds).
        filename (str): Output filename to save the generated audio.
        seed (int): Random seed for reproducibility.
        steps (int): Number of generation steps.
        cfg_scale (float): Prompt adherence strength.
        output_format (str): Output file format ('mp3' or 'wav').
        stability_key (str): API key for Stability AI; uses STABILITY_KEY env var if not provided.

    Returns:
        str: Path to the saved audio file.
    """
    STABILITY_KEY = stability_key or os.getenv("STABILITY_KEY")
    if not STABILITY_KEY:
        raise ValueError("Missing Stability API key. Pass it explicitly or set STABILITY_KEY env var.")
    response = requests.post(
        "https://api.stability.ai/v2beta/audio/stable-audio-2/text-to-audio",
        headers={"Authorization": f"Bearer {STABILITY_KEY}", "Accept": "audio/*"},
        files={"image": None},
        data={
            "prompt" : prompt,
            "duration": duration,
            "seed": seed,
            "steps": steps,
            "cfg_scale" : cfg_scale,
            "output_format": output_format,
        }
    )

    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    with open(filename, "wb") as f:
        f.write(response.content)

    print(f"✅ Saved generated audio to: {filename}")
    return filename



def audio2audio(
    prompt: str,
    audio_path: str,
    duration: int = 10,
    filename: str = "./audio/audio2audio.mp3",
    seed: int = 0,
    steps: int = 50,
    cfg_scale: float = 7.0,
    strength: float = 1.0,
    output_format: str = "mp3",
    stability_key: str = STABILITY_KEY,
) -> str:
    """
    Generate new audio from an existing audio file using Stability AI's Audio-to-Audio API.

    Args:
        prompt (str): Descriptive generation prompt.
        audio_path (str): Path to input audio file (.wav or .mp3).
        duration (int): Desired output length in seconds.
        filename (str): Output filename for the generated audio.
        seed (int): Random seed for reproducibility.
        steps (int): Number of generation steps.
        cfg_scale (float): Prompt adherence strength.
        strength (float): Degree of transformation (0.0 to 1.0).
        output_format (str): Output file format ('mp3' or 'wav').
        stability_key (str): API key for Stability; falls back to STABILITY_KEY env variable.

    Returns:
        str: Path to the saved audio file.
    """
    STABILITY_KEY = stability_key or os.getenv("STABILITY_KEY")
    if not STABILITY_KEY:
        raise ValueError("Missing Stability API key. Pass it explicitly or set STABILITY_KEY env var.")

    with open(audio_path, "rb") as audio_file:
        response = requests.post(
            "https://api.stability.ai/v2beta/audio/stable-audio-2/audio-to-audio",
            headers={
                "Authorization": f"Bearer {STABILITY_KEY}",
                "Accept": "audio/*",
            },
            files={"audio": audio_file},
            data={
                "prompt": prompt,
                "duration": duration,
                "seed": seed,
                "steps": steps,
                "cfg_scale": cfg_scale,
                "output_format": output_format,
                "strength": strength,
            },
        )

    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    with open(filename, "wb") as f:
        f.write(response.content)

    print(f"✅ Saved transformed audio to: {filename}")
    return filename

if __name__ == "__main__":
    # === Config ===
    prompt_text = "A slow ambient piece evoking a cloudy afternoon in London"
    input_audio_path = "./audio/synth_loop.wav"  # Replace with your own file path
    
    parser = argparse.ArgumentParser(description="Run text2audio or audio2audio.")
    parser.add_argument("--mode", choices=["text2audio", "audio2audio"], required=True, help="Select generation mode.")
    args = parser.parse_args()

    prompt = "A dreamy ambient soundtrack with soft textures"
    duration = 15

    if args.mode == "text2audio":
        print("🚀 Running text2audio()...")
        text2audio(
            prompt=prompt,
            duration=duration,
        )

    elif args.mode == "audio2audio":
        print("🎛️ Running audio2audio()...")
        audio2audio(
            prompt=prompt,
            audio_path=input_audio_path,  # make sure this file exists
            duration=duration,
        )