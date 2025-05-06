import os
from dotenv import load_dotenv
from openai import OpenAI

# load ur API keys
load_dotenv(override=True)  # load from .env file and overide os variables
HF_API_KEY = os.getenv('HF_TOKEN')  # ur hugging face api key

# set ur query img url
img_url = "https://raw.githubusercontent.com/Wonder947/Public-Images/refs/heads/main/examples/718616-bart.png"

# get VLM response
client = OpenAI(
    # base_url="https://router.huggingface.co/hf-inference/models/Qwen/Qwen2-VL-7B-Instruct/v1",
    base_url="https://router.huggingface.co/nebius/v1",
    api_key=HF_API_KEY
)

completion = client.chat.completions.create(
    model="Qwen/Qwen2-VL-7B-Instruct",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    # "text": "Describe this image in one sentence."
                    "text": "Describe this image in one or two sentences. Do not simply list visible objects—instead, highlight any unusual, emotional, or contradictory elements that could hint at a hidden backstory. Focus on the scene’s setting, character actions or expressions, and anything that feels mysterious, out of place, or unexplained. The goal is to inspire a lateral thinking puzzle."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        # "url": "https://cdn.britannica.com/61/93061-050-99147DCE/Statue-of-Liberty-Island-New-York-Bay.jpg"
                        "url": img_url
                    }
                }
            ]
        }
    ],
    max_tokens=512,
)

print(completion.choices[0].message)
