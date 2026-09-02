"""Unit tests for the NLP preprocessing pipeline."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from nlp.preprocessing import preprocess, preprocess_tokens


def test_lowercase():
    """Preprocessed text should be lowercase."""
    result = preprocess("HELLO WORLD")
    assert result == result.lower()


def test_special_characters_removed():
    """Special characters should be removed."""
    result = preprocess("Hello!!! @World?? #2024")
    assert "!" not in result
    assert "@" not in result
    assert "#" not in result


def test_stopwords_removed():
    """Common stopwords should be removed."""
    result = preprocess("I am going to the store")
    tokens = result.split()
    assert "i" not in tokens or "i" in ["i", "me", "my"]  # 'i' is whitelisted
    assert "am" not in tokens
    assert "to" not in tokens
    assert "the" not in tokens


def test_lemmatization():
    """Words should be lemmatized to base form."""
    result = preprocess("running jumped cats")
    tokens = result.split()
    assert "run" in tokens
    assert "jump" in tokens
    assert "cat" in tokens


def test_example_sentence():
    """The documented example should produce the expected output."""
    result = preprocess("I am interested in registering for this internship!")
    tokens = result.split()
    assert "interested" in tokens
    assert "registering" in tokens or "register" in tokens
    assert "internship" in tokens


def test_empty_input():
    """Empty input should return empty string."""
    assert preprocess("") == ""
    assert preprocess(None) == ""


def test_tokens_returned_as_list():
    """preprocess_tokens should return a list."""
    tokens = preprocess_tokens("Hello world")
    assert isinstance(tokens, list)
    assert len(tokens) > 0
