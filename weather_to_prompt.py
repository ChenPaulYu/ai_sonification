from typing import Dict, Optional
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from config import OPENAI_API_KEY

# === Pydantic Schema ===
class WeatherInterpretation(BaseModel):
    location: str
    summary: str
    mood_keywords: list[str]
    suggested_prompt: str

# === Create Agent (only once) ===
def create_weather_agent() -> Agent:
    provider = OpenAIProvider(api_key=OPENAI_API_KEY)
    model = OpenAIModel(model_name="gpt-4", provider=provider)
    return Agent(
        model=model,
        result_type=WeatherInterpretation,
        system_prompt="You are a music prompt designer. Interpret weather data and optionally a journal entry to suggest a music generation prompt that reflects emotional and atmospheric conditions."
    )

# === Main Function ===
def interpret_weather_to_music_prompt(
    weather: Dict,
    journal: Optional[str] = "",
    image_caption: Optional[str] = ""
) -> WeatherInterpretation:
    """
    Generate a music prompt based on weather data, journal entry, and optional image caption.

    Args:
        weather: dict with keys: city, temperature, humidity, weather_main, weather_desc, wind_speed
        journal: optional string (user's journal entry)
        image_caption: optional string (description of uploaded image)

    Returns:
        WeatherInterpretation object
    """
    agent = create_weather_agent()

    base_prompt = f"""
    Location: {weather['city']}
    Temperature: {weather['temperature']} °C
    Weather: {weather['weather_main']} ({weather['weather_desc']})
    Wind Speed: {weather['wind_speed']} m/s
    Humidity: {weather['humidity']}%
    """

    if journal.strip():
        base_prompt += f"\n\nJournal entry:\n{journal.strip()}"

    if image_caption.strip():
        base_prompt += f"\n\nImage description:\n{image_caption.strip()}"

    base_prompt += """

    Please reflect on the emotional and atmospheric tone that arises from this combination of weather, personal reflection, and visual context.

    Then, provide:
    1. A short, poetic or natural language summary that captures the mood and feel of the day.
    2. Three evocative mood keywords that summarize this overall feeling.
    3. A creative music generation prompt in the style of Stable Audio. Use rich musical language to describe the sound. You may follow this structure for clarity, but feel free to adjust creatively:

    Format: [Solo/Band/Orchestra] |
    Genre: [e.g., Ambient, Chillout, Hip Hop] |
    Subgenre: [optional] |
    Instruments: [e.g., synth pads, acoustic guitar, drum machine] |
    Moods: [mood1, mood2, mood3] |
    BPM: [optional] |
    Additional descriptors: [optional, e.g., 'lo-fi texture', 'warm analog vibe']

    The final music prompt should feel like a sonic interpretation of the day’s atmosphere.
    """

    result = agent.run_sync(base_prompt)
    return result.data

# === Example Usage ===
if __name__ == "__main__":
    sample_weather = {
        "city": "London",
        "temperature": 15.3,
        "humidity": 72,
        "weather_main": "Clouds",
        "weather_desc": "broken clouds",
        "wind_speed": 4.6
    }
    sample_journal       = "Feeling a bit tired today after a long week. I walked home through the grey streets and it felt oddly calming—quiet, reflective."
    sample_image_caption = "A person with an umbrella walks through a quiet street with wet pavement and dim city lights reflecting in puddles."

    result = interpret_weather_to_music_prompt(sample_weather, sample_journal, sample_image_caption)
    print("🎯 Summary:", result.summary)
    print("🎼 Mood Keywords:", result.mood_keywords)
    print("🎧 Suggested Prompt:", result.suggested_prompt)