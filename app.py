from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


model = genai.GenerativeModel("models/gemini-1.5-flash")


if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

def get_response(new_query):
    prompt_intro = """
You are a memory-retentive bot. You can remember previous interactions and use that information to provide better responses.

Instructions: 
1. Always refer to previous questions and answers in your responses.
2. If the user asks a new question, use the context of previous interactions to inform your answer.
3. Always respond in a friendly and helpful manner.
4. Just answer the question without repeating the question itself.
5. After answering the question. Do not ask if the user has any more questions. Just answer the question.

Below is the conversation so far between you and the user:
"""

    history_text = ""
    for i, (q, a) in enumerate(st.session_state.conversation_history):
        history_text += f"User: {q}\nAssistant: {a}\n"

    full_prompt = f"{prompt_intro}\n{history_text}\nUser: {new_query}\nAssistant:"

    try:  
        response = model.generate_content(full_prompt)
        parts = response.candidates[0].content.parts
        text = ' '.join(part.text for part in parts)

        st.session_state.conversation_history.append((new_query, text.strip()))
        return text.strip()

    except Exception as e:
        st.error(f"Error: {e}")
        return None



# Streamlit UI with Chat Interface
st.set_page_config(page_title="Memory Chatbot", layout="wide")
st.title("🤖 Memory Chatbot")

# Display previous messages in chat bubbles
for q, a in st.session_state.conversation_history:
    with st.chat_message("user"):
        st.markdown(q)
    with st.chat_message("assistant"):
        st.markdown(a)

# Chat input box at the bottom
if prompt := st.chat_input("Type your message here..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        response = get_response(prompt)

    if response:
        with st.chat_message("assistant"):
            st.markdown(response)