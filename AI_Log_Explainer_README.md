# 🧠 AI Log Explainer (Cloud-Native DevOps AI Tool)

An AI-powered, cloud-native log analysis system that transforms raw, unstructured logs into **actionable insights** using **Google Gemini AI**.

---

## 🎬 Demo

![Demo GIF](assets/demo.gif)

> _(Replace with your actual demo GIF)_

---

## 🚀 Problem Statement

Modern systems generate massive volumes of logs that are:

- Unstructured
- Noisy
- Time-consuming to analyze
- Difficult to interpret under pressure

This project solves that by automatically interpreting logs and generating structured insights.

---

## 💡 Solution

AI Log Explainer is a **single-purpose AI agent** that:

- Analyzes logs using Gemini AI
- Extracts insights
- Outputs structured results

### 🔍 Output Format

- Summary
- Root Cause
- Suggested Fix
- Severity

---

## 🏗️ Architecture

```
User → Streamlit (Cloud Run) → Gemini API → Cloud SQL → Storage
```

---

## ⚙️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **AI:** Google Gemini (gemini-2.5-flash)
- **Cloud:** Cloud Run, Cloud SQL
- **Database:** SQLAlchemy, PyMySQL

---

## 🔥 Features

- AI-powered log summarization
- Root cause detection
- Step-by-step fixes
- Severity classification
- History tracking
- Rate limiting + sanitization
- Secure DB handling

---

## ⚡ Local Setup

```bash
python -m venv venv
source venv/bin/activate # Git Bash (activate python venv)
pip install -r requirements.txt
streamlit run app.py
```

```bash
# Ensure that you have created your own CLOUD SQL INSTANCE and GEMINI API key first in Google Cloud!
# Then set your configuration variables on the terminal
GEMINI_API_KEY=your_api_key_here
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_NAME=your_db_name
```

---

## ☁️ Deploy (Cloud Run)

```bash
gcloud run deploy ai-log-explainer --source . --region us-central1 --allow-unauthenticated --set-env-vars GEMINI_API_KEY="$GEMINI_API_KEY",DB_USER="$DB_USER",DB_PASSWORD="$DB_PASSWORD",DB_HOST="$DB_HOST",DB_NAME="$DB_NAME"

#Then use the deployment link produced after running gcloud run to use the app in your browser.
```

---

## 🧪 Usage

1. Paste logs
2. Click Analyze
3. View results
4. Check history

---

## 📊 Example Output

```
Summary:
Memory issue detected

Root Cause:
Possible memory leak

Suggested Fix:
1. Restart service
2. Optimize usage
3. Monitor system

Severity:
HIGH
```

---

## 📸 Screenshots

### 🖥 Main Interface

![Main UI](assets/screenshots/main-ui.png)

### 🔍 Analysis Results

![Results](assets/screenshots/results.png)

### 🛠 Suggested Fix

![Fix](assets/screenshots/fix.png)

### 📊 History Feature

![History](assets/screenshots/history.png)

---

## 🚀 Future Improvements

- Auth system
- API endpoints
- Monitoring dashboard
- Secret Manager integration

---

## 👨‍💻 Author

Ralph Henry L. Dominisac

---

## 📄 License

Educational use only.
