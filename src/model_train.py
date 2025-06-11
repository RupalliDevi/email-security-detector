import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import pickle
import os

# Load train and test datasets separately
X_train = pd.read_csv('data/X_train.csv')['message']  # Adjust column name if different
y_train = pd.read_csv('data/y_train.csv')['label']    # Adjust column name if different
X_test = pd.read_csv('data/X_test.csv')['message']
y_test = pd.read_csv('data/y_test.csv')['label']

# Vectorize the text data based on training data
vectorizer = TfidfVectorizer(stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)  # Use the same vectorizer for test data

# Train the model
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Evaluate on test data
y_pred = model.predict(X_test_vec)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

# Save the vectorizer and model
os.makedirs('models', exist_ok=True)
with open('models/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
with open('models/spam_detector.pkl', 'wb') as f:
    pickle.dump(model, f)
