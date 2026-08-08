import streamlit as st
from openai import OpenAI
from datetime import datetime

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Mental Health Support Chatbot",
    page_icon="🧠",
    layout="centered"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 20px;
    }

    .disclaimer {
        background-color: #fff3cd;
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# OpenRouter API
# -----------------------------
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

except Exception:
    st.error("API key is not configured. Please configure OPENROUTER_API_KEY.")
    st.stop()

# -----------------------------
# System Prompt
# -----------------------------
SYSTEM_PROMPT = """
You are a compassionate mental wellness assistant.

You are not a therapist or doctor.

Your role is to:
- Listen with empathy.
- Provide emotional support.
- Suggest safe and general coping strategies.
- Encourage the user to talk with trusted people or qualified professionals.
- Encourage professional help when appropriate.

Never:
- Diagnose mental health conditions.
- Prescribe medication.
- Pretend to be a doctor or therapist.
- Give dangerous medical advice.

If the user indicates immediate danger, self-harm,
suicidal thoughts, or danger to others, encourage them
to contact local emergency services, a trusted person,
or a qualified mental health professional immediately.
"""

# -----------------------------
# AI Function
# -----------------------------
def ask_ai(message):

    try:

        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Sorry, something went wrong: {str(e)}"


# -----------------------------
# Title
# -----------------------------
st.markdown(
    '<div class="main-title">🧠 AI-Powered Mental Health Support Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">A compassionate AI assistant for emotional support</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Disclaimer
# -----------------------------
st.markdown("""
<div class="disclaimer">
⚠️ <b>Disclaimer:</b> This chatbot is not a doctor or therapist.
It provides general emotional support and should not replace
professional medical or mental health care.
<br><br>
If you are in immediate danger, please contact local emergency
services or a trusted person.
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Chat History
# -----------------------------
if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! 👋 How are you feeling today?"
        }
    ]

# -----------------------------
# Display Messages
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

# -----------------------------
# Clear Chat Button
# -----------------------------
if st.button("🗑️ Clear Chat"):

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! 👋 How are you feeling today?"
        }
    ]

    st.rerun()

# -----------------------------
# User Input
# -----------------------------
user_message = st.chat_input(
    "Type how you're feeling..."
)

if user_message:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    with st.chat_message("user"):
        st.write(user_message)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("AI is thinking..."):

            response = ask_ai(user_message)

        st.write(response)

    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")

st.caption(
    "🧠 AI-Powered Mental Health Support Chatbot | "
    "For educational and supportive purposes only."
)