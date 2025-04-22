import os
from story_generator import StoryGenerator
from agents import CriticAgent, RefinerAgent, JudgeAgent

def run_puzzle(keywords: str, max_rounds: int = 3) -> dict:

    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    sg = StoryGenerator(api_key)
    raw = sg.generate(keywords)
    start, final = sg.parse_layers(raw)

    for round_idx in range(1, max_rounds+1):
        critic = CriticAgent(client)
        feedback = critic.critique(start, final)

        refiner = RefinerAgent(client)
        new_start, new_final = refiner.refine(start, final, feedback)

        judge = JudgeAgent(client)
        decision, judge_text = judge.evaluate(new_start, new_final)
        if decision == 'ACCEPT':
            return {
                'start_scenario': new_start,
                'final_solution': new_final,
                'judge_decision': judge_text
            }
        start, final = new_start, new_final

    return {
        'start_scenario': start,
        'final_solution': final,
        'judge_decision': judge_text
    }

  
if __name__ == '__main__':
    keywords = "cat, clock, dark alley, old photograph"
    result = run_puzzle(keywords)
    print(result)