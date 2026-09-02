"""
Dialog Manager

Maintains the conversation state and registration data for the current session.
Drives the multi-turn registration flow:

IDLE -> COLLECTING_NAME -> COLLECTING_EMAIL -> COLLECTING_FIELD
    -> COLLECTING_EXPERIENCE -> CONFIRMATION -> COMPLETED
"""
from entities.entity_extractor import (
    extract_name,
    extract_email,
    extract_field,
    extract_experience,
    is_valid_name,
    is_valid_email,
    is_valid_field,
    is_valid_experience,
    SUPPORTED_FIELDS,
    EXPERIENCE_LEVELS,
)

# Conversation states.
IDLE = "idle"
COLLECTING_NAME = "collecting_name"
COLLECTING_EMAIL = "collecting_email"
COLLECTING_FIELD = "collecting_field"
COLLECTING_EXPERIENCE = "collecting_experience"
CONFIRMATION = "confirmation"
COMPLETED = "completed"
COLLECTING_STATUS_EMAIL = "collecting_status_email"


class DialogManager:
    """Stateful dialog manager for a single conversation session."""

    def __init__(self):
        self.state = IDLE
        self.registration = {}  # name, email, field, experience
        self.last_intent = None

    # --- Public API ---

    def reset(self):
        """Reset the conversation to its initial state."""
        self.state = IDLE
        self.registration = {}
        self.last_intent = None

    def get_state(self) -> str:
        return self.state

    def get_registration(self) -> dict:
        return dict(self.registration)

    def is_completed(self) -> bool:
        return self.state == COMPLETED

    def handle_intent(self, intent: str, message: str, classifier_response: str) -> tuple:
        """
        Process the classified intent + raw message in the context of the current state.
        Returns (response_text, registration_state).
        """
        self.last_intent = intent

        # If we are mid-registration, the dialog flow takes priority over free intents,
        # except for explicit cancellation/help.
        if self.state in (
            COLLECTING_NAME,
            COLLECTING_EMAIL,
            COLLECTING_FIELD,
            COLLECTING_EXPERIENCE,
            COLLECTING_STATUS_EMAIL,
        ):
            return self._handle_collection(message, intent)

        if self.state == CONFIRMATION:
            return self._handle_confirmation(intent, message)

        # IDLE or COMPLETED: respond based on intent.
        return self._handle_idle(intent, message, classifier_response)

    # --- State handlers ---

    def _handle_idle(self, intent: str, message: str, classifier_response: str) -> tuple:
        """Handle intents when not in the middle of a registration flow."""
        if intent == "register":
            self.state = COLLECTING_NAME
            return "Sure! I'll help you with the registration. What is your full name?", self.state

        if intent == "application_status":
            self.state = COLLECTING_STATUS_EMAIL
            return (
                "Let me check your application status. "
                "Could you please provide the email you registered with?",
                self.state
            )

        # greeting, internship_info, requirements, help, thank_you, goodbye, unknown
        return classifier_response, self.state

    def _handle_collection(self, message: str, intent: str) -> tuple:
        """Collect registration fields one at a time based on current state."""

        if self.state == COLLECTING_NAME:
            return self._collect_name(message)

        if self.state == COLLECTING_EMAIL:
            return self._collect_email(message)

        if self.state == COLLECTING_FIELD:
            return self._collect_field(message)

        if self.state == COLLECTING_EXPERIENCE:
            return self._collect_experience(message)

        if self.state == COLLECTING_STATUS_EMAIL:
            return self._collect_status_email(message)

        return "Something went wrong. Let's start over.", IDLE

    def _collect_name(self, message: str) -> tuple:
        name = extract_name(message)
        if not name:
            # If no explicit pattern matched, treat the whole message as the name
            # provided it contains alphabetic characters.
            candidate = message.strip()
            if is_valid_name(candidate):
                name = candidate

        if not is_valid_name(name):
            return "I didn't catch your name. Could you please tell me your full name?", self.state

        self.registration["name"] = name
        self.state = COLLECTING_EMAIL
        return f"Nice to meet you, {name}! What is your email address?", self.state

    def _collect_email(self, message: str) -> tuple:
        email = extract_email(message)
        if not is_valid_email(email):
            return "That email address doesn't look valid. Please enter a valid email address.", self.state

        self.registration["email"] = email
        self.state = COLLECTING_FIELD
        fields_list = ", ".join(SUPPORTED_FIELDS)
        return f"Great! What is your field of study? (e.g. {fields_list})", self.state

    def _collect_field(self, message: str) -> tuple:
        field = extract_field(message)
        if not is_valid_field(field):
            fields_list = ", ".join(SUPPORTED_FIELDS)
            return f"I couldn't recognize that field. Please choose from: {fields_list}", self.state

        self.registration["field"] = field
        self.state = COLLECTING_EXPERIENCE
        levels = ", ".join(EXPERIENCE_LEVELS)
        return f"Excellent! What is your programming experience level? ({levels})", self.state

    def _collect_status_email(self, message: str) -> tuple:
        email = extract_email(message)

        if not is_valid_email(email):
            return (
                "That email address doesn't look valid. "
                "Please enter a valid registered email address.",
                self.state
            )

        self.state = IDLE

        return email, self.state

    def _collect_experience(self, message: str) -> tuple:
        experience = extract_experience(message)
        if not is_valid_experience(experience):
            levels = ", ".join(EXPERIENCE_LEVELS)
            return f"I didn't recognize that level. Please choose from: {levels}", self.state

        self.registration["experience"] = experience
        self.state = CONFIRMATION
        summary = self._build_summary()
        return summary, self.state

    def _handle_confirmation(self, intent: str, message: str) -> tuple:
        """Handle the confirmation step (yes / no)."""
        if intent == "confirmation_yes":
            self.state = COMPLETED
            return "yes", self.state  # special marker: caller saves the registration
        if intent == "confirmation_no":
            self.state = IDLE
            self.registration = {}
            return "Your registration has been cancelled. You can start again anytime by saying you'd like to register.", self.state
        # Ambiguous answer at confirmation: re-show summary.
        return "Please reply with 'yes' to confirm or 'no' to cancel. Would you like to confirm your registration?", self.state

    # --- Helpers ---

    def _build_summary(self) -> str:
        r = self.registration
        summary = (
            "Here is your registration summary:\n\n"
            f"Name: {r.get('name', 'N/A')}\n"
            f"Email: {r.get('email', 'N/A')}\n"
            f"Field: {r.get('field', 'N/A')}\n"
            f"Experience: {r.get('experience', 'N/A')}\n\n"
            "Would you like to confirm your registration? (yes / no)"
        )
        return summary
