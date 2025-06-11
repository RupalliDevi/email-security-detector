import pandas as pd
from sklearn.model_selection import train_test_split

# Load dataset
file_path = r'D:/email-security-detector/data/SMSSpamCollection.csv'  # Update path if needed
df = pd.read_csv(file_path, sep='\t', header=None, names=['label', 'message'])

print(f"Dataset shape: {df.shape}")
print("Sample data:\n", df.head())

# Convert labels to binary
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

# Optional: Clean text (basic)
df['message'] = df['message'].str.lower()

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    df['message'], df['label'], test_size=0.2, random_state=42)

# Save processed data
X_train.to_csv('data/X_train.csv', index=False)
X_test.to_csv('data/X_test.csv', index=False)
y_train.to_csv('data/y_train.csv', index=False)
y_test.to_csv('data/y_test.csv', index=False)

print("✅ Preprocessing complete. Files saved to 'data/' folder.")
