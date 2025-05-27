## These prompts are simplified as the responses were achieved after long back and forths, but the general prompt gets the idea across for how I used ai (chatGPT)

# Prompts

1. Give me code to add to my streamlit app to give me a pink-black gradient background, white text and a warm, cursive like but readable font for my headers.

# Ai Responses

1. "st.markdown(
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
)"
