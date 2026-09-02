from flask import Flask, request, jsonify
from flask_cors import CORS

from models.intent_classifier import IntentClassifier
from conversation.dialog_manager import DialogManager, COLLECTING_STATUS_EMAIL
from entities.entity_extractor import extract_entities

from database import (
    initialize_database,
    save_registration,
    get_registration_by_email,
    get_all_registrations
)


app = Flask(__name__)
CORS(app)


# Initialize SQLite database
initialize_database()


# Initialize AI Intent Classifier
classifier = IntentClassifier()


# Initialize Dialog Manager
dialog_manager = DialogManager()


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running"
    })


@app.route("/api/chat", methods=["POST"])
def chat():

    # Get JSON data from frontend
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({
            "error": "Message is required"
        }), 400


    message = data["message"].strip()

    if not message:
        return jsonify({
            "error": "Message cannot be empty"
        }), 400


    # STEP 1: Extract entities
    entities = extract_entities(message)


    # STEP 2: Classify user intent
    intent, confidence, classifier_response = classifier.classify(message)


    # IMPORTANT:
    # Save the current state BEFORE sending message to Dialog Manager
    previous_state = dialog_manager.get_state()


    # STEP 3: Dialog Manager handles conversation
    response, state = dialog_manager.handle_intent(
        intent,
        message,
        classifier_response
    )


    # ==================================================
    # STEP 4: CHECK APPLICATION STATUS
    # ==================================================

    # If chatbot was waiting for status email
    if previous_state == COLLECTING_STATUS_EMAIL:

        email = entities.get("email")

        if email:

            found_registration = get_registration_by_email(email)

            if found_registration:

                response = (
                    "🎉 Application Found!\n\n"
                    f"Name: {found_registration['name']}\n"
                    f"Email: {found_registration['email']}\n"
                    f"Field: {found_registration['field']}\n"
                    f"Experience: {found_registration['experience']}\n\n"
                    f"Status: {found_registration.get('status', 'Registration Confirmed')} ✅"
                )

            else:

                response = (
                    "❌ No registration found with this email address.\n\n"
                    "Please check the email address or register first."
                )


    # ==================================================
    # STEP 5: SAVE COMPLETED REGISTRATION TO SQLITE
    # ==================================================

    if state == "completed" and response == "yes":

        registration = dialog_manager.get_registration()


        success, db_message = save_registration(
            registration.get("name", ""),
            registration.get("email", ""),
            registration.get("field", ""),
            registration.get("experience", "")
        )


        if success:

            response = (
                "🎉 Your registration has been successfully completed!\n\n"
                f"Name: {registration.get('name', '')}\n"
                f"Email: {registration.get('email', '')}\n"
                f"Field: {registration.get('field', '')}\n"
                f"Experience: {registration.get('experience', '')}\n\n"
                "Status: Registration Confirmed ✅\n\n"
                "Thank you for registering!"
            )

        else:

            response = (
                f"⚠️ {db_message}\n\n"
                "This email may already be registered. "
                "Please check your application status."
            )


    # ==================================================
    # STEP 6: RETURN RESPONSE TO FRONTEND
    # ==================================================

    return jsonify({
        "response": response,
        "intent": intent,
        "confidence": round(confidence, 2),
        "entities": entities,
        "registration_state": state,
        "registration_data": dialog_manager.get_registration()
    })


# ==================================================
# RESET CONVERSATION
# ==================================================

@app.route("/api/reset", methods=["POST"])
def reset():

    dialog_manager.reset()

    return jsonify({
        "message": "Conversation reset successfully",
        "registration_state": "idle"
    })


# ==================================================
# GET ALL REGISTRATIONS
# ==================================================

@app.route("/api/registrations", methods=["GET"])
def registrations():

    all_registrations = get_all_registrations()

    return jsonify({
        "registrations": all_registrations
    })


# ==================================================
# RUN FLASK SERVER
# ==================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )