import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from langdetect import detect
from io import BytesIO
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

st.set_page_config(
    page_title="AI Translator",
    page_icon="🌍"
)

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

h1 {
    text-align: center;
}

[data-testid="stTextArea"] {
    border-radius: 15px;
}

[data-testid="stSelectbox"] {
    border-radius: 15px;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 18px;
}

.stDownloadButton > button {
    width: 100%;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
    
if "translated" not in st.session_state:
    st.session_state.translated = ""

if "detected_language" not in st.session_state:
    st.session_state.detected_language = ""

if "source_text" not in st.session_state:
    st.session_state.source_text = ""

if "text_area_key" not in st.session_state:
    st.session_state.text_area_key = 0

clear_btn = False

languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Russian": "ru",
    "Arabic": "ar",
    "Korean": "ko",
    "Italian": "it",
    "Portuguese": "pt",
    "Turkish": "tr",
    "Dutch": "nl",
    "Greek": "el"
}

language_names = {
    "en": "English",
    "hi": "Hindi",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "ja": "Japanese",
    "zh-cn": "Chinese",
    "ru": "Russian",
    "ar": "Arabic",
    "ko": "Korean",
    "it": "Italian",
    "pt": "Portuguese",
    "tr": "Turkish",
    "nl": "Dutch",
    "el": "Greek"
}

with st.sidebar:

    st.markdown("""
    #  Dashboard
    """)
    st.success("System Online")

    st.markdown("---")

    st.write("### Features")

    with st.expander("📋 View Features"):

        st.write("🌍 Multi-language Support")
        st.write("🔍 Language Detection")
        st.write("⚡ Google Translate Engine")
        st.write("🤖 Gemini AI Engine")
        st.write("🔊 Text-to-Speech")
        st.write("📜 Translation History")
        st.write("📥 Download Translation")
        st.write("### 🌐 Languages Supported")
        st.write(f"**{len(languages)} Languages**")

    
    st.markdown("---")
    
    st.write("###  Translation History")

    with st.expander("📜 Translation History"):

        for index, item in enumerate(
            reversed(st.session_state.history),
            start=1
        ):

            preview = item["source"][:35]

            st.markdown(f"### #{index}")
            st.caption(preview + "...")
            st.caption(f"🌍 {item['language']}")
            st.caption(f"🤖 {item['engine']}")
            st.markdown("---")


    if  st.button("🗑 Clear History"):
        st.session_state.history = []
        st.session_state.translated = ""
        st.rerun()

    st.markdown("---")

    st.write("### 👨‍💻 Developer")
    st.write(" Tushar Patel")
    st.write("Version 2.0")

st.markdown("""
<h1 style='text-align:center;
color:#4CAF50;'>
🌍 AI Language Translator
</h1>

<h4 style='text-align:center;
color:gray;'>
Translate Any Language Instantly
</h4>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center; color:gray;'>
Translate text instantly into multiple languages using AI-powered translation.
</p>
""", unsafe_allow_html=True)

source_col, output_col = st.columns(2)

with source_col:
    text = st.text_area(
        "📝Source Text",
        key=f"source_text_{st.session_state.text_area_key}",
        height=180,
        placeholder="Type or paste text here..."
    )

    st.caption(f"Characters: {len(text)}")


target_language = st.selectbox(
    "Select Target Language",
    list(languages.keys())
)

translation_engine = st.radio(
    "Choose Translation Engine",
    ["Google Translate", "Gemini AI"]
)

translate_btn = st.button("🚀 Translate")

st.info(f"Translating to: {target_language}")



col1, col2 = st.columns(2)

with col1:
    st.metric("Characters", len(text))

with col2:
    st.metric("Words", len(text.split()))


if translate_btn:

    if text:

        try:

            if translation_engine == "Google Translate":

                translated = GoogleTranslator(
                    source="auto",
                    target=languages[target_language]
                ).translate(text)

            else:

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                prompt = f"""
                Translate the following text into {target_language}.

                Return ONLY the translated text.
                Do not explain anything.

                Text:
                {text}
                """

                response = model.generate_content(prompt)

                translated = response.text.strip()

            try:
                detected_code = detect(text)

                st.session_state.detected_language = (
                language_names.get(
                detected_code.lower(),
                detected_code.upper()
                )
            )

            except:
                st.session_state.detected_language = "Unknown"
            
            
            st.session_state.translated = translated
            st.toast("Translation completed successfully!")

            audio_buffer = BytesIO()

            tts = gTTS(
                text=translated,
                lang=languages[target_language]
            )

            tts.write_to_fp(audio_buffer)

            audio_buffer.seek(0)

            if st.session_state.detected_language:

                colA, colB = st.columns(2)

                with colA:
                    st.info(
                        f"🌐 Source: {st.session_state.detected_language}"
                    )
                    
                with colB:
                    st.info(
                        f"🎯 Target: {target_language}"
                    )

            st.audio(
                audio_buffer.read(),
                format="audio/mp3"
            )

            entry = {
                "source": text,
                "translated": translated,
                "language": target_language,
                "engine": translation_engine
            }

            if entry not in st.session_state.history:

                st.session_state.history.append(entry)

                if len(st.session_state.history) > 10:
                    st.session_state.history.pop(0)

        except Exception as e:
            st.error(f"Translation Error: {e}")

    else:
        st.warning("Please enter some text.")



with output_col:

    if st.session_state.translated:

        st.text_area(
            "📄 Translation",
            value=st.session_state.translated,
            height=180,
            disabled=True
        )

        col_download, col_clear = st.columns(2)

        with col_download:
            st.download_button(
                label="📥 Download Translation",
                data=st.session_state.translated,
                file_name="translation.txt",
                mime="text/plain"
            )

        with col_clear:
            clear_btn = st.button("🗑 Clear Text")
        
        if clear_btn:
            st.session_state.translated = ""
            st.session_state.detected_language = ""
            st.session_state.text_area_key += 1
            st.rerun()

    else:

        st.text_area(
            "📄 Translation",
            value="Waiting for translation...",
            height=180,
            disabled=True
        )


st.markdown("""
---
<div style='text-align:center; color:gray;'>

👨‍💻 <b>Developed by Tushar Patel</b><br>

🌍 AI Language Translator v2.0<br><br>

© 2026 Tushar Patel | MIT License

</div>
""", unsafe_allow_html=True)