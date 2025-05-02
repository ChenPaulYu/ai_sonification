from typing import Dict, Optional
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from config import OPENAI_API_KEY
from utils  import load_prompt

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
        system_prompt=load_prompt("prompts/weather_music_system.txt")
    )

# === Main Function ===
def interpret_weather_to_music_prompt(
    weather: Dict,
    journal: Optional[str] = "",
    image_caption: Optional[str] = ""
) -> WeatherInterpretation:
    agent = Agent(
        model=create_weather_agent().model,
        result_type=WeatherInterpretation,
        system_prompt=load_prompt("prompts/weather_music_system.txt")
    )

    dynamic_context = f"""
    Location: {weather['city']}
    Temperature: {weather['temperature']} °C
    Weather: {weather['weather_main']} ({weather['weather_desc']})
    Wind Speed: {weather['wind_speed']} m/s
    Humidity: {weather['humidity']}%
    """

    if journal.strip():
        dynamic_context += f"\n\nJournal entry:\n{journal.strip()}"

    if image_caption.strip():
        dynamic_context += f"\n\nImage description:\n{image_caption.strip()}"

    base_prompt = dynamic_context + "\n\n" + load_prompt("prompts/weather_music_base.txt")

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