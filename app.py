# ============================================
# INSTALL REQUIRED LIBRARIES
# ============================================

!pip install -q --upgrade pip
!pip install -q openai-whisper
!pip install -q ffmpeg-python
!pip install -q streamlit
!pip install -q pyngrok
!pip install -q groq
!pip install -q nest_asyncio
!pip install -q streamlit-mic-recorder
!pip install -q gtts

!apt install ffmpeg -y

# ============================================
# IMPORTS
# ============================================

import os
import threading
import nest_asyncio

from google.colab import userdata
from pyngrok import ngrok

# ============================================
# LOAD SECRETS FROM COLAB
# ============================================

GROQ_API_KEY = userdata.get("Groq")
NGROK_AUTH_TOKEN = userdata.get("Ngrok")

# ============================================
# SET NGROK AUTH TOKEN
# ============================================

ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# ============================================
# STREAMLIT APP CODE
# ============================================

app_code = f"""

# ============================================
# IMPORTS
# ============================================

import os
import re
import json
import whisper
import streamlit as st

from groq import Groq
from gtts import gTTS
from datetime import datetime
from streamlit_mic_recorder import mic_recorder

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Fluent AI",
    page_icon="🎤",
    layout="wide"
)


# ============================================
# GROQ CLIENT
# ============================================

client = Groq(
    api_key="{GROQ_API_KEY}"
)

# ============================================
# LOAD WHISPER MODEL
# ============================================

@st.cache_resource
def load_whisper():
    return whisper.load_model("base")

whisper_model = load_whisper()

# ============================================
# MODE PROMPTS
# ============================================

MODE_PROMPTS = {{

    "Casual Conversation": \"\"\"
You are a friendly English conversation coach.

Focus on:
- natural speaking
- casual fluency
- confidence building

Correct mistakes gently.
Keep conversations relaxed and natural.
\"\"\",

    "IELTS Speaking": \"\"\"
You are a strict IELTS speaking examiner.

Focus on:
- grammar accuracy
- advanced vocabulary
- fluency
- coherence
- band-score style corrections

Point out every mistake clearly.
Suggest higher-level vocabulary and better sentence structures.
\"\"\",

    "Job Interview": \"\"\"
You are a professional English interview coach.

Focus on:
- professional communication
- confidence
- formal vocabulary
- concise answers

Improve interview-style responses.
\"\"\",

    "Travel English": \"\"\"
You are a travel English speaking coach.

Focus on:
- practical communication
- simple clear English
- travel vocabulary
- confidence in public speaking situations

Keep responses easy and useful.
\"\"\"
}}

# ============================================
# SYSTEM PROMPT
# ============================================

SYSTEM_PROMPT = \"\"\" You are FluentAI.
You are a strict English grammar and fluency correction AI.
Your ONLY purpose:
- Correct grammar
- Improve fluency
- Suggest better vocabulary
- Improve sentence structure
- Help users speak natural English
STRICT RULES:
- If the user asks anything NOT related to English grammar, writing, speaking, or fluency, politely refuse.
- Do NOT answer general knowledge questions, coding, math, opinions, or personal advice.
- Do NOT continue the conversation outside English learning.
REFUSAL STYLE:
If request is unrelated, reply: "I'm designed only to help with English grammar and fluency. Please send a sentence you'd like me to improve."
TONE:
- Polite
- Short
- No extra explanation Speak conversationally and clearly. \"\"\"

# ============================================
# SCORING PROMPT
# ============================================

SCORING_PROMPT = \"\"\"You are an English fluency evaluator.

Score the user's sentence from 1-10 for:

1. Grammar
2. Fluency
3. Vocabulary
4. Confidence

Return ONLY this format:

Grammar: X/10
Fluency: X/10
Vocabulary: X/10
Confidence: X/10

Keep it short.\"\"\"

# ============================================
# HEADER
# ============================================

st.title("🎤 Fluent AI")
st.caption("Voice-First AI Language Learning Platform")

# ============================================
# SESSION STATE
# ============================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:

    st.header("Fluent AI")

    # Clear Chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # Mode Selection
    st.markdown("### Learning Mode")

    mode = st.selectbox(
        "Choose your training mode",
        [
            "Casual Conversation",
            "IELTS Speaking",
            "Job Interview",
            "Travel English"
        ]
    )

    st.caption("AI adapts response style based on your mode")

    st.divider()

    # Export Chat
    st.markdown("### 📤 Export Data")

    chat_export = json.dumps(
        st.session_state.messages,
        indent=4
    )

    st.download_button(
        label="⬇️ Download Chat History",
        data=chat_export,
        file_name="chat_history.json",
        mime="application/json"
    )

    st.divider()

    # Save Chat
    st.markdown("### 💾 Save Session")

    if st.button("Save Chat Locally"):

        filename = f"chat_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.json"

        with open(filename, "w") as f:
            json.dump(st.session_state.messages, f, indent=4)

        st.success(f"Saved → {{filename}}")

    st.divider()

    # System Status Panel (NEW)
    st.markdown("### System Status")

    st.success("AI Engine Active")
    st.info("Voice Model Loaded")
    st.info("Groq LLM Connected")

    st.divider()

    # Tips Panel
    st.markdown("### Pro Tips")

    st.write("• Use IELTS mode for strict correction")
    st.write("• Speak clearly for better transcription")
    st.write("• Keep sentences short for better feedback")
    st.write("• Try voice + text combo for faster learning")

    st.divider()

    st.caption("Fluent AI • Learning Companion")

# ============================================
# DISPLAY CHAT
# ============================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================
# VOICE INPUT
# ============================================

st.subheader("🎙️ Voice Input")

audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹️ Stop Recording",
    key="recorder"
)

transcribed_text = None

if audio:
    with open("input.wav", "wb") as f:
        f.write(audio["bytes"])

    with st.spinner("Transcribing..."):
        result = whisper_model.transcribe("input.wav")
        transcribed_text = result["text"]

    st.success("Voice Transcribed")

# ============================================
# TEXT INPUT
# ============================================

text_prompt = st.chat_input("Type your message...")

prompt = transcribed_text or text_prompt

# ============================================
# FIXED GATE FUNCTION
# ============================================

def is_english_task(text):
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {{
                    "role": "system",
                    "content": "Return ONLY YES or NO. Is this sentence related to English grammar, speaking, writing, or fluency practice?"
                }},
                {{
                    "role": "user",
                    "content": text
                }}
            ],
            temperature=0
        )

        return "YES" in res.choices[0].message.content.upper()

    except Exception as e:
        st.error(f"Gate error: {{e}}")
        return True

# ============================================
# CHAT PROCESS
# ============================================

if prompt:

    st.session_state.messages.append({{
        "role": "user",
        "content": prompt
    }})

    with st.chat_message("user"):
        st.markdown(prompt)

    # HARD BLOCK
    if not is_english_task(prompt):
        with st.chat_message("assistant"):
            st.warning("I'm designed only for English grammar and fluency practice. Please send an English sentence.")
        st.stop()

    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        limited_messages = st.session_state.messages[-10:]

        messages = [
            {{
                "role": "system",
                "content": SYSTEM_PROMPT + f" Current mode: {{mode}}"
            }}
        ] + limited_messages

        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            stream=True
        )

        full_response = ""

        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                full_response += content
                response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)

        st.session_state.messages.append({{
            "role": "assistant",
            "content": full_response
        }})

"""
# ============================================
# WRITE STREAMLIT FILE
# ============================================

with open("app.py", "w") as f:
    f.write(app_code)

nest_asyncio.apply()

def run_streamlit():
    os.system("streamlit run app.py --server.port 8501")

threading.Thread(target=run_streamlit).start()

public_url = ngrok.connect(8501)

print(public_url)
