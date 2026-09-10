from gemini_classifier import classify_message


messages = [
    "My order is delayed",
    "I want a refund for this item",
    "I was charged twice for my order",
    "I cannot login to my account",
    "My Prime membership is not working",
]


for message in messages:
    prediction = classify_message(message)

    print("Message:", message)
    print("Intent:", prediction)
    print()