"""
Entity Extractor

Extracts structured information from user messages:

- Name
- Email
- Field of Study
- Programming Experience

Also validates extracted entities.
"""

import re


# ============================================================
# FIELD OF STUDY
# ============================================================

SUPPORTED_FIELDS = [
    "Information Technology",
    "Computer Science Engineering",
    "Computer Science",
    "Data Science",
    "Artificial Intelligence",
    "Electronics",
    "Mechanical Engineering",
    "Biotechnology",
]


# Common short forms / aliases
FIELD_ALIASES = {
    "it": "Information Technology",
    "information technology": "Information Technology",

    "cse": "Computer Science Engineering",
    "computer science engineering": "Computer Science Engineering",

    "cs": "Computer Science",
    "computer science": "Computer Science",

    "ds": "Data Science",
    "data science": "Data Science",

    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",

    "ece": "Electronics",
    "electronics": "Electronics",

    "me": "Mechanical Engineering",
    "mechanical": "Mechanical Engineering",
    "mechanical engineering": "Mechanical Engineering",

    "biotech": "Biotechnology",
    "biotechnology": "Biotechnology",
}


# Longer phrases first
_FIELD_ALTERNATIVES = "|".join(
    sorted(
        [re.escape(key) for key in FIELD_ALIASES.keys()],
        key=len,
        reverse=True
    )
)

FIELD_REGEX = re.compile(
    r"\b(" + _FIELD_ALTERNATIVES + r")\b",
    re.IGNORECASE
)


# ============================================================
# EXPERIENCE
# ============================================================

EXPERIENCE_LEVELS = [
    "Beginner",
    "Intermediate",
    "Advanced",
    "Expert",
]


EXPERIENCE_ALIASES = {

    # Beginner
    "beginner": "Beginner",
    "beginner level": "Beginner",
    "fresher": "Beginner",
    "freshers": "Beginner",
    "no experience": "Beginner",
    "no programming experience": "Beginner",
    "just starting": "Beginner",
    "new to programming": "Beginner",

    # Intermediate
    "intermediate": "Intermediate",
    "intermediate level": "Intermediate",

    # Advanced
    "advanced": "Advanced",
    "advanced level": "Advanced",

    # Expert
    "expert": "Expert",
    "expert level": "Expert",
}


_EXPERIENCE_ALTERNATIVES = "|".join(
    sorted(
        [re.escape(key) for key in EXPERIENCE_ALIASES.keys()],
        key=len,
        reverse=True
    )
)

EXPERIENCE_REGEX = re.compile(
    r"\b(" + _EXPERIENCE_ALTERNATIVES + r")\b",
    re.IGNORECASE
)


# ============================================================
# EMAIL
# ============================================================

EMAIL_REGEX = re.compile(
    r"[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}",
    re.IGNORECASE
)


# ============================================================
# NAME
# ============================================================

# Name extraction supports:
#
# My name is Renuka
# My name is Renuka Srivastava
# I am Renuka
# I'm Renuka
# This is Renuka
# Name is Renuka
# Call me Renuka
#
# It stops before words such as:
# and, my, email, field, study, etc.

NAME_PATTERNS = [

    re.compile(
        r"\bmy name is\s+([A-Za-z][A-Za-z'\-]*(?:\s+[A-Za-z][A-Za-z'\-]*){0,3})",
        re.IGNORECASE
    ),

    re.compile(
        r"\bi am\s+([A-Za-z][A-Za-z'\-]*(?:\s+[A-Za-z][A-Za-z'\-]*){0,3})",
        re.IGNORECASE
    ),

    re.compile(
        r"\bi'm\s+([A-Za-z][A-Za-z'\-]*(?:\s+[A-Za-z][A-Za-z'\-]*){0,3})",
        re.IGNORECASE
    ),

    re.compile(
        r"\bim\s+([A-Za-z][A-Za-z'\-]*(?:\s+[A-Za-z][A-Za-z'\-]*){0,3})",
        re.IGNORECASE
    ),

    re.compile(
        r"\bthis is\s+([A-Za-z][A-Za-z'\-]*(?:\s+[A-Za-z][A-Za-z'\-]*){0,3})",
        re.IGNORECASE
    ),

    re.compile(
        r"\bname is\s+([A-Za-z][A-Za-z'\-]*(?:\s+[A-Za-z][A-Za-z'\-]*){0,3})",
        re.IGNORECASE
    ),

    re.compile(
        r"\bcall me\s+([A-Za-z][A-Za-z'\-]*(?:\s+[A-Za-z][A-Za-z'\-]*){0,3})",
        re.IGNORECASE
    ),
]


# Words that indicate the name has ended
NAME_STOP_WORDS = {
    "and",
    "my",
    "email",
    "is",
    "field",
    "study",
    "experience",
    "level",
    "i",
    "am",
    "im",
}


def _clean_name(candidate: str) -> str | None:
    """
    Clean an extracted name and stop at common sentence connectors.
    """

    words = candidate.strip().split()

    cleaned = []

    for word in words:

        if word.lower() in NAME_STOP_WORDS:
            break

        cleaned.append(word)

        if len(cleaned) == 4:
            break

    if not cleaned:
        return None

    name = " ".join(cleaned).strip()

    if re.search(r"[A-Za-z]", name):
        return name

    return None


def extract_name(text: str) -> str | None:
    """Extract a person's name from the message."""

    if not text:
        return None

    for pattern in NAME_PATTERNS:

        match = pattern.search(text)

        if match:

            name = _clean_name(match.group(1))

            if name:
                return name

    return None


# ============================================================
# EMAIL EXTRACTION
# ============================================================

def extract_email(text: str) -> str | None:
    """Extract an email address from the message."""

    if not text:
        return None

    match = EMAIL_REGEX.search(text)

    if match:
        return match.group(0).strip()

    return None


# ============================================================
# FIELD EXTRACTION
# ============================================================

def extract_field(text: str) -> str | None:
    """Extract and normalize field of study."""

    if not text:
        return None

    match = FIELD_REGEX.search(text)

    if match:

        field_key = match.group(1).lower().strip()

        return FIELD_ALIASES.get(field_key)

    return None


# ============================================================
# EXPERIENCE EXTRACTION
# ============================================================

def extract_experience(text: str) -> str | None:
    """Extract and normalize programming experience."""

    if not text:
        return None

    match = EXPERIENCE_REGEX.search(text)

    if match:

        experience_key = match.group(1).lower().strip()

        return EXPERIENCE_ALIASES.get(experience_key)

    return None


# ============================================================
# EXTRACT ALL ENTITIES
# ============================================================

def extract_entities(text: str) -> dict:
    """
    Extract all entities present in a message.

    Possible keys:
    name
    email
    field
    experience
    """

    entities = {}

    name = extract_name(text)
    email = extract_email(text)
    field = extract_field(text)
    experience = extract_experience(text)

    if name:
        entities["name"] = name

    if email:
        entities["email"] = email

    if field:
        entities["field"] = field

    if experience:
        entities["experience"] = experience

    return entities


# ============================================================
# VALIDATION
# ============================================================

def is_valid_name(name: str) -> bool:
    """Validate a person's name."""

    if not name or not isinstance(name, str):
        return False

    name = name.strip()

    if len(name) < 2:
        return False

    if not re.search(r"[A-Za-z]", name):
        return False

    return True


def is_valid_email(email: str) -> bool:
    """Validate an email address."""

    if not email or not isinstance(email, str):
        return False

    return bool(
        EMAIL_REGEX.fullmatch(email.strip())
    )


def is_valid_field(field: str) -> bool:
    """Validate a field of study."""

    if not field:
        return False

    return field in SUPPORTED_FIELDS


def is_valid_experience(level: str) -> bool:
    """Validate experience level."""

    if not level:
        return False

    return level in EXPERIENCE_LEVELS