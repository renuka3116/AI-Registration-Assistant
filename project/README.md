# AI Registration Assistant

**NLP-Based Conversational Chatbot for Internship Registration**

An AI-powered conversational chatbot that helps students complete an internship registration process using Natural Language Processing and Machine Learning — built entirely with local, free, open-source tools. No paid APIs, no OpenAI, no Gemini, no external AI services.

---

## Overview

The AI Registration Assistant is a full-stack web application that demonstrates practical use of:

- Artificial Intelligence
- Natural Language Processing (NLP)
- Machine Learning (ML)
- Conversational AI
- Entity Extraction
- Web Development
- REST APIs

The chatbot understands natural-language queries, recognizes user intent, extracts and validates student information, maintains conversation state, guides the student through registration, shows a summary, asks for confirmation, and stores confirmed registrations.

---

## Problem Statement

Traditional internship registration requires students to fill out static forms with no guidance. This project replaces that experience with an intelligent conversational assistant that interacts in natural language, validates input dynamically, and guides the student step by step.

---

## Objectives

1. Build a conversational chatbot that understands natural language.
2. Classify user intent using TF-IDF + Logistic Regression.
3. Extract entities (name, email, field, experience) using regex.
4. Validate user input before proceeding.
5. Maintain dialog state across a multi-turn conversation.
6. Store confirmed registrations in a JSON file.
7. Provide a clean, responsive web interface.

---

## Features

1. **NLP Processing** — tokenization, stopword removal, lemmatization via NLTK
2. **Intent Recognition** — TF-IDF + Logistic Regression classification
3. **Entity Extraction** — regex-based extraction of name, email, field, experience
4. **Email Validation** — format validation before proceeding
5. **Conversational Registration** — multi-turn dialog management
6. **JSON Data Storage** — local file persistence, no external database
7. **Unknown Intent Handling** — confidence threshold with graceful fallback
8. **Responsive Web Interface** — works on desktop, tablet, and mobile

---

## Architecture

```
User types a message
        |
        v
React Frontend (Vite)
        |  POST /api/chat
        v
Flask Backend (Python)
        |
        +--> NLP Preprocessing (NLTK)
        |         lowercase -> remove special chars -> tokenize
        |         -> remove stopwords -> lemmatize
        |
        +--> TF-IDF Vectorizer
        |
        +--> Logistic Regression -> intent + confidence
        |
        +--> Entity Extractor (regex) -> name, email, field, experience
        |
        +--> Dialog Manager (state machine)
        |         IDLE -> COLLECTING_NAME -> COLLECTING_EMAIL
        |         -> COLLECTING_FIELD -> COLLECTING_EXPERIENCE
        |         -> CONFIRMATION -> COMPLETED
        |
        +--> Registration Manager -> JSON file storage
        |
        v
JSON response returned to frontend
```

---

## Technologies

| Layer      | Technology                                      |
|------------|-------------------------------------------------|
| Backend    | Python 3, Flask, Flask-CORS                     |
| NLP        | NLTK (tokenization, stopwords, lemmatization)   |
| ML         | Scikit-learn (TF-IDF, Logistic Regression)      |
| Entities   | Regular Expressions (regex)                    |
| Storage    | JSON files                                      |
| Frontend   | React, Vite, TypeScript, Tailwind CSS          |
| Icons      | Lucide React                                    |

---

## Project Structure

```
AI-Registration-Assistant/
│
├── backend/
│   ├── app.py                      # Flask application + REST API
│   ├── requirements.txt            # Python dependencies
│   │
│   ├── models/
│   │   └── intent_classifier.py    # TF-IDF + Logistic Regression
│   │
│   ├── nlp/
│   │   └── preprocessing.py        # NLTK preprocessing pipeline
│   │
│   ├── entities/
│   │   └── entity_extractor.py     # Regex entity extraction + validation
│   │
│   ├── conversation/
│   │   └── dialog_manager.py       # Conversation state machine
│   │
│   ├── registration/
│   │   └── registration_manager.py # JSON storage logic
│   │
│   ├── data/
│   │   ├── intents.json            # Training dataset (10 intents)
│   │   └── registrations.json     # Stored registrations
│   │
│   └── tests/
│       ├── test_preprocessing.py
│       ├── test_classifier.py
│       └── test_entity_extractor.py
│
├── src/                            # React frontend
│   ├── App.tsx                     # Main app component
│   ├── main.tsx                    # Entry point
│   ├── index.css                   # Tailwind CSS
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   ├── ChatWindow.tsx
│   │   ├── MessageBubble.tsx
│   │   ├── ChatInput.tsx
│   │   ├── TypingIndicator.tsx
│   │   ├── RegistrationSummary.tsx
│   │   ├── AboutView.tsx
│   │   └── FeaturesView.tsx
│   └── services/
│       └── api.ts                  # Backend API client
│
├── README.md
└── package.json
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- npm

### 1. Backend Setup

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

NLTK resources (punkt, stopwords, wordnet) are downloaded automatically on first run.

### 2. Frontend Setup

From the project root:

```bash
npm install
```

---

## Running the Application

You need **two terminals** — one for the backend, one for the frontend.

### Terminal 1: Backend

```bash
cd backend
source venv/bin/activate      # (or venv\Scripts\activate on Windows)
python app.py
```

The Flask backend runs on: http://localhost:5000

### Terminal 2: Frontend

From the project root:

```bash
npm run dev
```

The React frontend runs on: http://localhost:5173

Open http://localhost:5173 in your browser to use the application.

---

## API Documentation

### GET /api/health
Health check.

**Response:**
```json
{ "status": "running" }
```

### POST /api/chat
Process a user message.

**Request:**
```json
{ "message": "I want to register" }
```

**Response:**
```json
{
  "response": "Sure! I'll help you with the registration. What is your full name?",
  "intent": "register",
  "confidence": 0.89,
  "entities": {},
  "registration_state": "collecting_name"
}
```

### POST /api/register
Save a confirmed registration directly.

**Request:**
```json
{
  "name": "Renuka Srivastava",
  "email": "renuka@gmail.com",
  "field": "Information Technology",
  "experience": "Beginner"
}
```

### GET /api/registrations
Retrieve all stored registrations.

**Response:**
```json
{
  "registrations": [
    {
      "id": 1,
      "name": "Renuka Srivastava",
      "email": "renuka@gmail.com",
      "field": "Information Technology",
      "experience": "Beginner",
      "registered_at": "2026-08-26T10:00:00Z"
    }
  ]
}
```

### POST /api/reset
Reset the conversation state.

---

## Example Conversation

```
Assistant: Hello! 👋 Welcome to the AI Registration Assistant.
           Would you like to register for the internship?

User:      I want to register

Assistant: Sure! I'll help you with the registration. What is your full name?

User:      My name is Renuka Srivastava

Assistant: Nice to meet you, Renuka Srivastava! What is your email address?

User:      renuka@gmail.com

Assistant: Great! What is your field of study? (e.g. Information Technology, ...)

User:      Information Technology

Assistant: Excellent! What is your programming experience level? (Beginner, ...)

User:      Beginner

Assistant: Here is your registration summary:
             Name: Renuka Srivastava
             Email: renuka@gmail.com
             Field: Information Technology
             Experience: Beginner
           Would you like to confirm your registration? (yes / no)

User:      Yes

Assistant: 🎉 Registration completed successfully!
```

---

## Testing

Run the Python unit tests from the `backend` directory:

```bash
cd backend
source venv/bin/activate
pip install pytest
pytest tests/ -v
```

Test coverage:
- Preprocessing (lowercasing, special char removal, stopwords, lemmatization)
- Intent classification (greeting, register, requirements, unknown)
- Entity extraction (name, email, field, experience, validation)

---

## How the Frontend Communicates with the Backend

The React frontend uses the `fetch` API to send HTTP requests to the Flask backend:

1. The user types a message in the chat input.
2. `src/services/api.ts` sends a `POST /api/chat` request with the message.
3. The Flask backend processes the message (NLP + ML + dialog management).
4. The backend returns a JSON response with the chatbot reply, intent, confidence, and registration state.
5. The frontend renders the assistant's response as a chat bubble.
6. If the response includes registration data, a summary card is displayed inline.

CORS is enabled on the backend via `flask-cors` so the browser can call the API directly.

---

## How NLP and Machine Learning Work

### NLP Preprocessing Pipeline
1. **Lowercase** the text.
2. **Remove special characters** (keep letters and spaces).
3. **Tokenize** into individual words using NLTK's `word_tokenize`.
4. **Remove stopwords** (common words like "the", "is", "at") — except intent-bearing ones like "not", "yes", "what".
5. **Lemmatize** tokens to their base form (e.g., "running" → "run", "cats" → "cat") using NLTK's WordNetLemmatizer.

### Intent Classification
1. The preprocessed text is converted into a numerical vector using **TF-IDF Vectorization** (Term Frequency–Inverse Document Frequency with bigrams).
2. The vector is fed into a **Logistic Regression** classifier trained on the `intents.json` dataset.
3. The classifier outputs a probability for each intent.
4. The highest probability intent is selected.
5. If the probability (confidence) is below **0.40**, the intent is treated as **unknown** and the chatbot asks the user to rephrase.

### Entity Extraction
Regular expressions extract structured data:
- **Name**: matches "my name is X", "I am X", "I'm X", "call me X" patterns.
- **Email**: matches standard email regex.
- **Field**: matches against a list of supported fields (Information Technology, Computer Science, etc.).
- **Experience**: matches Beginner, Intermediate, Advanced, Expert.

---

## Complete Registration Flow

```
IDLE
  |
  v  (user says "I want to register")
COLLECTING_NAME
  |
  v  (user provides name)
COLLECTING_EMAIL
  |
  v  (user provides email, validated)
COLLECTING_FIELD
  |
  v  (user provides field, validated)
COLLECTING_EXPERIENCE
  |
  v  (user provides experience, validated)
CONFIRMATION  -- shows summary, asks yes/no
  |
  +--> YES --> save to JSON --> COMPLETED
  |
  +--> NO --> cancel, reset to IDLE
```

---

## Future Scope

These are **not** currently implemented and are mentioned only as future enhancements:

- BERT / Transformers for intent classification
- LLM integration
- RAG (Retrieval-Augmented Generation)
- Multilingual support
- Voice assistant
- Database integration (SQL/NoSQL)
- Admin dashboard
- Analytics
- Sentiment analysis

---

## Academic Context

This project is presented as a **7th semester Industrial Training project** for a B.Tech Information Technology program. It demonstrates practical application of NLP, Machine Learning, and full-stack web development without relying on any paid or external AI API.
