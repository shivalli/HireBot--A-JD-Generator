import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-pro")

# Streamlit UI Configuration
st.set_page_config(page_title="HireBot - Job Description Generator", layout="wide")

# Apply custom CSS for Dark Mode & Input Box at Bottom
st.markdown(
    """
    <style>
        body {
            background-color: black;
            color: white;
        }
        .stApp {
            background-color: black;
            color: white;
        }
        .stTextInput > div > div > input {
            background-color: #1e1e1e !important;
            color: white !important;
            border: 1px solid white !important;
        }
        .stTextInput > label {
            color: white !important;
        }
        .stMarkdown {
            color: white !important;
        }
        .stButton > button {
            background-color: white !important;
            color: black !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("✨ Enhance Job Descriptions with HireBot ✨")

# Initialize session state for conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = [
        {"role": "system", "content": "You are an AI-powered Job Description Generator Chatbot. "
         "Your task is to assist recruiters in creating well-structured, engaging, and professional job descriptions. "
         "Engage in a conversation to gather necessary details before generating the final JD. "
         "Ask one relevant question at a time based on user responses. "
         "Once enough details are collected, summarize and generate the complete job description."},
        {"role": "assistant", "content": "Hello! Let's create a great job description. What is the job title?"}
    ]

# Display chat history
for message in st.session_state.conversation_history:
    if message["role"] == "assistant":
        st.markdown(f"**🤖 HireBot:** {message['content']}")
    elif message["role"] == "user":
        st.markdown(f"**🧑 You:** {message['content']}")

# Function to generate AI response
def generate_response(conversation_history, user_input):
    if user_input.lower().strip() == "bye":
        return "👋 Goodbye! If you need any job descriptions in the future, feel free to ask. 😊"

    # Construct prompt with conversation history
    prompt = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in conversation_history])
    prompt += f"\nUser: {user_input}\nHireBot:"

    response = model.generate_content(prompt)
    return response.text.strip()

# Ensure user input is in session state before the text input widget
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# User Input at the Bottom with Submit Button
user_input = st.text_input("💬 Type your response and press Submit...", key="user_input")
submit_button = st.button("Submit")

if submit_button and user_input.strip():
    # Store user input in session state
    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    # Generate response
    response = generate_response(st.session_state.conversation_history, user_input)

    # Store AI response in session state
    st.session_state.conversation_history.append({"role": "assistant", "content": response})

    # Clear input safely
    st.session_state.pop("user_input", None)

    # Refresh UI
    st.rerun()
