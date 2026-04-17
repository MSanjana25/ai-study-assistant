import streamlit as st
import sqlite3
import requests

# =========================
# DATABASE (SQLite)
# =========================
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

def create_usertable():
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT UNIQUE,
            password TEXT,
            api_key TEXT
        )
    """)
    conn.commit()

def add_userdata(username, password, api_key):
    try:
        c.execute(
            'INSERT INTO users(username, password, api_key) VALUES (?, ?, ?)',
            (username, password, api_key)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    c.execute(
        'SELECT * FROM users WHERE username=? AND password=?',
        (username, password)
    )
    return c.fetchone()

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "api_key" not in st.session_state:
    st.session_state.api_key = None

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# =========================
# AI FUNCTION
# =========================
def get_openrouter_response(model, prompt, **kwargs):
    try:
        model_map = {
            "ChatGPT": "openai/gpt-oss-20b:free",
            "Gemini": "google/gemma-3-27b-it:free",
            "LLaMA": "meta-llama/llama-3.3-70b-instruct:free",
            "DeepSeek": "deepseek/deepseek-r1-0528-qwen3-8b:free"
        }

        selected_model = model_map.get(model, "openai/gpt-oss-20b:free")

        headers = {
            "Authorization": f"Bearer {st.session_state.api_key}",
            "HTTP-Referer": "http://localhost",
            "X-Title": "AI Study Assistant",
            "Content-Type": "application/json"
        }

        system_prompt = (
            f"Task={kwargs.get('task')} | "
            f"Tone={kwargs.get('tone')} | "
            f"Mode={kwargs.get('mode')} | "
            f"Style={kwargs.get('style')} | "
            f"Persona={kwargs.get('persona')} | "
            f"Depth={kwargs.get('depth')} | "
            f"Format={kwargs.get('format_type')} | "
            f"Language={kwargs.get('language')} | "
            f"Memory={kwargs.get('memory')}"
        )

        data = {
            "model": selected_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(OPENROUTER_URL, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()
        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {str(e)}"

# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="AI Study Assistant", layout="wide")
create_usertable()

# =========================
# LOGIN / SIGNUP
# =========================
if not st.session_state.authenticated:
    st.title("🎓 AI Study Assistant")
    st.write("Generate explanations, summaries, and study help using AI.")

    menu = ["Login", "Signup"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Signup":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        new_api_key = st.text_input("OpenRouter API Key", type="password")

        st.markdown(
            "<a href='https://openrouter.ai/keys' target='_blank'>Get OpenRouter API Key</a>",
            unsafe_allow_html=True
        )

        if st.button("Signup"):
            if new_user and new_pass and new_api_key:
                success = add_userdata(new_user, new_pass, new_api_key)
                if success:
                    st.success("Account created successfully! Please login.")
                else:
                    st.warning("Username already exists. Try another username.")
            else:
                st.warning("Please fill all fields.")

    elif choice == "Login":
        st.subheader("Login to your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            result = login_user(username, password)
            if result:
                st.success(f"Welcome {username}")
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.api_key = result[2]
                st.rerun()
            else:
                st.error("Invalid username or password")

# =========================
# MAIN APP
# =========================
if st.session_state.authenticated:
    st.sidebar.markdown(f"Logged in as **{st.session_state.username}**")

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.api_key = None
        st.session_state.messages = []
        st.rerun()

    st.sidebar.title("Study Settings")

    model = st.sidebar.selectbox("Model", ["ChatGPT", "Gemini", "LLaMA", "DeepSeek"])
    task = st.sidebar.selectbox("Task", ["Explain", "Summarize", "Generate Questions", "Tutor"])
    mode = st.sidebar.selectbox("Mode", ["Stepwise", "Direct", "Analogy", "Comparative"])
    style = st.sidebar.selectbox("Style", ["Beginner", "Formal", "Conversational", "Exam-ready"])
    persona = st.sidebar.selectbox("Persona", ["Teacher", "Tutor", "Student"])
    depth = st.sidebar.selectbox("Depth", ["Short", "Medium", "Long"])
    format_type = st.sidebar.selectbox("Format", ["Text", "Bullet Points", "Markdown"])
    language = st.sidebar.selectbox("Language", ["English", "Hindi", "Telugu"])
    tone = st.sidebar.selectbox("Tone", ["Neutral", "Friendly", "Polite"])
    memory = st.sidebar.radio("Memory", ["Stateless", "Session-based"])

    st.title("🎓 AI Study Assistant")
    st.write("Ask any topic, concept, or question and get an AI-generated study response.")

    if st.session_state.messages:
        st.subheader("Conversation")
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**Assistant:** {msg['content']}")

    user_input = st.text_area(
        "Enter a topic or question:",
        placeholder="Example: Explain DBMS in simple words"
    )

    if st.button("Generate Response"):
        if user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})

            response = get_openrouter_response(
                model,
                user_input,
                task=task,
                mode=mode,
                style=style,
                persona=persona,
                depth=depth,
                format_type=format_type,
                language=language,
                tone=tone,
                memory=memory
            )

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            st.rerun()
        else:
            st.warning("Please enter a topic or question.")