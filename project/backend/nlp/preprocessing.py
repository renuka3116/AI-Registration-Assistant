"""
NLP Preprocessing Pipeline

Performs:
1. Lowercasing
2. Special character removal
3. Tokenization
4. Stopword removal
5. Lemmatization

Uses NLTK. Required resources are downloaded automatically on first use.
"""
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure required NLTK resources are available. Downloaded once, cached locally.
_NLTK_RESOURCES = ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4"]


def _ensure_nltk_resources():
    """Download required NLTK resources if not already present."""
    for resource in _NLTK_RESOURCES:
        try:
            nltk.data.find(f"tokenizers/{resource}")
        except LookupError:
            try:
                nltk.download(resource, quiet=True)
            except Exception:
                pass
    # Stopwords and wordnet live in corpora/
    for corpus in ["stopwords", "wordnet", "omw-1.4"]:
        try:
            nltk.data.find(f"corpora/{corpus}")
        except LookupError:
            try:
                nltk.download(corpus, quiet=True)
            except Exception:
                pass


_ensure_nltk_resources()

# Module-level singletons (created once, reused across requests).
_LEMMATIZER = WordNetLemmatizer()
try:
    _STOPWORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords", quiet=True)
    _STOPWORDS = set(stopwords.words("english"))

# Keep these tokens because they carry intent meaning even though they are stopwords.
_INTENT_STOPWORD_WHITELIST = {"not", "no", "yes", "i", "me", "my", "what", "how", "when", "where"}

# Pattern for characters to keep: word chars, spaces, and basic punctuation we strip later.
_SPECIAL_CHAR_RE = re.compile(r"[^a-z\s]")


def preprocess(text: str) -> str:
    """Run the full NLP preprocessing pipeline and return a cleaned string."""
    if not text or not isinstance(text, str):
        return ""

    # 1. Lowercase
    text = text.lower()

    # 2. Remove special characters (keep only letters and whitespace)
    text = _SPECIAL_CHAR_RE.sub(" ", text)

    # 3. Tokenize
    tokens = word_tokenize(text)

    # 4. Remove stopwords (keep intent-bearing ones) + 5. Lemmatize
    cleaned_tokens = []
    for token in tokens:
        if token in _STOPWORDS and token not in _INTENT_STOPWORD_WHITELIST:
            continue
        if len(token) <= 1:
            continue
        cleaned_tokens.append(_LEMMATIZER.lemmatize(token))

    return " ".join(cleaned_tokens)


def preprocess_tokens(text: str) -> list:
    """Return the cleaned token list instead of a joined string."""
    return preprocess(text).split()
