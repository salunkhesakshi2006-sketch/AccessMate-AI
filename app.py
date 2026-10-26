    for label, question in PROMPTS.items():
        if st.button(label, key=f"side_{label}", use_container_width=True):
            st.session_state.pending_prompt = question
            st.session_state.page_override = "💬 AI Assistant"
            st.rerun()
    st.divider()
    if st.button("↺ Clear chat", use_container_width=True):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Hi, I'm AccessMate. Tell me what device you're using and what you'd like to do. We'll take it one step at a time."
        }]
        st.rerun()
    st.markdown("<div style='color:#b7c4df;font-size:.78rem;margin-top:1rem'>Built for clearer, more inclusive digital experiences.</div>", unsafe_allow_html=True)

if "page_override" in st.session_state:
    page = st.session_state.pop("page_override")

if page == "🏠 Home":
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">Accessible technology, made easier</div>
      <h1>More confidence.<br>Fewer digital barriers.</h1>
      <p>Friendly, practical support for screen readers, captions, visual settings, voice typing, and keyboard navigation — one step at a time.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    c1, c2, c3 = st.columns(3)
    cards = [
        ("🗣️", "Screen reader help", "Get started with TalkBack, VoiceOver, and Narrator."),
        ("💬", "Captions & audio", "Explore captions, subtitles, and live transcription."),
        ("⌨️", "Alternative navigation", "Learn keyboard shortcuts and hands-free options."),
    ]
    for col, (icon, title, desc) in zip([c1,c2,c3], cards):
        with col:
            st.markdown(f'<div class="feature-card"><div class="feature-icon">{icon}</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
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
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role":"assistant","content":"Hi, I'm AccessMate. Tell me what device you're using and what you'd like to do. We'll take it one step at a time."}]
    pending = st.session_state.pop("pending_prompt", None)
    if pending:
        st.session_state.messages.append({"role":"user","content":pending})
        reply, mode = get_reply(pending)
        st.session_state.messages.append({"role":"assistant","content":reply})
    render_chat()
    st.caption("Mode: AI replies are enabled when OPENAI_API_KEY is configured; otherwise local demo guidance is used.")

elif page == "🧰 Accessibility Toolkit":
    st.markdown('<div class="section-kicker">Small changes, meaningful impact</div>', unsafe_allow_html=True)
    st.title("Accessibility Toolkit")
    st.write("Explore practical adjustments that may make digital tasks more comfortable.")
    with st.container(border=True):
        st.subheader("🔎 Readability")
        font_size = st.select_slider("Choose a reading size for this preview", options=["Small", "Medium", "Large", "Extra large"], value="Medium")
        contrast = st.toggle("Show high-contrast preview")
        size_map = {"Small":"14px", "Medium":"17px", "Large":"21px", "Extra large":"25px"}
        bg = "#111827" if contrast else "#ffffff"
        fg = "#ffffff" if contrast else "#24324a"
        border = "#111827" if contrast else "#dce5f2"
        st.markdown(f'<div style="background:{bg};color:{fg};border:2px solid {border};border-radius:14px;padding:1.2rem;font-size:{size_map[font_size]};line-height:1.6">This is a preview of readable text. You can adjust text size and contrast to find what feels comfortable.</div>', unsafe_allow_html=True)
        st.caption("This preview changes only the sample below, not your device's system settings.")
    c1,c2 = st.columns(2)
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
    st.caption("Version 2.0 · AccessMate AI")

st.markdown("---")
st.markdown("<div class='small-note'>♿ AccessMate AI · Clear guidance, respectful support, more accessible technology.</div>", unsafe_allow_html=True)
