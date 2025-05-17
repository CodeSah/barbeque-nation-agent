# Barbeque Nation Agent

This project is an AI-driven assistant for Barbeque Nation outlets (Delhi & Bangalore), capable of handling new bookings, modifications/cancellations, and FAQ-based queries through both voice and chatbot interfaces.

## 📁 Project Structure

```
barbeque-nation-agent/
├── backend/
│   ├── app.py                  # Flask API to handle chatbot interaction and logging
│   ├── log_to_sheet.py         # Google Sheets integration for conversation logging
│   ├── knowledge_base.json     # Structured responses for different intents
│   ├── requirements.txt        # Python dependencies
│   └── creds.json              # Google Service Account key (not in repo)
├── frontend/
│   ├── index.html              # Simple chatbot UI
│   └── script.js               # JS to interact with backend endpoints
├── retell-config/
│   └── state_machine.json      # Retell AI State Machine JSON config
└── docs/
    └── README.md               # Documentation (this file)
```

## ⚙️ Setup Instructions

### 1. Python Environment Setup

```bash
cd backend
pip install -r requirements.txt
```

### 2. Google Sheets Setup

* Place your `creds.json` file inside `backend/`
* Share your Google Sheet with the email ID in the creds file
* Ensure the sheet is named `Sheet1` (or the active sheet)

### 3. Run Backend

```bash
cd backend
python app.py
```

Backend will run at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 4. Frontend Chatbot (Local)

Open `frontend/index.html` in any modern browser.

## 🧠 Knowledge Base (knowledge\_base.json)

This JSON contains hard-coded responses mapped by property (e.g., "Delhi") and intent (e.g., "booking", "faq").
The backend searches this file to generate responses to user questions.

## 🧾 Logging to Google Sheets

The `log_to_sheet.py` script uses Google Sheets API to log each interaction post-chat/call. Triggered via `/log` endpoint.

## 🔄 State Machine (retell-config/state\_machine.json)

Defines Retell AI's voice/chat agent flow, using prompts and transitions configured in Jinja2 templating style.

* Collects variables like name, phone, guests, date, time
* Handles new bookings, cancellations, and FAQs

## 🚀 Endpoints

| Endpoint | Method | Purpose                          |
| -------- | ------ | -------------------------------- |
| `/`      | GET    | Welcome message                  |
| `/query` | POST   | Handle chatbot question          |
| `/log`   | POST   | Log interaction to Google Sheets |

## 🔗 References

* Retell AI Multi-Prompt Docs: [https://docs.retellai.com/build/write-multi-prompt](https://docs.retellai.com/build/write-multi-prompt)
* Jinja Templating: [https://jinja.palletsprojects.com/en/stable/](https://jinja.palletsprojects.com/en/stable/)
* Google Sheets API Setup: [https://developers.google.com/sheets/api/quickstart/python](https://developers.google.com/sheets/api/quickstart/python)

---

All components are modular and can be expanded easily to handle more locations, dynamic integrations, or advanced AI logic.