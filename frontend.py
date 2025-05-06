import gradio as gr
import whisper
import httpx
import atexit
import asyncio

# Load Whisper model
whisper_model = whisper.load_model("base")

# Backend URL
BASE_URL = "http://localhost:8000"

# Shared HTTPX client with timeout
client = httpx.AsyncClient(timeout=httpx.Timeout(600.0))
atexit.register(lambda: asyncio.run(client.aclose()))

# Transcribe audio to text
def transcribe(audio_path):
    if audio_path is None:
        return ""
    result = whisper_model.transcribe(audio_path)
    return result["text"]

# Validate input and start game
async def start_game(text_input, image_url, voice_text):
    # Require at least one of text or image
    if not text_input.strip() and not image_url.strip() and not voice_text.strip():
        return "", "❌ You must provide either text or an image URL to start.", False

    data = {
        "text": text_input,
        "image_path": image_url,
        "voice_text": voice_text,
    }
    resp = await client.post(f"{BASE_URL}/api/start_game", data=data)
    if resp.status_code == 200:
        puzzle = resp.json().get("puzzle", "")
        return puzzle, "✅ Game started!", True
    else:
        return "", f"❌ Failed to start game: {resp.text}", False

# Ask question
async def ask_question(user_question, history):
    data = {"input": user_question}
    resp = await client.post(f"{BASE_URL}/api/user_input", json=data)
    if resp.status_code != 200:
        return history + [(user_question, f"Error: {resp.text}")], ""
    result = resp.json()
    answer = result.get("response", "")
    if result.get("game_end", False):
        answer += f"\n\n🎉 Game Over! Truth: {result.get('truth', '')}"
    history.append((user_question, answer))
    return history, ""

# UI
with gr.Blocks() as demo:
    gr.Markdown("## 🧩 Puzzle Game")

    game_started = gr.State(False)
    history = gr.State([])

    # ---- Stage 1 ----
    gr.Markdown("### 🎬 Stage 1: Start the Game")

    with gr.Row():
        voice_input = gr.Audio(source="microphone", type="filepath", label="🎙️ Record Voice Prompt")
        transcribe_btn = gr.Button("Transcribe")

    text_input = gr.Textbox(label="Text Input (auto-filled from voice or typed manually)")
    image_url_input = gr.Textbox(label="Image URL (required if no text provided)")
    start_btn = gr.Button("Start Game")

    puzzle_display = gr.Textbox(label="Puzzle", interactive=False)
    status_display = gr.Textbox(label="Status", interactive=False)

    transcribe_btn.click(fn=transcribe, inputs=[voice_input], outputs=[text_input])

    def disable_stage1(puzzle, status, success):
        if success:
            return (
                puzzle,
                status,
                gr.update(interactive=False),
                gr.update(interactive=False),
                gr.update(interactive=False),
                gr.update(interactive=False),
                gr.update(interactive=False)
            )
        else:
            return puzzle, status, gr.update(), gr.update(), gr.update(), gr.update(), gr.update()

    start_btn.click(
        fn=start_game,
        inputs=[text_input, image_url_input, text_input],  # text_input also used for voice_text
        outputs=[puzzle_display, status_display, game_started]
    ).then(
        fn=disable_stage1,
        inputs=[puzzle_display, status_display, game_started],
        outputs=[puzzle_display, status_display, text_input, image_url_input, start_btn, transcribe_btn, voice_input]
    )

    # ---- Stage 2 ----
    gr.Markdown("### 💬 Stage 2: Ask Questions")

    question_input = gr.Textbox(label="Your Question")
    ask_btn = gr.Button("Ask")
    chat_display = gr.Chatbot(label="Game Chat")

    ask_btn.click(
        fn=ask_question,
        inputs=[question_input, history],
        outputs=[chat_display, question_input]
    )

demo.launch()