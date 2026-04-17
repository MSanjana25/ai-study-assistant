# 🎓 AI Study Assistant

AI Study Assistant is a **Streamlit-based Python application** that helps users generate **explanations, summaries, and study-oriented responses** for any topic or question using AI models via OpenRouter.

It includes **user authentication (SQLite)**, **chat history**, and **customizable study settings** such as task, tone, style, and depth.

---

## 🚀 Features

- 🔐 User Authentication (Signup/Login using SQLite)
- 🔑 API Key storage for OpenRouter access
- 🤖 Multiple AI Model Support:
  - ChatGPT
  - Gemini
  - LLaMA
  - DeepSeek
- ⚙️ Customizable Study Settings:
  - Task (Explain, Summarize, Generate Questions, Tutor)
  - Mode (Stepwise, Direct, Analogy, Comparative)
  - Style (Beginner, Formal, Conversational)
  - Persona (Teacher, Tutor, Student)
  - Depth (Short, Medium, Long)
  - Format (Text, Bullet Points, Markdown)
  - Language (English, Hindi, Telugu)
  - Tone (Neutral, Friendly, Polite)
  - Memory (Stateless / Session-based)
- 💬 Session-based chat history
- 🎓 Study-focused AI responses

---

## 📂 Project Structure

---

## 📂 Project Structure

```
📦 project-folder
 ┣ 📜 app.py          # Main Streamlit app
 ┣ 📜 users.db        # SQLite database (auto-created)
 ┣ 📜 README.md       # Documentation
 ┗ 📜 requirements.txt # Python dependencies
```

---

## 🛠️ Installation & Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-username/ai-study-assistant.git
   cd ai-study-assistant
   ```

2. **Create Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Mac/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the App**
   ```bash
   streamlit run app.py
   ```

---

## 📦 requirements.txt

```txt
streamlit
sqlite3   # (comes with Python, no need to install)
requests
```

---

## 🔑 API Key Setup

1. Sign up at [OpenRouter](https://openrouter.ai/).  
2. Generate your API key from [https://openrouter.ai/keys](https://openrouter.ai/keys).  
3. Use the key while signing up in the app.  

---

## 💡 Usage

- **Signup/Login** using the sidebar.  
- **Choose model & parameters** (task, tone, style, etc.).  
- **Enter prompt** and hit 🚀 Submit.  
- Responses will appear in a chat-like interface.  

---

## 🎨 UI Preview

- Sidebar for login, logout, and parameter selection.  
- Chat area with conversation history.  
- Smooth authentication flow.  

---




