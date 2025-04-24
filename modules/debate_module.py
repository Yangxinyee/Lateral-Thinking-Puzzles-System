import os
import openai
from debate_prompt import (
    SYSTEM_PROMPT,
    INITIAL_STORY_PROMPT,
    AGENT_A_PROMPT,
    AGENT_B_PROMPT,
    JUDGE_PROMPT
)

class PromptSystem:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.ChatCompletion

    def generate_story(self, keywords: str) -> dict:
        prompt = INITIAL_STORY_PROMPT.format(keywords_list=keywords)
        response = self.client.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message["content"]
        scenario, solution = self._split_story(content)
        return {"scenario": scenario, "solution": solution}

    def agent_a_feedback(self, story: dict) -> str:
        prompt = AGENT_A_PROMPT.format(
            scenario=story["scenario"],
            solution=story["solution"]
        )
        response = self.client.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message["content"]

    def agent_b_refine(self, story: dict, agent_a_feedback: str) -> dict:
        prompt = AGENT_B_PROMPT.format(
            scenario=story["scenario"],
            solution=story["solution"],
            agent_a_feedback=agent_a_feedback,
            new_scenario=story["scenario"],
            new_solution=story["solution"]
        )
        response = self.client.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message["content"]
        new_scenario, new_solution = self._split_story(content)
        return {"scenario": new_scenario, "solution": new_solution}

    def judge_evaluation(self, story: dict) -> str:
        prompt = JUDGE_PROMPT.format(
            revised_scenario=story["scenario"],
            revised_solution=story["solution"]
        )
        response = self.client.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message["content"]
        return "ACCEPT" if "<decision>ACCEPT</decision>" in content else "REVISE"

    def _split_story(self, content: str):
        parts = content.split("Final Solution:")
        scenario = parts[0].replace("Start Scenario:", "").strip()
        solution = parts[1].strip() if len(parts) > 1 else ""
        return scenario, solution
