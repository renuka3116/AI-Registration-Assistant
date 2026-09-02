"""Unit tests for the entity extractor."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from entities.entity_extractor import (
    extract_name,
    extract_email,
    extract_field,
    extract_experience,
    extract_entities,
    is_valid_name,
    is_valid_email,
    is_valid_field,
    is_valid_experience,
)


# --- Name ---

def test_name_my_name_is():
    assert extract_name("My name is Renuka Srivastava") == "Renuka Srivastava"


def test_name_i_am():
    assert extract_name("I am Renuka Srivastava") == "Renuka Srivastava"


def test_name_im():
    assert extract_name("I'm Renuka Srivastava") == "Renuka Srivastava"


def test_name_not_found():
    assert extract_name("Hello there") is None


# --- Email ---

def test_valid_email():
    assert extract_email("renuka@gmail.com") == "renuka@gmail.com"


def test_email_in_sentence():
    assert extract_email("My email is renuka@gmail.com please register me") == "renuka@gmail.com"


def test_invalid_email():
    assert extract_email("renuka at gmail dot com") is None


def test_email_validation():
    assert is_valid_email("renuka@gmail.com") is True
    assert is_valid_email("invalid-email") is False
    assert is_valid_email("user@.com") is False


# --- Field ---

def test_field_information_technology():
    assert extract_field("My field is Information Technology") == "Information Technology"


def test_field_computer_science():
    assert extract_field("I study Computer Science") == "Computer Science"


def test_field_data_science():
    assert extract_field("Data Science") == "Data Science"


def test_field_not_recognized():
    assert extract_field("I study Physics") is None


# --- Experience ---

def test_experience_beginner():
    assert extract_experience("I am a Beginner") == "Beginner"


def test_experience_intermediate():
    assert extract_experience("Intermediate level") == "Intermediate"


def test_experience_advanced():
    assert extract_experience("Advanced") == "Advanced"


def test_experience_expert():
    assert extract_experience("I am an Expert") == "Expert"


def test_experience_not_recognized():
    assert extract_experience("I have 5 years of experience") is None


# --- Combined ---

def test_extract_entities_all():
    text = "My name is Renuka Srivastava, email renuka@gmail.com, field Information Technology, experience Beginner"
    entities = extract_entities(text)
    assert entities.get("name") == "Renuka Srivastava"
    assert entities.get("email") == "renuka@gmail.com"
    assert entities.get("field") == "Information Technology"
    assert entities.get("experience") == "Beginner"


def test_extract_entities_none():
    entities = extract_entities("Hello there how are you")
    assert entities == {}


# --- Validation ---

def test_name_validation():
    assert is_valid_name("Renuka") is True
    assert is_valid_name("") is False
    assert is_valid_name("123") is False
    assert is_valid_name("A") is False


def test_field_validation():
    assert is_valid_field("Information Technology") is True
    assert is_valid_field("Physics") is False
    assert is_valid_field("") is False


def test_experience_validation():
    assert is_valid_experience("Beginner") is True
    assert is_valid_experience("Expert") is True
    assert is_valid_experience("Novice") is False
    assert is_valid_experience("") is False
