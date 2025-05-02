import os
import mimetypes
from typing import Optional
from base64 import b64encode
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel

from config import OPENAI_API_KEY

class ImageCaption(BaseModel):
    description: str

def caption_image_with_gpt4o(image_path: str) -> str:
    api_key = OPENAI_API_KEY

    with open(image_path, "rb") as f:
        image_data = f.read()
    b64_image = b64encode(image_data).decode("utf-8")
    mime_type, _ = mimetypes.guess_type(image_path)
    image_url = f"data:{mime_type};base64,{b64_image}"

    provider = OpenAIProvider(api_key=api_key)
    model  = OpenAIModel(model_name="gpt-4o", provider=provider)

    agent = Agent(
        model=model,
        result_type=ImageCaption,
        system_prompt=(
            "You are an expert image captioning agent. A user has uploaded an image that reflects their current context or environment. "
            "Your task is to describe the image in one complete, natural sentence. Focus entirely on what can be visually observed. "
            "Include key visual elements such as objects, setting, people, actions, posture, lighting, colors, spatial layout, and notable textures. "
            "Do not infer the user's emotions or intentions—just describe the image with precise, concrete detail. "
            "Your description will be combined with other user inputs to create an expressive audio experience."
        )
    )



    user_input = {
        "type": "image_url",
        "image_url": {"url": image_url}
    }

    result = agent.run_sync(
        messages=[
            {"role": "user", "content": [user_input]}
        ]
    )

    return result.data.description

if __name__ == "__main__":
    caption = caption_image_with_gpt4o("./image/test.jpg")
    print("🖼️ Image Caption:", caption)
