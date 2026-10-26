# AccessMate AI — Streamlit Accessibility Assistant

AccessMate AI provides practical, respectful guidance about screen readers, captions, visual accessibility, voice typing, and keyboard navigation.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

## Deploy on Streamlit Community Cloud

1. Upload `app.py`, `requirements.txt`, and this `README.md` to the root of your GitHub repository.
2. In Streamlit Community Cloud, set **Main file path** to `app.py`.
3. Deploy or reboot the app.
4. Optional: add `OPENAI_API_KEY = "your-api-key"` to the app's Streamlit Secrets to enable AI-generated replies. Without a key, local demo guidance still works.

## Important

- This project is a Streamlit app. Do not use a Flask version of `app.py`.
- Never commit API keys to GitHub.
- This is an educational accessibility-support project, not a medical or emergency service.
