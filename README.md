#  AI Registration Assistant

An NLP-based conversational chatbot designed to simplify and automate the internship registration process.

The system allows students to interact with a chatbot, get internship-related information, complete a multi-step registration process, and check their application status.

---

##  Features

-  Interactive chatbot interface
-  NLP-based user message processing
-  Intent Classification using TF-IDF and Logistic Regression
-  Entity Extraction for:
  - Name
  - Email Address
  - Field of Study
  - Programming Experience
-  Multi-step registration workflow
-  Registration confirmation and validation
-  Dialog Manager for conversation state management
-  SQLite database integration
-  Application status checking
-  React frontend connected with Flask backend
-  REST API integration

---

##  Technologies Used

### Frontend
- React
- TypeScript
- Vite
- Tailwind CSS

### Backend
- Python
- Flask
- Flask-CORS

### NLP & Machine Learning
- NLTK
- Scikit-learn
- TF-IDF Vectorizer
- Logistic Regression

### Database
- SQLite

---

##  System Architecture

```text
User
  │
  ▼
React Frontend
  │
  │ HTTP / JSON
  ▼
Flask Backend
  │
  ├── NLP Preprocessing
  ├── Intent Classification
  ├── Entity Extraction
  └── Dialog Manager
          │
          ▼
    SQLite Database
          │
          ▼
   Response to User
