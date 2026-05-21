# MindMosaic

**MindMosaic** is a web-based, AI-powered mental wellness platform. It provides a supportive chat assistant, crisis detection, and wellness resources, combining a Python Flask backend with a modern, responsive HTML/CSS/JavaScript frontend.

---

## 🌟 Key Features

- **AI Chat Assistant:**  
  Empathetic, multilingual (English & Roman Urdu) support for mental wellness, powered by OpenAI GPT models.
- **Crisis Detection:**  
  Detects crisis or stress keywords and provides immediate helpline resources.
- **Wellness Resources:**  
  Offers coping strategies, wellness tips, and supportive responses.
- **Session Management:**  
  Remembers chat history for ongoing support.
- **Modern UI:**  
  Clean, mobile-friendly interface with a warm, calming design.

---

## 🛠️ Tech Stack & Libraries

**Backend:**

- Python 3.x
- Flask
- Flask-CORS
- Requests
- python-dotenv
- OpenAI GPT (via OpenRouter API, e.g., `openai/gpt-4o-mini`)

**Frontend:**

- HTML5, CSS3, JavaScript (Vanilla)

---

## 🤖 AI Model

- Uses OpenAI GPT (e.g., GPT-4o-mini) via OpenRouter API for chat responses.
- System prompt ensures empathetic, non-clinical support.
- Crisis and stress detection for English and Roman Urdu.

---

## 🚀 Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/mindmosaic.git
   cd mindmosaic
   ```

2. **Backend Setup:**

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **API Key Setup:**
   - Create a `.env` file in the `backend/` directory.
   - Add your OpenRouter API key:
     ```
     OPENROUTER_API_KEY=your_api_key_here
     ```

4. **Run the Backend:**

   ```bash
   python app.py
   ```

5. **Frontend:**
   - Open `frontend/index.html` in your browser.

---

## 📁 Project Structure

```
mindmosaic/
│
├── backend/
│   ├── app.py
│   ├── ai_agent.py
│   ├── crisis.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── index.html
│   ├── chat.html
│   ├── wellness.html
│   ├── script.js
│   └── style.css
│
├── sessions.json
└── README.md
```

---

## ⚠️ Disclaimer

MindMosaic is **not** a replacement for professional mental health care. For urgent help, always contact a qualified professional or a crisis helpline.

---

## 📜 License

MIT License
