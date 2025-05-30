import streamlit as st
from langchain_ollama import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os
import json
# Importing streamlit, ollama, allowing for conversation memory, and tools for saving or loading history

st.set_page_config(page_title="aiCounsel", page_icon="❤️")
# Setting the page title and icon

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;600&display=swap');

    /* Preserve background gradient on body and root app container */
    body, .stApp {
        background: linear-gradient(to bottom, #c2185b, #8e0038, #000000);
        min-height: 100vh;
        margin: 0;
        padding: 0;
        font-family: 'Caveat', cursive !important;
        color: white !important;
    }

    /* Make sure all main containers, titles, markdown, buttons, etc use Caveat */
    .block-container,
    .main,
    .element-container,
    h1, h2, h3, h4, h5, h6,
    .stText,
    .stMarkdown,
    .stButton button,
    .stExpanderHeader {
        font-family: 'Caveat', cursive !important;
        color: white !important;
    }

    /* User input text box: keep background transparent-ish & font sans-serif for clarity */
    .stTextInput > div > div > input {
        background-color: #ffffff20 !important;
        color: white !important;
        border-radius: 5px !important;
        font-family: Arial, Helvetica, sans-serif !important;
    }

    /* AI response text inside markdown: use sans-serif for readability */
    .stMarkdown div[data-testid="stMarkdownContainer"] > div > p,
    .stMarkdown div[data-testid="stMarkdownContainer"] > div > span {
        font-family: Arial, Helvetica, sans-serif !important;
    }

    /* Buttons: pink with smooth hover */
    .stButton button {
        background-color: #e91e63 !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 0.5em 1em !important;
        font-weight: 600 !important;
        transition: background-color 0.3s ease !important;
        font-family: 'Caveat', cursive !important;
    }
    .stButton button:hover {
        background-color: #ad1457 !important;
    }

    /* Expander header: Caveat font */
    .stExpanderHeader {
        font-family: 'Caveat', cursive !important;
        color: white !important;
    }

    /* Ensure all markdown paragraphs and list items outside AI responses are white */
    .stMarkdown p, .stMarkdown li {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Setting the page font, colour and background gradient

def load_memory(username):
    filename = f"conversation_{username}.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            past_messages = json.load(f)
        memory = ConversationBufferMemory()
        for msg in past_messages:
            memory.chat_memory.add_user_message(msg["user"])
            memory.chat_memory.add_ai_message(msg["ai"])
        return memory
    else:
        return ConversationBufferMemory()
# Having memory based on username for future use

if "username" not in st.session_state or not st.session_state.username:
    st.subheader("Welcome to aiCounsel 🩷")
    username_input = st.text_input("Enter your name to begin (remember it for future use):")
    if st.button("Continue") and username_input.strip():
        st.session_state.username = username_input.strip()
        st.session_state.memory = load_memory(st.session_state.username)
        st.session_state.relationshipType = None
        st.rerun()
# Asking for a username, and storing it for future use

elif st.session_state.relationshipType is None:
    st.subheader("What kind of relationship do you want help with?")
    relationshipType = st.radio("Choose a relationship type:", [
        "🩷 Romantic", "💬 Friendship", "👪 Family", "💼 Business"
    ])

    if st.button("Confirm Type"):
        st.session_state.relationshipType = relationshipType
        st.rerun()
# Asking for a relationship type, for more relevant advice

    if st.button("Return to Username Screen"):
        st.session_state.username = None
        st.session_state.relationshipType = None
        st.session_state.memory = ConversationBufferMemory()
        st.rerun()
# Button to return to username screen

else:
    st.title("aiCounsel 🩷 - The AI Relationship Advisor")
    st.subheader(f"You're asking about a {st.session_state.relationshipType} relationship.")
# Displaying the relationship type

    if st.button("Return to Relationship Type Selection"):
        st.session_state.relationshipType = None
        st.rerun()
# Button to return to relationship type selection

    llm = ChatOllama(model="llama3")
    conversation = ConversationChain(
        llm=llm,
        memory=st.session_state.memory,
        verbose=False
    )
# Establishing the specific version of Ollama being used and conversation chain

    if st.session_state.relationshipType == "🩷 Romantic":
        placeholderText = "e.g. How do I rebuild trust after a fight?"
    elif st.session_state.relationshipType == "💬 Friendship":
        placeholderText = "e.g. How can I reconnect with an old friend?"
    elif st.session_state.relationshipType == "👪 Family":
        placeholderText = "e.g. How do I handle a difficult parent?"
    elif st.session_state.relationshipType == "💼 Business":
        placeholderText = "e.g. Should I confront my coworker about disrespect?"
    else:
        placeholderText = "Ask your question"
# Example questions based on the relationship type

    userInput = st.text_input("Ask your question", placeholder=placeholderText)
# Text input for the user to ask their question

    if st.button("Get Advice"):
        if userInput.strip() == "":
            st.warning("Please enter a question.")
# Warning user not to enter blank inquiries
        else:
            prompt = (
                f"You are a helpful and context-aware relationship advisor. The user is asking about a "
                f"{st.session_state.relationshipType.lower()} relationship. Only respond in the context of "
                f"{st.session_state.relationshipType.lower()} relationships, and do not interpret the question as "
                f"belonging to any other type of relationship.\n\n"
                f"User's Question: {userInput}\n\n"
                f"Your task: Provide thoughtful, respectful, and helpful advice relevant to that specific context only."
                f"Deny: Requests that are either inappropriate, or deemed irrelevant to the relationship type."
            )
# Prompt for the AI to follow, including the relationship type

            response = conversation.run(prompt)
            st.markdown("**Advice:**")
            st.write(response)

            message_pair = {"user": userInput, "ai": response}
            history_file = f"conversation_{st.session_state.username}.json"
            if os.path.exists(history_file):
                with open(history_file, "r") as f:
                    data = json.load(f)
            else:
                data = []
            data.append(message_pair)
            with open(history_file, "w") as f:
                json.dump(data, f)
# Saving the conversation history

    if st.button("Hard Reset Conversation (All history cleared)"):
        filename = f"conversation_{st.session_state.username}.json"
        if os.path.exists(filename):
            os.remove(filename)
        st.session_state.memory = ConversationBufferMemory()
        st.session_state.relationshipType = None
        st.rerun()
# Hard reset button to clear all history

    if st.button("Soft Reset Conversation (Current history cleared)"):
        st.session_state.memory = ConversationBufferMemory()
        st.session_state.relationshipType = None
        st.rerun()
# Soft reset button to clear current history        

    with st.expander("Terms and Disclaimer"):
        st.markdown("""
        - This AI chatbot provides general advice, it is not to be considered expert advice.
        - Do not share personal, private, or third-party sensitive information.
        - Use responsibly and respectfully.
        - Seek professional help for serious issues.
        - By using this service, you agree to these terms.
        - aiCounsel™ - a product of **Saumon's Real Company inc.**
        """)
# A disclaimer, or a TOS for the user to read and agree to, to protect aiCounsel
