# 🔒 Email Spam & Phishing Detector

An interactive Streamlit-based web application that analyzes email content for potential spam and phishing threats. It provides an intuitive UI and insightful results including a summary, suspicious phrases, URLs, and both spam and phishing scores.

## 🚀 Features

- 🔍 **Spam & Phishing Detection** using keyword matching, domain reputation, and heuristic scoring.
- 📊 **Spam Score vs Phishing Score** side-by-side visual representation.
- 📝 **Email Summarization** using TF-IDF and KMeans clustering.
- 🌐 **URL Extraction** from email body.
- ☁️ **Word Cloud Visualization** for high-frequency terms.
- 📥 **Downloadable JSON Report** for analysis output.

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **Scikit-learn**
- **Matplotlib**
- **WordCloud**
- **Regex**

## 📂 How to Run

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/email-spam-phishing-detector.git
   cd email-spam-phishing-detector
2. Install dependencies:
pip install -r requirements.txt

3.Run the Streamlit app:
streamlit run app.py

The downloadable result includes:
{
  "spam_check": "Spam / Not Spam",
  "spam_score": 75,
  "phishing_score": 60,
  "suspicious_phrases": ["urgent", "verify"],
  "urls_found": ["http://example.com"],
  "email_summary": "Summary of the email",
  "sender_email": "example@domain.com",
  "reputation": "⚠️ Suspicious / ✅ Trusted",
  "word_count": 124,
  "read_time_min": 0.6
}


Author
Rupalli Devi
📧 Email: rupalli2802@gmail.com
🔗 LinkedIn: [linkedin.com/in/yourprofile](https://www.linkedin.com/in/rupalli-d-2b0659224/)
# © 2025 Rupalli Devi. All rights reserved.

