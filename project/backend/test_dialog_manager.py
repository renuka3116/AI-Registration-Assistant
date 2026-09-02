from conversation.dialog_manager import DialogManager


dialog = DialogManager()


def test_message(intent, message, classifier_response=""):
    response, state = dialog.handle_intent(
        intent,
        message,
        classifier_response
    )

    print("\nUser:", message)
    print("Intent:", intent)
    print("Bot:", response)
    print("State:", state)


# Step 1: Start registration
test_message(
    "register",
    "I want to register"
)

# Step 2: Name
test_message(
    "unknown",
    "Renuka Srivastava"
)

# Step 3: Email
test_message(
    "unknown",
    "renuka@gmail.com"
)

# Step 4: Field
test_message(
    "unknown",
    "Information Technology"
)

# Step 5: Experience
test_message(
    "unknown",
    "Beginner"
)

# Step 6: Confirmation
test_message(
    "confirmation_yes",
    "Yes"
)


print("\n--- FINAL RESULT ---")
print("Registration:", dialog.get_registration())
print("Completed:", dialog.is_completed())