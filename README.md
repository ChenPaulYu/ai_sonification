# 🎵 AI Sonification API

A FastAPI-based service for generating emotionally driven music prompts and audio using:
- 📍 Location (text or IP-based geolocation)
- 📝 Journal entry
- 🖼 Image captioning (via GPT-4o)
- 🎧 Reference audio (optional)
- 🌤 Real-time weather data

Built with **FastAPI** + **Gradio** UI + **Stable Audio** + **OpenAI GPT-4o**, and uses `uv` for package management.

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone <github link>
cd ai_sonification
```

### 2. Install `uv` (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Install dependencies with `uv`
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

If `requirements.txt` is missing, you can install the basics manually:
```bash
uv pip install fastapi uvicorn python-multipart openai pydantic-ai gradio
```

---

## 🔐 API Key Setup

### 🔑 How to Obtain API Keys
- OpenWeatherMap (Weather Data): Sign up at https://openweathermap.org/appid to create an account and obtain your API key.
- OpenAI (Image Captioning with GPT-4o): Register at https://platform.openai.com/signup to create an account. After logging in, navigate to https://platform.openai.com/account/api-keys to generate your API key.
- Stability AI (Stable Audio): Create an account at https://platform.stability.ai/. Once logged in, go to the API Keys section to generate your API key. 
- OpenCage (Geolocation): Sign up at https://opencagedata.com/users/sign_up to create an account and obtain your API key.

Once you've obtained these API keys, store them securely in your `config.py` file as follows:

Once you've obtained these API keys, store them securely in your config.py file as follows:
```python
OPENAI_API_KEY      = "<your-openai-key>"
STABILITY_API_KEY   = "<your-stability-key>"
OPENCAGE_API_KEY    = "<your-opencage-key>"
OPENWEATHER_API_KEY = "<your-openweather-key>"
```

---

## 🚀 Running the API Server

Use `uvicorn` to launch the FastAPI server:

```bash
uvicorn api:app --reload --loop asyncio
```

> We disable `uvloop` with `--loop asyncio` for compatibility with GPT-4o + `pydantic_ai`.

---

## 🎛️ Running the Gradio UI

To launch the interactive Gradio interface:

```bash
python ui.py
```

This will start a local web app at `http://localhost:7860`.

---

## 🔍 API Usage (Quick Guide)

### POST `/generate`
Generate music and prompt from multimodal inputs.

**Form Data Inputs:**
- `location` (string, optional)
- `journal` (string, optional)
- `duration` (int, seconds, default: 20, max: 180)
- `image` (file, optional)
- `reference_audio` (file, optional)

**Example Response:**
```json
{
  "location": "Taipei 101",
  "image_caption": "A rainy city street viewed from a café window...",
  "weather_summary": "Taipei | 22.5C | light rain",
  "mood_keywords": ["calm", "introspective", "soft"],
  "summary": "Clouds hover low, matching the stillness of the room...",
  "prompt": "Solo | Genre: Ambient | Instruments: rain textures, piano...",
  "mode": "text2audio",
  "audio_url": "/audio/generated_music.mp3"
}
```

### GET `/audio/{filename}`
Serve the generated audio file for download or playback.

---

## 🧪 Testing in Postman
- Set `POST http://localhost:8000/generate`
- Set **Body** → `form-data`
- Add fields: `location`, `journal`, `duration`, `image` (file), `reference_audio` (file)
- Only include `image` and `reference_audio` if you actually upload files (don’t send empty strings)

---

## 🗂 Project Structure
```
├── ui.py                # Gradio UI interface
├── api.py               # FastAPI main server
├── image_caption.py     # GPT-4o vision-based image captioning
├── openweather_api.py   # OpenWeatherMap wrapper
├── opencage_api.py      # Geolocation via OpenCage
├── stableaudio_api.py   # Stable Audio API calls
├── weather_to_prompt.py # Weather + journal + image caption → prompt fusion
├── pyproject.toml       # uv tool metadata
├── config.py            # Centralized API key + constants
├── README.md            # This file
```

---

Made with 🎧 by Bo-Yu Chen
