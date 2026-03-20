import sys
import os

# ================= PROJECT ROOT =================
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


# ================= LOAD .env =================
from dotenv import load_dotenv

ENV_PATH = os.path.join(PROJECT_ROOT, "config", ".env")
load_dotenv(ENV_PATH)


# ================= IMPORTS =================
import streamlit as st
import pandas as pd
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import base64
import tempfile
import io
from groq import Groq

from app.ai.text_to_sql import generate_sql
from app.db.run_query import execute_sql


# ================= API KEY =================
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)


# ================= PAGE CONFIG =================
st.set_page_config(page_title="VoiceQuery AI", layout="wide")

st.title("VoiceQuery AI — Smart Analytics Assistant")


# ================= LOAD DATA =================
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "retail_data.csv")
df = pd.read_csv(DATA_PATH)

query_area = st.container()
output_area = st.container()


# ============================================================
# 🔊 TEXT TO SPEECH
# ============================================================
def speak(text):
    tts = gTTS(text)

    buf = io.BytesIO()
    tts.write_to_fp(buf)

    b64 = base64.b64encode(buf.getvalue()).decode()

    st.markdown(f"""
    <audio autoplay>
      <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """, unsafe_allow_html=True)


# ============================================================
# 🚀 PROCESS QUERY
# ============================================================
def process_query(query):

    with query_area:
        st.info(f"**You Said:** {query}")

    # ---- AI → SQL ----
    sql_query = generate_sql(query)

    # ---- Execute SQL ----
    results = execute_sql(sql_query)

    with output_area:

        st.markdown("### Answer")
        st.markdown("#### Generated SQL")
        st.code(sql_query, language="sql")

        if isinstance(results, str):
            st.error(results)
            answer = "Error executing query."
        else:
            df_res = pd.DataFrame(results)
            st.dataframe(df_res)

            top_items = ", ".join(df_res.iloc[:5, 0].astype(str))
            answer = f"Here’s what I found: {top_items}"

        st.success(answer)

    speak(answer)


# ============================================================
# 🧾 INPUT BAR — LINEAR LAYOUT
# ============================================================

col_text, col_voice = st.columns([8, 2])


# ---------- LEFT: TEXT INPUT ----------
with col_text:
    manual_query = st.chat_input("Ask anything about your data...")


# ---------- RIGHT: VOICE BUTTON ----------
with col_voice:
    audio = mic_recorder(
        start_prompt="🎤 Ask Your Question",
        stop_prompt="⏹️ Stop",
        just_once=True,
        use_container_width=True,
        key="voice"
    )


# ============================================================
# ⌨️ MANUAL INPUT PROCESS (ENTER KEY)
# ============================================================

if manual_query:
    process_query(manual_query)


# ============================================================
# 🎤 VOICE INPUT PROCESS
# ============================================================

if audio:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
        f.write(audio["bytes"])
        audio_path = f.name

    try:
        with open(audio_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=file,
                model="whisper-large-v3"
            )

        voice_query = transcription.text

        # Show spoken text
        st.info(f"**You Said:** {voice_query}")

        process_query(voice_query)

    except Exception as e:
        st.error(f"Speech recognition failed: {e}")