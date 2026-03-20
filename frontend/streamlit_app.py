import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from dotenv import load_dotenv

ENV_PATH = os.path.join(PROJECT_ROOT, "config", ".env")
load_dotenv(ENV_PATH)

import streamlit as st
import pandas as pd
from streamlit_mic_recorder import mic_recorder
import uuid
from gtts import gTTS
import base64
import tempfile
import io
from groq import Groq

from app.ai.text_to_sql import generate_sql
from app.db.run_query import execute_sql

audio_placeholder = st.empty()

api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.set_page_config(page_title="VoiceQuery AI", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
* {
    font-family: 'Poppins', sans-serif !important;
}
button {
  font-family: 'Poppins', sans-serif !important;
  height: 56px;
  width: 100%;
  border-radius: 10px;
  font-size: 16px;
}
.bottom-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    padding: 10px 20px;
    border-top: 1px solid #ddd;
    z-index: 9999;
}
.main-content {
    padding-bottom: 90px;
}
div.stButton > button {
    height: 56px;
    width: 100%;
    border-radius: 10px;
    font-size: 16px;
}
.sidebar-field {
    font-size: 12px;    
    font-weight: 500;         
    white-space: nowrap;      
    overflow: hidden;
    text-overflow: ellipsis;  
    margin-bottom: 10px;      
}
[data-testid="column"]:last-child button {
    background: linear-gradient(135deg, #ff4b4b, #ff0000) !important;
    color: white !important;
    border-radius: 14px !important;
    border: none !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    height: 52px !important;
    width: 100% !important;
    box-shadow: 0 4px 14px rgba(255, 75, 75, 0.5);
    transition: all 0.2s ease-in-out;
}
</style>
""", unsafe_allow_html=True)

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "retail_data.csv")

df = pd.read_csv(DATA_PATH)

st.sidebar.title("VoiceQuery AI")
st.sidebar.header("📊 Dataset Info")

st.sidebar.subheader("Available Fields")

col1, col2 = st.sidebar.columns(2)

col1, col2 = st.sidebar.columns(2)

for i, col in enumerate(df.columns):

    display_name = col.replace("_", " ")
    field_html = f"""
    <div class="sidebar-field" title="{col}">
        <b>{display_name}</b>
    </div>
    """

    if i % 2 == 0:
        col1.markdown(field_html, unsafe_allow_html=True)
    else:
        col2.markdown(field_html, unsafe_allow_html=True)

st.title("VoiceQuery AI — Smart Analytics Assistant")

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "retail_data.csv")
df = pd.read_csv(DATA_PATH)

query_area = st.container()
output_area = st.container()

# Text to Speech
# def speak(text):
#     tts = gTTS(text)

#     buf = io.BytesIO()
#     tts.write_to_fp(buf)

#     b64 = base64.b64encode(buf.getvalue()).decode()

#     st.markdown(f"""
#     <audio autoplay>
#       <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
#     </audio>
#     """, unsafe_allow_html=True)
def speak(text):
    tts = gTTS(text)

    buf = io.BytesIO()
    tts.write_to_fp(buf)

    b64 = base64.b64encode(buf.getvalue()).decode()
    audio_id = f"audio-{uuid.uuid4()}"

    audio_placeholder.markdown(f"""
    <audio id="{audio_id}" autoplay style="position:fixed; left:-9999px;">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>

    <script>
    const audio = document.getElementById("{audio_id}");
    if (audio) {{
        audio.pause();
        audio.currentTime = 0;
        audio.play().catch(e => console.log(e));
    }}
    </script>
    """, unsafe_allow_html=True)

# Process Query
def process_query(query):

    with query_area:
        st.info(f"**You Said:** {query.title()}")

    # AI to SQL
    sql_query = generate_sql(query)

    # Execute SQL
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


# Input and Btn
st.markdown('<div class="bottom-bar">', unsafe_allow_html=True)
col_text, col_voice = st.columns([8, 2])


# Left: Text Input
with col_text:
    manual_query = st.chat_input("Ask anything about your data...")


# Right: Btn
with col_voice:
    audio = mic_recorder(
        start_prompt="Ask Your Question",
        stop_prompt="Stop",
        just_once=True,
        use_container_width=True,
        key="voice"
    )
st.markdown('</div>', unsafe_allow_html=True)

# Manual Input process
if manual_query:
    process_query(manual_query)


# Voice Input Process
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
        # st.info(f"**You Said:** {voice_query}")

        process_query(voice_query)

    except Exception as e:
        st.error(f"Speech recognition failed: {e}")