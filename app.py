import os
import streamlit as st

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

st.set_page_config(
    page_title="AccessMate AI",
    page_icon="♿",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROMPTS = {
    "🗣️ Screen readers": "Help me get started with a screen reader on my device.",
    "💬 Captions": "Show me how to turn on captions or live transcription.",
    "⌨️ Keyboard access": "Help me navigate my device using the keyboard.",
    "🔎 Readability": "Help me make text easier to read on my device.",
    "🎙️ Voice typing": "Help me use voice typing or dictation.",
}

GUIDES = {
    "Windows PC": [
        ("Turn on Narrator", "Press **Ctrl + Windows + Enter** to turn Narrator on or off. You can also open **Settings → Accessibility → Narrator**."),
        ("Make text larger", "Open **Settings → Accessibility → Text size** and move the slider. Select **Apply** if shown."),
        ("Turn on captions", "Open **Settings → Accessibility → Captions** and adjust the caption style."),
        ("Use keyboard navigation", "Use **Tab** to move forward, **Shift + Tab** to move backward, and **Enter** or **Space** to activate a focused control."),
    ],
    "Mac": [
        ("Turn on VoiceOver", "Press **Command + F5** to toggle VoiceOver on supported Macs. You can also open **System Settings → Accessibility → VoiceOver**."),
        ("Make text larger", "Open **System Settings → Displays** to adjust display scaling, and check **Accessibility → Display** for additional options."),
        ("Turn on captions", "Open **System Settings → Accessibility → Captions** where available."),
        ("Use keyboard navigation", "Open **System Settings → Keyboard** and review keyboard navigation settings. Shortcuts can vary by macOS version."),
    ],
    "Android phone/tablet": [
        ("Turn on TalkBack", "Open **Settings → Accessibility → TalkBack** and switch it on. On some devices, the menu names differ."),
        ("Make text larger", "Open **Settings → Display → Font size** or **Display size** and adjust the sliders."),
        ("Turn on captions", "Open **Settings → Accessibility → Caption preferences** or search Settings for **Live Caption**."),
        ("Use voice typing", "Open the keyboard in a text field and tap the microphone icon, if available. Review dictated text before sending."),
    ],
    "iPhone/iPad": [
        ("Turn on VoiceOver", "Open **Settings → Accessibility → VoiceOver** and switch it on. You can also configure the Accessibility Shortcut."),
        ("Make text larger", "Open **Settings → Display & Brightness → Text Size**. For larger sizes, check **Accessibility → Display & Text Size → Larger Text**."),
        ("Turn on captions", "Open **Settings → Accessibility → Subtitles & Captioning**. Availability varies by app and content."),
        ("Use voice typing", "Open a text field, tap the microphone on the keyboard, and dictate. Check the text before sharing it."),
    ],
}

LOCAL_RESPONSES = [
    ("screen reader", "A screen reader reads on-screen text and controls aloud. First, tell me your device (Windows, Mac, Android, or iPhone/iPad). Then open its Accessibility settings and look for Narrator, VoiceOver, or TalkBack. Start with the built-in tutorial and try it somewhere low-risk."),
    ("talkback", "On most Android devices, open **Settings → Accessibility → TalkBack** and switch it on. Menu names vary by manufacturer. TalkBack changes touch gestures, so follow the on-screen tutorial and learn how to turn it off before exploring."),
    ("voiceover", "On iPhone or Mac, open **Settings/System Settings → Accessibility → VoiceOver** and switch it on. You can also use the VoiceOver shortcut on supported devices. Follow the built-in tutorial first."),
    ("narrator", "On Windows, press **Ctrl + Windows + Enter** to toggle Narrator on supported versions, or open **Settings → Accessibility → Narrator**. The Narrator Home window offers a quick-start guide."),
    ("caption", "Try your device's **Accessibility** settings and look for **Captions**, **Live Caption**, or **Subtitles & Captioning**. Some apps have their own caption button, often shown as **CC**. Captions depend on the app, device, language, and content."),
    ("keyboard", "Use **Tab** to move to the next control, **Shift + Tab** to move backward, and **Enter** or **Space** to activate a focused button. **Esc** closes many menus. The exact shortcuts depend on the app."),
    ("text", "To make text easier to read, check your device's **Accessibility** settings for text size, display scaling, contrast, or color filters. You can also zoom in many apps with **Ctrl + +** on Windows or **Command + +** on Mac."),
    ("voice typing", "Open a text field and look for the microphone icon on your keyboard, or search your device settings for **voice typing** or **dictation**. Speak clearly, then review the text for errors before sending."),
    ("default", "I can help you work through accessibility settings one step at a time. Tell me which device and app you're using, what you're trying to do, and what you see on the screen. Avoid sharing passwords or other sensitive information.")
]

def get_reply(question: str):
    """Return an answer and the mode used (AI or local demo)."""
    api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", "")).strip()
    if api_key and OpenAI is not None:
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are AccessMate, a friendly digital accessibility guide. "
                            "Give safe, concise, numbered steps. Ask for the device or app if needed. "
                            "Explain that menu names vary by version. Never request passwords or sensitive data. "
                            "Do not claim to change device settings yourself."
                        ),
                    },
                    {"role": "user", "content": question},
                ],
                temperature=0.4,
                max_tokens=500,
            )
            answer = response.choices[0].message.content
            if answer:
                return answer.strip(), "AI"
        except Exception:
            pass

    lowered = question.lower()
    for keyword, answer in LOCAL_RESPONSES:
        if keyword != "default" and keyword in lowered:
            return answer, "Local demo"
    return LOCAL_RESPONSES[-1][1], "Local demo"


def render_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask about accessibility settings…")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Preparing helpful steps…"):
                reply, mode = get_reply(prompt)
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.last_mode = mode


st.markdown(
    """
    <style>
    .stApp { background: #f5f7fb; color: #24324a; }
    [data-testid="stSidebar"] { background: #14213d; }
    [data-testid="stSidebar"] * { color: #f5f7ff; }
    .hero {
        padding: 2.2rem 2.4rem; border-radius: 24px;
        background: linear-gradient(125deg, #173b70 0%, #2866a8 58%, #4d9ac7 100%);
        color: white; margin-bottom: 1.2rem;
        box-shadow: 0 12px 30px rgba(28, 64, 112, .15);
    }
    .hero .eyebrow { text-transform: uppercase; letter-spacing: .12em; font-size: .78rem; font-weight: 700; opacity: .9; }
    .hero h1 { color: white; font-size: clamp(2rem, 4vw, 3.1rem); line-height: 1.12; margin: .6rem 0; }
    .hero p { color: #eef6ff; font-size: 1.08rem; max-width: 780px; margin-bottom: 0; }
    .feature-card {
        min-height: 175px; padding: 1.25rem; background: white;
        border: 1px solid #e0e7f1; border-radius: 18px;
        box-shadow: 0 5px 18px rgba(20, 45, 80, .05);
    }
    .feature-icon { font-size: 1.8rem; }
    .feature-card h3 { font-size: 1.12rem; margin: .6rem 0 .35rem; color: #173b70; }
    .feature-card p { font-size: .94rem; color: #58677d; }
    .section-kicker { color: #2866a8; font-size: .78rem; text-transform: uppercase; letter-spacing: .12em; font-weight: 750; margin-bottom: .35rem; }
    .small-note { color: #6b7890; font-size: .82rem; text-align: center; padding: .8rem 0 1.2rem; }
    div.stButton > button { border-radius: 10px; min-height: 2.7rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hi, I'm AccessMate. Tell me what device you're using and what you'd like to do. We'll take it one step at a time.",
    }]

with st.sidebar:
    st.markdown("## ♿ AccessMate AI")
    st.caption("Your friendly accessibility guide")
    st.divider()
    page = st.radio(
        "Navigate",
        ["🏠 Home", "💬 AI Assistant", "🧰 Accessibility Toolkit", "📱 Device Guides", "ℹ️ About"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("### Quick questions")
    for label, question in PROMPTS.items():
        if st.button(label, key=f"side_{label}", use_container_width=True):
            st.session_state.pending_prompt = question
            st.session_state.page_override = "💬 AI Assistant"
            st.rerun()
    st.divider()
    if st.button("↺ Clear chat", use_container_width=True):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Hi, I'm AccessMate. Tell me what device you're using and what you'd like to do. We'll take it one step at a time.",
        }]
        st.rerun()
    st.markdown(
        "<div style='color:#b7c4df;font-size:.78rem;margin-top:1rem'>Built for clearer, more inclusive digital experiences.</div>",
        unsafe_allow_html=True,
    )

if "page_override" in st.session_state:
    page = st.session_state.pop("page_override")

if page == "🏠 Home":
    st.markdown(
        """
        <div class="hero">
          <div class="eyebrow">Accessible technology, made easier</div>
          <h1>More confidence.<br>Fewer digital barriers.</h1>
          <p>Friendly, practical support for screen readers, captions, visual settings, voice typing, and keyboard navigation — one step at a time.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    cards = [
        ("🗣️", "Screen reader help", "Get started with TalkBack, VoiceOver, and Narrator."),
        ("💬", "Captions & audio", "Explore captions, subtitles, and live transcription."),
        ("⌨️", "Alternative navigation", "Learn keyboard shortcuts and hands-free options."),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3], cards):
        with col:
            st.markdown(
                f'<div class="feature-card"><div class="feature-icon">{icon}</div><h3>{title}</h3><p>{desc}</p></div>',
                unsafe_allow_html=True,
            )
    st.write("")
    st.markdown('<div class="section-kicker">Start here</div>', unsafe_allow_html=True)
    st.subheader("What would you like help with?")
    cols = st.columns(5)
    for col, (label, question) in zip(cols, PROMPTS.items()):
        with col:
            if st.button(label, key=f"home_{label}", use_container_width=True):
                st.session_state.pending_prompt = question
                st.session_state.page_override = "💬 AI Assistant"
                st.rerun()
    st.write("")
    with st.container(border=True):
        st.markdown("### ✨ How AccessMate works")
        a, b, c = st.columns(3)
        a.markdown("**1. Tell us your goal**\n\nDescribe what you want to do in everyday language.")
        b.markdown("**2. Get clear steps**\n\nReceive practical suggestions and device-specific tips.")
        c.markdown("**3. Choose what works**\n\nTry the steps that feel useful and comfortable for you.")
    st.caption("AccessMate is an educational support tool. Features and menu names can vary by device and software version.")

elif page == "💬 AI Assistant":
    st.markdown('<div class="section-kicker">Your friendly guide</div>', unsafe_allow_html=True)
    st.title("Ask AccessMate")
    st.write("Ask a question in your own words. You don't need to know the name of a setting.")
    pending = st.session_state.pop("pending_prompt", None)
    if pending:
        st.session_state.messages.append({"role": "user", "content": pending})
        reply, mode = get_reply(pending)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.last_mode = mode
    render_chat()
    st.caption(f"Mode: {st.session_state.get('last_mode', 'AI or local demo')} replies. Configure OPENAI_API_KEY in Streamlit Secrets to enable AI-generated replies.")

elif page == "🧰 Accessibility Toolkit":
    st.markdown('<div class="section-kicker">Small changes, meaningful impact</div>', unsafe_allow_html=True)
    st.title("Accessibility Toolkit")
    st.write("Explore practical adjustments that may make digital tasks more comfortable.")
    with st.container(border=True):
        st.subheader("🔎 Readability")
        font_size = st.select_slider(
            "Choose a reading size for this preview",
            options=["Small", "Medium", "Large", "Extra large"],
            value="Medium",
        )
        contrast = st.toggle("Show high-contrast preview")
        size_map = {"Small": "14px", "Medium": "17px", "Large": "21px", "Extra large": "25px"}
        bg = "#111827" if contrast else "#ffffff"
        fg = "#ffffff" if contrast else "#24324a"
        border = "#111827" if contrast else "#dce5f2"
        st.markdown(
            f'<div style="background:{bg};color:{fg};border:2px solid {border};border-radius:14px;padding:1.2rem;font-size:{size_map[font_size]};line-height:1.6">This is a preview of readable text. You can adjust text size and contrast to find what feels comfortable.</div>',
            unsafe_allow_html=True,
        )
        st.caption("This preview changes only the sample below, not your device's system settings.")
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("⌨️ Keyboard navigation")
            st.markdown("- **Tab:** move forward between controls\n- **Shift + Tab:** move backward\n- **Enter / Space:** activate a focused control\n- **Esc:** close many menus and dialogs")
    with c2:
        with st.container(border=True):
            st.subheader("🎧 Audio & communication")
            st.markdown("- Turn on captions when available\n- Try live transcription for conversations\n- Use voice typing to dictate text\n- Check audio, microphone, and caption settings")
    st.info("Tip: You can ask the AI Assistant for instructions tailored to your device and app.")

elif page == "📱 Device Guides":
    st.markdown('<div class="section-kicker">Step-by-step starting points</div>', unsafe_allow_html=True)
    st.title("Device Guides")
    st.write("Choose your device to see common accessibility settings. Menu names may vary by version.")
    device = st.selectbox("Select a device", list(GUIDES.keys()))
    for title, body in GUIDES[device]:
        with st.expander(title, expanded=False):
            st.markdown(body)
    st.divider()
    st.subheader("Need help with a specific app?")
    app_name = st.text_input("App or task (optional)", placeholder="e.g., YouTube captions, reading a PDF")
    if st.button("Ask AccessMate about this", type="primary"):
        question = f"I'm using {device}. Help me with {app_name or 'accessibility settings'} step by step."
        st.session_state.pending_prompt = question
        st.session_state.page_override = "💬 AI Assistant"
        st.rerun()

elif page == "ℹ️ About":
    st.markdown('<div class="section-kicker">Designed around independence</div>', unsafe_allow_html=True)
    st.title("About AccessMate AI")
    st.write("AccessMate is a student-friendly accessibility assistant concept that offers respectful, practical help with everyday digital technology.")
    with st.container(border=True):
        st.subheader("What it can help with")
        st.markdown("- Screen readers and spoken feedback\n- Captions and transcription\n- Display settings and readability\n- Voice typing and keyboard access\n- Device-specific step-by-step guidance")
    with st.container(border=True):
        st.subheader("Technology")
        st.markdown("Built with **Python and Streamlit**, with optional **OpenAI API** integration. When no API key is configured, the app uses local demo responses.")
    st.warning("AccessMate is not a medical, legal, or emergency service. It does not control your device, and it never needs you to share sensitive personal details.")
    st.caption("Version 2.1 · AccessMate AI")

st.markdown("---")
st.markdown(
    "<div class='small-note'>♿ AccessMate AI · Clear guidance, respectful support, more accessible technology.</div>",
    unsafe_allow_html=True,
)
