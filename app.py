from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

SYSTEM_PROMPT = """You are AccessMate, a kind, patient, practical AI accessibility assistant.
Help people with disabilities use technology and navigate everyday digital tasks.
Use plain, respectful language. Ask one question at a time when needed.
Offer step-by-step instructions, keyboard alternatives, screen-reader-friendly guidance,
captions/transcription tips, and communication support. Never assume a person's disability.
Do not claim to diagnose, provide emergency services, or control the user's device.
If OpenAI is unavailable, the app will use simple local demo replies."""

def local_reply(message):
    m = message.lower()
    if any(x in m for x in ["screen reader", "talkback", "voiceover", "read screen"]):
        return ("I can help with screen readers. On Android, open Settings → Accessibility → TalkBack. "
                "On iPhone, open Settings → Accessibility → VoiceOver. Menu names may vary by device. "
                "Tell me your device and I’ll give you exact steps.")
    if any(x in m for x in ["caption", "subtitle", "hearing", "deaf"]):
        return ("You can make audio easier to follow by turning on captions or live transcription. "
                "Look in your device’s Accessibility settings for Live Captions, or enable captions in the app "
                "you’re watching. Which device or app are you using?")
    if any(x in m for x in ["blind", "low vision", "see", "visual"]):
        return ("I can suggest options such as larger text, high contrast, screen magnification, and a screen reader. "
                "On most phones, open Settings → Accessibility. Are you using Android, iPhone, Windows, or Mac?")
    if any(x in m for x in ["type", "speech", "speak", "voice"]):
        return ("You may be able to use voice typing or speech-to-text. Look for the microphone on your keyboard, "
                "or check Settings → Accessibility for voice control options. Which device are you using?")
    if any(x in m for x in ["keyboard", "motor", "movement", "click"]):
        return ("Try keyboard navigation: press Tab to move between controls, Shift+Tab to go back, "
                "Enter or Space to activate a control, and Esc to close many dialogs. You can also explore "
                "switch access or voice control in Accessibility settings.")
    if any(x in m for x in ["hello", "hi", "hey", "namaste"]):
        return ("Hello! 👋 I’m AccessMate. I can help with screen readers, captions, voice typing, keyboard access, "
                "and making apps easier to use. What would you like help with?")
    return ("I’m here to help. Tell me what device or app you’re using and what you want to do. "
            "I can guide you step by step. This demo is running in local-help mode; add an OpenAI API key "
            "to enable AI-generated replies.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"reply": "Please type or speak a question first."}), 400

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                instructions=SYSTEM_PROMPT,
                input=message
            )
            return jsonify({"reply": response.output_text, "mode": "ai"})
        except Exception:
            # Keep the app usable if API configuration/network is unavailable.
            pass
    return jsonify({"reply": local_reply(message), "mode": "local"})

if __name__ == "__main__":
    app.run(debug=True)
