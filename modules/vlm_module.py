import os
from dotenv import load_dotenv
from openai import OpenAI

class VisionLanguageModel:
    def __init__(self):
        load_dotenv(override=True)
        hf_api_key = os.getenv('HF_TOKEN')

        self.client = OpenAI(
            # base_url="https://router.huggingface.co/hf-inference/models/Qwen/Qwen2-VL-7B-Instruct/v1",
            base_url="https://router.huggingface.co/nebius/v1",
            api_key=hf_api_key
        )

    def extract_keywords(self, image_url: str) -> str:
        print(f"Processing image for keyword extraction: {image_url}")
        completion = self.client.chat.completions.create(
            model="Qwen/Qwen2-VL-7B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe this image in one or two sentences. Do not simply list visible objects—instead, highlight any unusual, emotional, or contradictory elements that could hint at a hidden backstory. Focus on the scene’s setting, character actions or expressions, and anything that feels mysterious, out of place, or unexplained. The goal is to inspire a lateral thinking puzzle."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],
            max_tokens=512,
        )

        # response_text = completion.choices[0].message['content']
        response_text = completion.choices[0].message.content.strip()
        print("Extracted description:", response_text)
        return response_text
