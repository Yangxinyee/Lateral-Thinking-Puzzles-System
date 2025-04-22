from openai import OpenAI
from prompt import AGENT_A_PROMPT


class CriticAgent:
    def __init__(self, client: OpenAI, model: str = "gpt-4", temperature: float = 0.0, max_tokens: int = 300):
        self.client = client
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def critique(self, scenario: str, solution: str) -> str:
        prompt = AGENT_A_PROMPT.format(scenario=scenario, solution=solution)
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return resp.choices[0].message.content
      
class RefinerAgent:
    def __init__(self, client: OpenAI, model: str = "gpt-4", temperature: float = 0.0, max_tokens: int = 300):
        self.client = client
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def refine(self, scenario: str, solution: str, feedback: str) -> tuple[str, str]:
        prompt = AGENT_B_PROMPT.format(
            agent_a_feedback=feedback,
            scenario=scenario,
            solution=solution,
            new_scenario="",
            new_solution=""
        )
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        text = resp.choices[0].message.content

        return StoryGenerator.parse_layers(text)

class JudgeAgent:

    def __init__(self, client: OpenAI, model: str = "gpt-4", temperature: float = 0.0, max_tokens: int = 150):
        self.client = client
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def evaluate(self, scenario: str, solution: str) -> tuple[str, str]:
        prompt = JUDGE_PROMPT.format(revised_scenario=scenario, revised_solution=solution)
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        text = resp.choices[0].message.content

        m = re.search(r"<decision>(ACCEPT|REVISE)</decision>", text)
        decision = m.group(1) if m else 'REVISE'
        return decision, text