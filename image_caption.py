import os
import mimetypes
from typing import Optional
from base64 import b64encode
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel

from utils  import load_prompt
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
        system_prompt=load_prompt("prompts/image_caption.txt")
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
