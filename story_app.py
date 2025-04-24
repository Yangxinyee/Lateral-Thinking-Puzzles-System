from typing import Optional
from modules.stt_module import SpeechToText
from modules.vlm_module import VisionLanguageModel
from modules.debate_module import PromptSystem
from modules.host_module import TurtleSoupGame
import argparse

class UserInputManager:
    """Handles input from text, local image file, or voice recording."""
    def __init__(self):
        self.speech = SpeechToText()
        self.vlm = VisionLanguageModel()

    def from_text(self, text: str) -> str:
        return text.strip()

    def from_image(self, image_path: str) -> str:
        return self.vlm.extract_keywords(image_path)

    def from_voice(self) -> str:
        return self.speech.record_and_transcribe()

class StoryGameSystem:
    """Core system to create and play an interactive story game."""
    def __init__(self):
        self.prompt_system = PromptSystem()
        self.input_manager = UserInputManager()
        self.game_engine = TurtleSoupGame()

    def generate_and_play(self, *, text: Optional[str] = None, image_path: Optional[str] = None, use_voice: bool = False):
        # Step 1: Gather all available keywords
        keyword_segments = []

        if text:
            keyword_segments.append(self.input_manager.from_text(text))

        if image_path:
            keyword_segments.append(self.input_manager.from_image(image_path))

        if use_voice:
            keyword_segments.append(self.input_manager.from_voice())

        if not keyword_segments:
            raise ValueError("You must provide at least one of the following: text, image_path, or use_voice=True.")

        keywords = ", ".join(keyword_segments)
        print("\nCombined Keywords:", keywords)

        # Step 2: Generate initial story
        story = self.prompt_system.generate_story(keywords)
        print("\nInitial Story:\nStart Scenario:\n", story['scenario'], "\n\nFinal Solution:\n", story['solution'])

        # Step 3: Refine story using debate agents (loop until accepted)
        revised = story
        rounds = 0
        while True:
            rounds += 1
            print(f"\n Debate Round {rounds}:")
            feedback = self.prompt_system.agent_a_feedback(revised)
            revised = self.prompt_system.agent_b_refine(revised, feedback)
            decision = self.prompt_system.judge_evaluation(revised)

            if decision == "ACCEPT":
                print("\n Final Story Accepted by Judge.")
                break
            else:
                print("Judge requested another revision...")

        # Step 4: Display final story
        print("\nFinal Story:\nStart Scenario:\n", revised['scenario'], "\n\nFinal Solution:\n", revised['solution'])

        # Step 5: Launch interactive puzzle game
        print("\nStarting interactive turtle soup puzzle game...")
        self.game_engine.start_game(revised['scenario'], revised['solution'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run interactive Turtle Soup story generation system.")
    parser.add_argument("--text", type=str, help="Optional keyword text input")
    parser.add_argument("--image", type=str, help="Optional image file path for vision model")
    parser.add_argument("--voice", action="store_true", help="Use voice input")

    args = parser.parse_args()

    app = StoryGameSystem()
    app.generate_and_play(
        text=args.text,
        image_path=args.image,
        use_voice=args.voice
    )
