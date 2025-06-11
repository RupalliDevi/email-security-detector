import streamlit as st
import time
import json
import re
from io import StringIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# === Page Config ===
st.set_page_config(page_title="Email Detector", layout="centered")

# === Custom CSS Styling ===
st.markdown("""
<style>
body, .stApp {
    background-color: #0f111a;
    color: #f0f0f0;
    font-family: 'Segoe UI', sans-serif;
}

h1, h2, h3, h4, .css-10trblm, .css-1v3fvcr {
    color: #00f2ff !important;
}

.stTextInput label, .stTextArea label {
    color: #ffffff !important;
    font-weight: bold;
}

.stButton button {
    background-color: #00f2ff;
    color: black;
    border: 2px solid #00f2ff;
    border-radius: 8px;
    font-weight: bold;
    transition: 0.4s;
}

.stButton button:hover {
    background-color: #0d7377;
    color: white;
    box-shadow: 0 0 15px #00f2ff;
}

.stDownloadButton button {
    background-color: #111;
    color: #00f2ff;
    border: 2px solid #00f2ff;
    border-radius: 8px;
    font-weight: bold;
    padding: 8px 16px;
    margin-top: 10px;
    transition: 0.3s;
}

.stDownloadButton button:hover {
    background-color: #00f2ff;
    color: black;
    box-shadow: 0 0 10px #00f2ff;
}

.spinner-ball {
    margin: auto;
    width: 30px;
    height: 30px;
    background-color: #00f2ff;
    border-radius: 50%;
    animation: bounce 0.8s infinite alternate;
}

@keyframes bounce {
    to {
        transform: translateY(-20px);
    }
}

.score-bar {
    background-color: #333;
    height: 20px;
    border-radius: 10px;
    margin-top: 10px;
    margin-bottom: 10px;
}

.score-fill {
    background-color: #e74c3c;
    height: 100%;
    border-radius: 10px;
    text-align: center;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# === Summarizer Function ===
def summarize_email(text, num_sentences=2):
    sentences = re.split(r'(?<=[.!?]) +', text)
    if len(sentences) <= num_sentences:
        return text
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(sentences)
    model = KMeans(n_clusters=num_sentences, random_state=0).fit(X)
    summary_sentences = [sentences[i] for i in model.cluster_centers_.argsort(axis=0)[:num_sentences].flatten()]
    return ' '.join(summary_sentences)

# === Analyzer Function ===
def analyze_email(email_text, sender_email):
    time.sleep(1.5)

    score = 0
    suspicious_phrases = []
    if "urgent" in email_text.lower():
        suspicious_phrases.append("urgent")
        score += 30
    if "verify" in email_text.lower():
        suspicious_phrases.append("verify")
        score += 20
    if "bank account" in email_text.lower():
        suspicious_phrases.append("bank account")
        score += 30

    urls_found = re.findall(r'https?://\S+', email_text)
    if urls_found:
        score += 10

    spam_result = "Spam" if score >= 50 else "Not Spam"
    reputation = "⚠️ Suspicious" if any(domain in sender_email for domain in [".ru", ".xyz", "mail.ru"]) else "✅ Trusted"
    if "Suspicious" in reputation:
        score += 10

    summary = summarize_email(email_text)
    score = min(score, 100)

    return spam_result, suspicious_phrases, urls_found, reputation, summary, score

# === App UI ===
st.title("🔒 Email Spam & Phishing Detector")

sender_email = st.text_input("📧 Sender Email Address", placeholder="e.g., scammer@mail.ru")
email_text = st.text_area("✉️ Paste the full email body here…", height=150, placeholder="Enter or paste your email text here...")

if st.button("Analyze"):
    if not email_text.strip() or not sender_email.strip():
        st.warning("Please enter both sender email and email content.")
    else:
        with st.spinner("Analyzing email..."):
            st.markdown('<div class="spinner-ball"></div>', unsafe_allow_html=True)
            spam_result, suspicious_phrases, urls_found, reputation, summary, score = analyze_email(email_text, sender_email)

        st.subheader("🔍 Analysis Result")

        # Spam result with icon
        if spam_result == "Spam":
            st.markdown(f"<h4 style='color:#e74c3c'>🚨 Spam</h4>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h4 style='color:#27ae60'>✅ Not Spam</h4>", unsafe_allow_html=True)

        # Reputation
        if "Suspicious" in reputation:
            st.markdown(f"<b style='color:#f39c12'>{reputation}</b>", unsafe_allow_html=True)
        else:
            st.markdown(f"<b style='color:#2980b9'>{reputation}</b>", unsafe_allow_html=True)

        # Score visualization
        st.markdown("**Spam/Phishing Score:**")
        st.markdown(f"""
            <div class="score-bar">
                <div class="score-fill" style="width: {score}%;">{score}%</div>
            </div>
        """, unsafe_allow_html=True)

        # Suspicious Phrases
        if suspicious_phrases:
            st.markdown("**Suspicious Phrases:**")
            st.markdown(", ".join([f"<span style='background-color: #f39c12; padding: 3px 6px; border-radius: 5px;'>{p}</span>" for p in suspicious_phrases]), unsafe_allow_html=True)
        else:
            st.markdown("**Suspicious Phrases:** None detected")

        # URLs
        if urls_found:
            st.markdown("**URLs Found:**")
            for url in urls_found:
                st.markdown(f"- {url}")
        else:
            st.markdown("**URLs Found:** None")

        # Summary
        with st.expander("📝 Email Summary"):
            st.success(summary)

        # Word stats
        word_count = len(email_text.split())
        read_time = round(word_count / 200, 2)
        st.info(f"**Word Count:** {word_count} | **Estimated Read Time:** {read_time} min")

        # Wordcloud
        st.markdown("**📊 Word Cloud:**")
        wordcloud = WordCloud(width=600, height=300, background_color='black', colormap='spring').generate(email_text)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

        # Download
        result_data = {
            "spam_check": spam_result,
            "score": score,
            "suspicious_phrases": suspicious_phrases,
            "urls_found": urls_found,
            "email_summary": summary,
            "email_text": email_text,
            "sender_email": sender_email,
            "reputation": reputation,
            "word_count": word_count,
            "read_time_min": read_time
        }
        result_json = json.dumps(result_data, indent=4)
        st.download_button(
            label="📥 Download Result as JSON",
            data=result_json,
            file_name="email_analysis.json",
            mime="application/json"
        )
