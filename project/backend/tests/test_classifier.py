"""Unit tests for the intent classifier."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.intent_classifier import IntentClassifier, CONFIDENCE_THRESHOLD


def test_greeting_intent():
    """A greeting message should be classified as 'greeting'."""
    clf = IntentClassifier()
    intent, confidence, response = clf.classify("Hello there!")
    assert intent == "greeting"
    assert confidence >= CONFIDENCE_THRESHOLD
    assert isinstance(response, str) and len(response) > 0


def test_register_intent():
    """A registration request should be classified as 'register'."""
    clf = IntentClassifier()
    intent, confidence, response = clf.classify("I want to register for the internship")
    assert intent == "register"
    assert confidence >= CONFIDENCE_THRESHOLD


def test_requirements_intent():
    """A requirements query should be classified as 'requirements'."""
    clf = IntentClassifier()
    intent, confidence, response = clf.classify("What are the requirements to apply?")
    assert intent == "requirements"
    assert confidence >= CONFIDENCE_THRESHOLD


def test_unknown_intent():
    """An off-topic query with low confidence should be 'unknown'."""
    clf = IntentClassifier()
    intent, confidence, response = clf.classify("What is the weather today?")
    assert intent == "unknown"
    assert confidence < CONFIDENCE_THRESHOLD


def test_empty_message():
    """An empty message should be classified as 'unknown'."""
    clf = IntentClassifier()
    intent, confidence, response = clf.classify("")
    assert intent == "unknown"
    assert confidence == 0.0


def test_internship_info():
    """An internship info query should be classified correctly."""
    clf = IntentClassifier()
    intent, confidence, response = clf.classify("Tell me about the internship")
    assert intent == "internship_info"
    assert confidence >= CONFIDENCE_THRESHOLD


def test_help_intent():
    """A help request should be classified as 'help'."""
    clf = IntentClassifier()
    intent, confidence, response = clf.classify("I need help")
    assert intent == "help"
    assert confidence >= CONFIDENCE_THRESHOLD


def test_goodbye_intent():
    """A goodbye message should be classified correctly."""
    clf = IntentClassifier()
    intent, confidence, response = clf.classify("Goodbye see you later")
    assert intent == "goodbye"
    assert confidence >= CONFIDENCE_THRESHOLD


def test_confirmation_yes():
    """A 'yes' confirmation should be classified correctly."""
    clf = IntentClassifier()
    intent, confidence, response = clf.classify("Yes confirm")
    assert intent == "confirmation_yes"
    assert confidence >= CONFIDENCE_THRESHOLD


def test_confirmation_no():
    """A 'no' confirmation should be classified correctly."""
    clf = IntentClassifier()
    intent, confidence, response = clf.classify("No cancel that")
    assert intent == "confirmation_no"
    assert confidence >= CONFIDENCE_THRESHOLD


def test_response_is_string():
    """Every classification should return a string response."""
    clf = IntentClassifier()
    for msg in ["Hi", "I want to register", "Help me", "Goodbye"]:
        _, _, response = clf.classify(msg)
        assert isinstance(response, str)
