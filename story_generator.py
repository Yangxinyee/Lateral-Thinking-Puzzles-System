from openai import OpenAI
import re
from prompt import SYSTEM_PROMPT, INITIAL_STORY_PROMPT

class StoryGenerator:
    def __init__(self, api_key: str, model: str = "gpt-4", temperature: float = 0.0, max_tokens: int = 300):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, keywords_list: str) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": INITIAL_STORY_PROMPT.format(keywords_list=keywords_list)}
        ]
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return resp.choices[0].message.content

    @staticmethod
    def parse_layers(text: str) -> tuple[str, str]:
        parts = re.split(r"Start Scenario:|Final Solution:", text)
        if len(parts) >= 3:
            start = parts[1].strip()
            final = parts[2].strip()
        else:
            # fallback entire text as scenario
            start, final = text.strip(), ''
        return start, final
