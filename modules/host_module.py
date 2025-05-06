import os
from openai import OpenAI
from dotenv import load_dotenv

class TurtleSoupGame:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def analyze_story_structure(self, puzzle: str, truth: str) -> str:
        system_prompt = (
            "You are a professional story analyst, skilled in deconstructing stories from multiple dimensions.\n"
            "Please analyze the following story from these aspects:\n"
            "1. Timeline: List key events in chronological order\n"
            "2. Causal Relationships: Describe the causal links between events\n"
            "3. Character Motivations: Analyze the psychological motivations of main characters\n"
            "4. Key Turning Points: Identify the major turning points in the story\n"
            "5. Hidden Clues: List important hidden clues embedded in the story\n"
            "6. Emotional Progression: Describe how the characters' emotions evolve throughout the story\n"
            "Please output the analysis in JSON format and include all the above dimensions.\n"
            "Each dimension should be detailed with specific content."
        )

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Puzzle: {puzzle}\nTruth: {truth}"}
            ],
            temperature=0.2
        )
        # return response.choices[0].message['content']
        return response.choices[0].message.content

    def answer_question(self, puzzle: str, truth: str, question: str, story_analysis: str, history: list = None) -> str:
        system_prompt = (
            "You are a professional, humorous, and empathetic host of a Turtle Soup puzzle game.\n"
            "Your goal is to guide the player step by step toward the truth through questioning and reasoning—not by directly revealing the answer.\n"
            "Puzzle: " + puzzle + "\n"
            "Truth: " + truth + "\n"
            "You must strictly refer to structural analysis of the story when guiding the player:\n"
            "You must also strictly refer to conversation history when responding:\n"
            "Please follow these rules when replying:\n"
            "1. If the reasoning is logical and relevant: answer 'Yes'\n"
            "2. If the reasoning is off-topic or irrelevant: answer 'No'\n"
            "3. Maintain mystery: respond briefly and consider using emojis\n"
            "4. Avoid contradictions: check the dialogue history for consistency\n"
            "5. If contradictions exist: point them out without revealing the truth\n"
            "6. Stay coherent: keep your answers consistent with the past conversation\n"
            "7. Do not reason on your own—strictly base your answers on the story, story analysis, and dialogue history\n"
            "8. If you believe the user has already completed the full reasoning process based on the history and current question, say: "
            "'You're very close to the truth. Please organize all your thoughts and tell me your final answer.'"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Puzzle: {puzzle}\nTruth: {truth}\nAnalysis: {story_analysis}"}
        ]

        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": f"Question: {question}"})

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.2
        )
        # return response.choices[0].message['content'].strip()
        return response.choices[0].message.content.strip()

    def check_game_end(self, puzzle: str, truth: str, user_input: str, story_analysis: str, history_text: str) -> str:
        system_prompt = (
            "You are a strict but fair judge in a turtle soup (lateral thinking) puzzle game.\n"
            "Your task is to determine whether the player has fully solved the mystery.\n"
            "You will be given the Puzzle, the Truth, story's structure analysis, the user's dialogue history, and the user's current input.\n"
            "Use this information to make a judgment based on the following criteria:\n"
            "1. The player must fully describe the background of the events.\n"
            "2. The player must accurately describe the key causal chain.\n"
            "3. The player must explain the motivations of the characters.\n"
            "4. The player must mention the final outcome.\n"
            "5. If the player only reveals part of the truth, it does not count as a full solution.\n"
            "6. If the player uses different wording but conveys the same meaning, it should be considered correct.\n"
            "7. If the player includes unrelated details but the core elements are correct, it should still be considered solved.\n"
            "Please respond based on the above criteria with only 'Yes' or 'No'.\n"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Puzzle: {puzzle}\nTruth: {truth}\nAnalysis: {story_analysis}\nHistory: {history_text}\nUser input: {user_input}"}
        ]

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.2
        )
        # result = response.choices[0].message['content'].strip().lower()
        result = response.choices[0].message.content.strip().lower()
        return "end" if "yes" in result else "continue"

    def start_game(self, puzzle: str, truth: str):
        print("\nWelcome to the Turtle Soup Puzzle Game!")
        print("\n" + puzzle + "\n")

        story_analysis = self.analyze_story_structure(puzzle, truth)
        print("Story analysis completed.\n")

        history = []
        history_text = ""

        while True:
            user_input = input("Your question or solution (type 'give up' to reveal the truth): ")
            if user_input.strip().lower() in ["give up", "i give up"]:
                print("\nThe truth was:\n", truth)
                break

            answer = self.answer_question(puzzle, truth, user_input, story_analysis, history)
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": answer})
            history_text += f"Q: {user_input}\nA: {answer}\n"

            print("Answer:", answer)

            end_check = self.check_game_end(puzzle, truth, user_input, story_analysis, history_text)
            if end_check == "end":
                print("🎉 Congratulations! You've reached a sufficient understanding of the truth.")
                break
