# backend.py

from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional

from story_app import StoryGameSystem
from modules.host_module import TurtleSoupGame


# global game session
class GameSession:
    def __init__(self):
        self.puzzle = None
        self.truth = None
        self.story_analysis = None
        self.history = []
        self.history_text = ""
        self.is_game_over = False
        self.latest_response = ""



# Initialize FastAPI app
app = FastAPI()

# Initialize core systems
game_system = StoryGameSystem()
game_engine = TurtleSoupGame()
game_session = GameSession()  # Global single session (for now)

@app.get("/")
def root():
    return {"message": "hi~ POST /api/start_game to start, POST /api/user_input to ask."}

@app.post("/api/start_game")
async def start_game(
    text: Optional[str] = Form(None),
    image_path: Optional[str] = Form(None),
    voice_text: Optional[str] = Form(None)
):
    """
    Start a new game.
    Inputs:
    - text: optional text input
    - image: optional image path
    - voice_text: optional text transcribed from voice
    """
    keyword_segments = []
    if text:
        keyword_segments.append(game_system.input_manager.from_text(text))
    if image_path:
        keyword_segments.append(game_system.input_manager.from_image(image_path))
    if voice_text:
        keyword_segments.append(voice_text.strip())

    if not keyword_segments:
        return {"error": "You must provide at least one input: text, image, or voice."}

    keywords = ", ".join(keyword_segments)

    story = game_system.prompt_system.generate_story(keywords)

    # Use debate system to refine
    revised = story
    rounds = 0
    while True:
        rounds += 1
        feedback = game_system.prompt_system.agent_a_feedback(revised)
        revised = game_system.prompt_system.agent_b_refine(revised, feedback)
        decision = game_system.prompt_system.judge_evaluation(revised)
        if decision == "ACCEPT":
            break

    # ----------------------------
    # Initialize game session
    # ----------------------------
    game_session.puzzle = revised['scenario']
    game_session.truth = revised['solution']
    game_session.story_analysis = game_engine.analyze_story_structure(game_session.puzzle, game_session.truth)
    game_session.history = []
    game_session.history_text = ""
    game_session.is_game_over = False
    game_session.latest_response = ""

    return {
        "puzzle": game_session.puzzle,
        "message": "Game started!"
    }

class UserInput(BaseModel):
    input: str

@app.post("/api/user_input")
async def user_input_post(user_input: UserInput):
    """
    Post a user question.
    """
    if game_session.is_game_over:
        return {
            "game_end": True,
            "message": "Game already ended. Please restart.",
            "truth": game_session.truth
        }

    user_question = user_input.input.strip()

    if user_question.lower() in ["give up", "i give up"]:
        game_session.is_game_over = True
        return {
            "game_end": True,
            "message": "Game over. Here is the truth.",
            "truth": game_session.truth
        }

    # Process the user's question
    answer = game_engine.answer_question(
        puzzle=game_session.puzzle,
        truth=game_session.truth,
        question=user_question,
        story_analysis=game_session.story_analysis,
        history=game_session.history
    )

    # Update session state
    game_session.history.append({"role": "user", "content": user_question})
    game_session.history.append({"role": "assistant", "content": answer})
    game_session.history_text += f"Q: {user_question}\nA: {answer}\n"
    game_session.latest_response = answer

    # Check if the game should end
    end_check = game_engine.check_game_end(
        puzzle=game_session.puzzle,
        truth=game_session.truth,
        user_input=user_question,
        story_analysis=game_session.story_analysis,
        history_text=game_session.history_text
    )
    if end_check == "end":
        game_session.is_game_over = True

    return {
        "game_end": game_session.is_game_over,
        "response": answer,
        "truth": game_session.truth if game_session.is_game_over else None
    }


