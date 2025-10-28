# 💬 AI-Powered LinkedIn Outreach Message Generator

## 🧠 Overview

This project is an AI-powered LinkedIn Outreach Message Generator that creates personalized, human-like outreach messages for professionals at scale.

It uses Groq’s AI API with a Streamlit web app to help recruiters, marketers, founders, and networkers send natural, context-aware LinkedIn messages that sound authentic, not robotic.

## ⚙️ Approach Summary

The system dynamically generates outreach messages using:

- Recipient’s Name

- Job Role / Title

- Company

- Outreach Intent (hiring, marketing, sales, partnership, collaboration, networking)

- LinkedIn post or profile text for deeper personalization

Unlike rule-based templates, this app leverages prompt-driven generative AI to produce messages that are conversational, unique, and contextually aligned.
It also includes real-time user feedback and infinite regeneration for improved personalization.

## 💡 Key Features

## 🧩 Input Options

- **Manual Entry**: Add recipient details directly through the app interface.

- **Bulk Upload**: Upload a CSV / JSON / TXT file to generate outreach messages for thousands of recipients.

## 🤖 AI-Powered Personalization

- Powered by openai/gpt-oss-20b model via Groq API

- Each message is dynamically phrased and tone-optimized

- Avoids repetitive or robotic text by varying sentence flow and vocabulary

## 🔁 Feedback & Regeneration

After generating a message, users can choose:

- 👍 Useful / Perfect

- 👎 Not Useful

- 🎯 Try Another Version — instantly generates a new version with a fresh tone or structure

## ✅ Unlimited regeneration supported

- Scalability & Efficiency

- Multi-threaded architecture using ThreadPoolExecutor

- Built-in retry logic and rate-limit backoff

- Handles large datasets efficiently for enterprise-level outreach

## Streamlit Interface

- Clean, intuitive design

- Real-time progress tracking for bulk message generation

- One-click CSV export for use in outreach campaigns

- Field for LinkedIn post/profile text to increase contextual accuracy

## 📁 Files Included  

| **File Name**              | **Description**                                                   |
|:----------------------------|:------------------------------------------------------------------|
| `linkedin_outreach_app.py` | Main Streamlit app for generating personalized LinkedIn messages. |
| `sample_input.csv`         | Example input file containing columns: name, job_role, company, intent, post_text. |
| `requirements.txt`         | List of Python dependencies required to run the project.          |
| `README.md`                | Documentation and usage guide for setup and execution.            |


## ⚙️ Tech Stack

- **Language:** Python 3.10+

- **Framework:** Streamlit

- **API:** Groq (OpenAI-compatible API)

## Libraries:
- requests, pandas, json, dotenv, concurrent.futures, random, time

---
## 🚀 How to Run

- Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

- Set your Groq API key
   ```bash
   setx GROQ_API_KEY "your_api_key_here"
   ```

- (Mac/Linux: export GROQ_API_KEY="your_api_key_here")

- Run the app
   ```bash
   streamlit run linkedin_outreach_app.py
   ```

### **Choose Input Mode**

- Manual Entry – Enter recipient info one by one

- File Upload – Upload CSV/JSON/TXT for bulk generation

### **Generate & Download**

- View generated messages

- Rate or regenerate new versions

- Download final outreach messages as a CSV file

## 📈 Scalability & Reliability

- Multi-threaded execution for parallel processing

- Automatic retry on API timeouts or rate limits

- Dynamic variation to prevent repetitive outputs

- Graceful error handling for incomplete data rows

## 📄 Example Output 

| **Name**       | **Role**          | **Company**  | **Generated Message** |
|:----------------|:------------------|:--------------|:------------------------|
| Amit Sharma    | HR Manager       | TechNova     | Hi Amit, I noticed your recent post on how TechNova is reshaping career paths for junior developers — it sparked ideas about how my background in talent analytics could support your expansion goals. Would be great to connect and chat about it. |
| Priya Desai    | Marketing Head   | BrandBoost   | Hi Priya, your recent post on leadership in tech inspired me — BrandBoost’s approach to creative storytelling perfectly aligns with what I’ve been exploring in digital branding. Would love to exchange ideas sometime. |



## ✅ Project Status

This project is fully functional and production-ready, offering:

- Context-aware AI-generated outreach messages

- Infinite regeneration through user feedback

- Scalable and multi-threaded architecture

- Polished Streamlit interface with CSV export

## 💭 Future Enhancements (Optional Ideas)

- Accept LinkedIn post/profile URLs for live text extraction

- Integrate company website summarization for deeper personalization

- Support OCR extraction from screenshots of LinkedIn posts
