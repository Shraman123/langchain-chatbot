# 🤖 LangChain Chatbot

A minimal **AI chatbot** built with [LangChain](https://www.langchain.com/), [LangGraph](https://github.com/langchain-ai/langgraph), and Python.  
It uses memory persistence and can run either locally or connected to cloud LLMs like **Google Gemini** or **OpenAI GPT models**.

---

## 🚀 Features

- ✅ Chatbot built with **LangGraph** for structured conversational flow  
- 💾 Uses **MemorySaver** for in-memory state tracking  
- 🔁 Supports multiple sessions / threads  
- ⚙️ Works with **Google Gemini** or **OpenAI** models  
- 🧩 Easy to extend for APIs, web apps, or FastAPI backends  

---

## 🗂️ Project Structure



langchain-chatbot/
├─ chatbot.py # Main chatbot logic
├─ requirements.txt # Python dependencies
├─ .gitignore # Ignore venv and cache
└─ README.md # Project documentation


---

## 🧰 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Shraman123/langchain-chatbot.git
cd langchain-chatbot
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install langchain langgraph langsmith
pip install "langchain[google-genai]"
Set Your API Key
For Google Gemini:
$env:GOOGLE_API_KEY = "your_api_key_here"

For OpenAI:
$env:OPENAI_API_KEY = "your_api_key_here"


(You can also persist keys using setx for future PowerShell sessions.)

💬 Run the Chatbot
python chatbot.py


Then start chatting:

You: Hello!
Assistant: Hi there! How can I help you today?


Type:

clear → reset memory for this session

exit → quit the program

🧩 Example Prompt Template

The system message sets the chatbot’s personality:

("system", "You are a helpful assistant. Answer concisely.")


You can modify this line to make it creative, funny, or domain-specific (e.g., “You are a startup advisor who loves giving bold ideas.”)

🌱 Future Ideas

Add FastAPI or Streamlit frontend

Store chat memory in SQLite or Postgres

Deploy as a web app using Render / Vercel / Hugging Face Spaces

Add LangSmith tracing for better debugging and analytics

👨‍💻 Author

Shraman Hazra

🎓 B.Tech in AI & ML

💡 Passionate about tech, AI, startups, and business

🌐 GitHub Profile

🧾 License

This project is open-source under the MIT License
.


---

## 🪄 Next Steps

1. Save this as `README.md` in your project folder.  
2. In PowerShell:
   ```powershell
   git add README.md
   git commit -m "Added professional README.md"
   git push


