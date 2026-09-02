from models.intent_classifier import IntentClassifier

classifier = IntentClassifier()

queries = [
    "What are the requirements?",
    "What are the requirements",
    "What skills are needed?",
    "Who can apply?",
    "Tell me about the internship",
    "I want to register"
]

for query in queries:
    intent, confidence, response = classifier.classify(query)

    print("\nUser:", query)
    print("Intent:", intent)
    print("Confidence:", confidence)
    print("Response:", response)