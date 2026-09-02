"""
Intent Classifier

Trains a TF-IDF Vectorizer + Logistic Regression pipeline on intents.json.
The model is trained automatically when this module is imported (i.e. on backend start).
"""
import json
import os
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from nlp.preprocessing import preprocess

# Confidence threshold: predictions below this are treated as "unknown".
CONFIDENCE_THRESHOLD = 0.40

# Path to the intents dataset.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTENTS_PATH = os.path.join(BASE_DIR, "data", "intents.json")


def load_intents(path: str = INTENTS_PATH) -> dict:
    """Load the intents JSON dataset."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class IntentClassifier:
    """Wraps a TF-IDF + Logistic Regression pipeline for intent classification."""

    def __init__(self, intents_path: str = INTENTS_PATH):
        self.intents_path = intents_path
        self.pipeline = None
        self.tags = []  # ordered list of intent tags aligned with training labels
        self.responses = {}  # tag -> list of response templates
        self._train()

    def _train(self):
        """Train the classifier from the intents dataset."""
        data = load_intents(self.intents_path)
        texts = []
        labels = []
        self.responses = {}

        for intent in data["intents"]:
            tag = intent["tag"]
            self.responses[tag] = intent["responses"]
            for pattern in intent["patterns"]:
                cleaned = preprocess(pattern)
                if cleaned:
                    texts.append(cleaned)
                    labels.append(tag)

        # Keep the unique tag order for interpretability.
        self.tags = list(dict.fromkeys(labels))

        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
            ("clf", LogisticRegression(max_iter=1000, C=1.0)),
        ])
        self.pipeline.fit(texts, labels)

    def classify(self, text: str) -> tuple:
        """
        Classify a user message.
        Returns (intent_tag, confidence, response).
        If confidence < threshold, intent_tag is "unknown".
        """
        if not text or not text.strip():
            return "unknown", 0.0, "I didn't catch that. Could you please say that again?"

        cleaned = preprocess(text)
        if not cleaned:
            return "unknown", 0.0, "I'm not sure I understood that. Could you please rephrase your question?"

        proba = self.pipeline.predict_proba([cleaned])[0]
        classes = self.pipeline.classes_
        best_idx = int(proba.argmax())
        intent = classes[best_idx]
        confidence = float(proba[best_idx])

        if confidence < CONFIDENCE_THRESHOLD:
            return "unknown", confidence, "I'm not sure I understood that. Could you please rephrase your question?"

        response = random.choice(self.responses.get(intent, ["I'm not sure how to respond to that."]))
        return intent, confidence, response

    def get_response(self, tag: str) -> str:
        """Return a random response template for a known intent tag."""
        options = self.responses.get(tag, [])
        if not options:
            return "I'm not sure how to respond to that."
        return random.choice(options)
