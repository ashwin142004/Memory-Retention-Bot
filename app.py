from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


model = genai.GenerativeModel("models/gemini-1.5-flash")


if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

def get_travel_response(new_query):
    prompt_intro = """
You are a professional travel planner assistant.

Instructions:
1. Understand the user's travel-related queries.
2. Provide short and clear travel suggestions (e.g., destinations, best time to visit, itineraries, packing tips, budget tips, etc.).
3. Be friendly and helpful in tone.
4. If the question is unrelated to travel, respond with: "I'm a travel assistant and can only help with travel-related queries."

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

        # Save to history
        st.session_state.conversation_history.append((new_query, text.strip()))
        return text.strip()

    except Exception as e:
        st.error(f"Error: {e}")
        return None


st.set_page_config(page_title="Travel Planner Bot with Memory", layout="wide")
st.markdown("<h1 style='text-align: center;'>🧳 Travel Planner Assistant (With Memory)</h1>", unsafe_allow_html=True)

user_input = st.text_input("Ask your travel-related question:", key="travel_input")
submit = st.button("Send")

if submit and user_input:
    with st.spinner("Thinking..."):
        response = get_travel_response(user_input)
        if response:
            st.markdown("### ✈️ Travel Suggestions")
            st.write(response)


if st.checkbox("Show full conversation history"):
    st.markdown("### 🗂️ Chat History")
    for i, (q, a) in enumerate(st.session_state.conversation_history):
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Assistant:** {a}")
