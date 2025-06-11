import pickle

# Load the saved vectorizer and model
with open('models/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('models/spam_detector.pkl', 'rb') as f:
    model = pickle.load(f)

def predict_spam(message):
    # Transform the message using the loaded vectorizer
    message_vector = vectorizer.transform([message])
    # Predict using the loaded model
    prediction = model.predict(message_vector)
    return prediction[0]

if __name__ == "__main__":
    # Test some sample messages
    test_messages = [
        "Congratulations! You've won a $1000 Walmart gift card. Go to http://bit.ly/123456 to claim now.",
        "Hey, are we still meeting for lunch today?",
        "URGENT! Your mobile number has won £5000. Reply to claim your prize."
    ]
    
    for msg in test_messages:
        result = predict_spam(msg)
        print(f"Message: {msg}\nPrediction: {result}\n")
