import os
import streamlit as st

st.set_page_config(page_title="AccessMate AI", page_icon="♿", layout="centered")

SYSTEM_PROMPT = """You are AccessMate, a kind, patient, practical AI accessibility assistant.
Help people with disabilities use technology and navigate everyday digital tasks.
Use plain, respectful language. Ask one question at a time when needed.
Offer step-by-step instructions, keyboard alternatives, screen-reader-friendly guidance,
captions/transcription tips, and communication support. Never assume a person's disability.
Do not claim to diagnose, provide emergency services, or control the user's device.
If OpenAI is unavailable, the app will use simple local demo replies."""


def local_reply(message: str) -> str:
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


def get_reply(message: str):
    # Streamlit secrets can be used on Community Cloud; environment variables work locally too.
    api_key = os.getenv("OPENAI_API_KEY", "")
    try:
        if not api_key:
            api_key = st.secrets.get("OPENAI_API_KEY", "")
    except (FileNotFoundError, KeyError):
        pass

    if api_key:
        try:
            from openai import OpenAI
            model = os.getenv("OPENAI_MODEL", "")
            try:
                model = model or st.secrets.get("OPENAI_MODEL", "gpt-4.1-mini")
            except (FileNotFoundError, KeyError):
                model = model or "gpt-4.1-mini"
            client = OpenAI(api_key=api_key)
            response = client.responses.create(
                model=model,
                instructions=SYSTEM_PROMPT,
                input=message,
            )
            return response.output_text, "AI-powered reply"
        except Exception:
            return local_reply(message), "Local-help mode (AI service unavailable)"
    return local_reply(message), "Local-help mode"


st.title("♿ AccessMate AI")
st.caption("A kind, practical assistant for digital accessibility.")
st.info("Ask about screen readers, captions, visual accessibility, voice typing, or keyboard navigation.")

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! 👋 I’m AccessMate. What accessibility or technology task can I help you with?"
    }]

with st.sidebar:
    st.header("Accessibility support")
    st.write("Try asking about:")
    for prompt in ["How do I turn on TalkBack?", "How can I enable captions?", "How do I make text larger?", "How can I navigate with a keyboard?"]:
        st.markdown(f"- {prompt}")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Hello! 👋 I’m AccessMate. What accessibility or technology task can I help you with?"}]
        st.rerun()
    st.caption("Educational support only; not a medical or emergency service.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Type your accessibility question…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Preparing a helpful response…"):
            reply, mode = get_reply(prompt)
        st.markdown(reply)
        st.caption(mode)
    st.session_state.messages.append({"role": "assistant", "content": reply})
