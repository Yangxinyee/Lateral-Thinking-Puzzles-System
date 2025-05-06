import gradio as gr
import whisper
import asyncio
import httpx

# Load Whisper model
whisper_model = whisper.load_model("base")
BASE_URL = "http://localhost:8000"

# Transcribe audio using Whisper
def transcribe(audio_path):
    if audio_path is None:
        return ""
    result = whisper_model.transcribe(audio_path)
    return result["text"]

# Call backend to start the game
async def start_game(text_input, image_path):
    data = {
        "text": text_input,
        "image_path": image_path,
        # "use_voice": False,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/api/start_game", data=data, timeout=100)
    if resp.status_code == 200:
        puzzle = resp.json().get("puzzle", "")
        return puzzle, "Game started!", True
    else:
        return "", f"Failed to start game: {resp.text}", False

# Ask a user question
async def ask_question(user_question, history):
    data = {"input": user_question}
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/api/user_input", json=data)
    if resp.status_code != 200:
        return history + [(user_question, f"Error: {resp.text}")], ""

    result = resp.json()
    answer = result.get("response", "")
    if result.get("game_end", False):
        answer += f"\n\n🎉 Game Over! Truth: {result.get('truth', '')}"
    history.append((user_question, answer))
    return history, ""

# UI definition
with gr.Blocks() as demo:
    gr.Markdown("## 🧩 Puzzle Game")

    game_started = gr.State(False)
    history = gr.State([])

    # ---------- Stage 1 ----------
    gr.Markdown("### 🎬 Stage 1: Start the Game")

    with gr.Row():
        voice_input = gr.Audio(sources=["microphone"], type="filepath", label="🎙️ Record Voice Prompt")
        transcribe_btn = gr.Button("Transcribe")
    text_input = gr.Textbox(label="Text Input (filled after transcription or typed manually)")
    image_path = gr.Textbox(label="Image Path (optional)")
    start_btn = gr.Button("Start Game")

    puzzle_display = gr.Textbox(label="Puzzle", interactive=False)
    status_display = gr.Textbox(label="Status", interactive=False)

    # Transcribe voice and update text input
    transcribe_btn.click(
        fn=transcribe,
        inputs=[voice_input],
        outputs=[text_input]
    )

    # Disable inputs after game starts
    def disable_inputs(puzzle, status, success):
        if success:
            return (
                puzzle,
                status,
                gr.update(interactive=False),
                gr.update(interactive=False),
                gr.update(interactive=False),
                gr.update(interactive=False)
            )
        else:
            return puzzle, status, gr.update(), gr.update(), gr.update(), gr.update()

    start_btn.click(
        fn=lambda t, i: asyncio.run(start_game(t, i)),
        inputs=[text_input, image_path],
        outputs=[puzzle_display, status_display, game_started]
    ).then(
        fn=disable_inputs,
        inputs=[puzzle_display, status_display, game_started],
        outputs=[puzzle_display, status_display, text_input, image_path, start_btn, transcribe_btn]
    )

    # ---------- Stage 2 ----------
    gr.Markdown("### 💬 Stage 2: Ask Questions")

    question_input = gr.Textbox(label="Your Question")
    ask_btn = gr.Button("Ask")
    chat_display = gr.Chatbot(label="Chat History")

    ask_btn.click(
        fn=lambda q, h: asyncio.run(ask_question(q, h)),
        inputs=[question_input, history],
        outputs=[chat_display, question_input]
    )

demo.launch()