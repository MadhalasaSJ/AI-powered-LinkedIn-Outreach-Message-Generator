import streamlit as st
import pandas as pd
import json
import random
import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

# ----------------------------------------------------------
# ⚙️ Config
# ----------------------------------------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/responses"

st.set_page_config(page_title="LinkedIn Outreach Generator", layout="centered")
st.title("💬 Human-Style LinkedIn Outreach Generator (Groq-Powered)")

# ----------------------------------------------------------
# 🧠 Robust Groq API Handler
# ----------------------------------------------------------
def groq_generate(prompt, temperature=0.9, retries=3):
    """Generate AI message with retries & safety checks."""
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

    for attempt in range(retries):
        try:
            payload = {
                "model": "openai/gpt-oss-20b",
                "input": prompt,
                "temperature": temperature + random.uniform(-0.05, 0.05),
                "max_output_tokens": 550,
            }

            r = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            if r.status_code != 200:
                time.sleep(2)
                continue

            data = r.json()
            message_text = ""
            for item in data.get("output", []):
                if item.get("type") == "message":
                    for c in item.get("content", []):
                        if c.get("type") == "output_text":
                            message_text += c.get("text", "")

            message_text = (
                message_text.replace("—", "-")
                .replace("–", "-")
                .replace("…", ".")
                .strip()
                .strip('"')
            )

            if len(message_text) < 30:
                continue
            if not message_text.endswith((".", "!", "?")):
                message_text += "."
            return message_text

        except Exception:
            time.sleep(1.5)
            continue

    return "(No message generated after retries.)"


# ----------------------------------------------------------
# 🧩 Message Logic (uses post/profile context)
# ----------------------------------------------------------
def generate_ai_message(name, role, company, intent, post_text=None, sender_perspective="job applicant"):
    """Generate human, contextual LinkedIn messages with logical tone awareness and sender perspective."""

    # Detect post type — whether it's a hiring/recruitment post
    post_context_type = "general"
    if post_text:
        text_lower = post_text.lower()
        if any(keyword in text_lower for keyword in ["hiring", "recruiting", "join our team", "apply", "intern", "open position", "job opportunity"]):
            post_context_type = "hiring_post"

    # Randomized natural variations
    sample_topics = [
        "leadership in tech", "AI innovation", "team culture", "marketing strategy",
        "career growth", "product design", "creative storytelling",
        "customer engagement", "data-driven insights"
    ]
    topic = random.choice(sample_topics)

    openings = [
        f"Hi {name},", f"Hey {name},", f"Hello {name},", f"Hi there {name},", f"Good day {name},"
    ]
    closings = [
        "Would love to exchange ideas sometime.",
        "Maybe we could set up a short chat soon.",
        "Hope we can connect and share thoughts.",
        "Looking forward to staying in touch.",
        "Would be great to learn more about your work.",
        "Let’s stay connected and exchange ideas."
    ]

    tone_prompts = {
        "hiring": "You're a recruiter reaching out regarding hiring or career opportunities.",
        "marketing": "You're initiating a friendly marketing or brand partnership outreach.",
        "sales": "You're introducing a product or service that could support their goals.",
        "partnership": "You're exploring a potential business partnership or collaboration.",
        "networking": "You're building your professional network through shared interests.",
        "collaboration": "You're looking to collaborate on projects or research ideas.",
        "default": "You're sending a warm, professional connection message."
    }
    context = tone_prompts.get(intent.lower(), tone_prompts["default"])

    # 👤 Sender perspective logic
    perspective_contexts = {
        "job applicant": "You are reaching out as a potential applicant, responding to a job or research post. Be polite, professional, and express genuine interest in their work.",
        "recruiter": "You are reaching out as a recruiter, introducing an opportunity or expressing interest in the recipient’s expertise.",
        "peer": "You are reaching out as a fellow professional or researcher to connect and discuss shared topics of interest.",
        "networker": "You are simply reaching out to connect professionally and exchange perspectives.",
    }
    sender_context = perspective_contexts.get(sender_perspective.lower(), perspective_contexts["networker"])

    # Include LinkedIn post context if provided
    if post_text:
        snippet = post_text.strip()
        if len(snippet) > 400:
            snippet = snippet[:400] + "..."
        post_context = f"\nHere’s the content from their LinkedIn post or profile:\n\"{snippet}\"\n"
    else:
        post_context = f"\nMention something relevant to {topic} naturally.\n"

    # --- Adaptive framing depending on post type and sender role ---
    if post_context_type == "hiring_post" and sender_perspective == "job applicant":
        role_context = (
            "\nThe post is about a hiring opportunity. Frame your message as a polite, professional applicant "
            "expressing interest in their work or team, not just the job itself."
        )
    elif post_context_type == "hiring_post" and sender_perspective != "job applicant":
        role_context = (
            "\nThe post is a hiring announcement, but you are not applying. Acknowledge their hiring initiative "
            "respectfully and connect based on shared expertise or goals."
        )
    else:
        role_context = "\nThe post seems general — focus on shared professional insights or achievements."

    # Final prompt assembly
    opener, closer = random.choice(openings), random.choice(closings)
    prompt = f"""
You are crafting a personalized LinkedIn outreach message (2–3 sentences).
{context}
{sender_context}
{role_context}

Keep the message natural, logical, and aligned with {company}'s domain.
Avoid robotic phrases like "great insights" or "I was impressed by".
Write in a conversational, respectful tone.

{post_context}
Start with: {opener}
End with: {closer}

Output only the final outreach message text.
"""
    return groq_generate(prompt)

# ----------------------------------------------------------
# 🧩 Batch Processor
# ----------------------------------------------------------
def process_chunk(df_chunk):
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(
                generate_ai_message,
                row["name"], row["job_role"], row["company"], row["intent"], row.get("post_or_profile", None)
            ): idx
            for idx, row in df_chunk.iterrows()
        }
        for future in as_completed(futures):
            idx = futures[future]
            try:
                results.append((idx, future.result()))
            except Exception as e:
                results.append((idx, f"(Error: {e})"))
    return results


# ----------------------------------------------------------
# 🎯 Streamlit UI
# ----------------------------------------------------------
st.markdown("### 🧩 Provide Details or Upload File")
input_mode = st.radio("Choose input method:", ["Manual Entry", "Upload File (CSV / JSON / TXT)"])

# MANUAL ENTRY
if input_mode == "Manual Entry":
    name = st.text_input("Recipient Name", placeholder="e.g., Priya Desai")
    role = st.text_input("Recipient Role / Title", placeholder="e.g., Marketing Head")
    company = st.text_input("Recipient Company", placeholder="e.g., BrandBoost")
    intent = st.selectbox(
        "Purpose of Outreach",
        ["hiring", "marketing", "sales", "partnership", "networking", "collaboration", "default"],
    )

    # Optional LinkedIn post/profile text
    post_or_profile_input = st.text_area(
        "Post or profile text (paste the LinkedIn post OR About/Profile text for deeper personalization):",
        placeholder="Example: “At Autodesk, we’re driving the future of design and manufacturing through AI-powered workflows...”",
        height=140,
    )

    post_or_profile = post_or_profile_input.strip() or None

    # Initialize session states for messages
    if "generated_message" not in st.session_state:
        st.session_state.generated_message = None
    if "alternate_message" not in st.session_state:
        st.session_state.alternate_message = None

    # Generate button
    if st.button("✨ Generate Message"):
        if all([name, role, company]):
            with st.spinner("Crafting your personalized LinkedIn message..."):
                st.session_state.generated_message = generate_ai_message(
                    name, role, company, intent, post_or_profile
                )
                st.session_state.alternate_message = None
        else:
            st.warning("Please complete all fields first.")

    # Display the generated message (if available)
    if st.session_state.generated_message:
        st.success("✅ Message Generated:")
        st.write(st.session_state.generated_message)

        # Feedback section
        feedback = st.radio(
            "What do you think?",
            ["👍 Useful", "👎 Not useful", "🎯 Try another version"],
            index=None,
            horizontal=True,
            key="feedback_radio",
        )

        # Handle user feedback
        if feedback == "👍 Useful":
            st.success("✅ Thank you for your feedback! Glad it was useful.")
        elif feedback == "👎 Not useful":
            st.warning("⚠️ Thank you for your feedback! If you’d like, click on '🎯 Try another version' to improve it.")
        elif feedback == "🎯 Try another version":
            with st.spinner("Generating another variation..."):
                st.session_state.alternate_message = generate_ai_message(
                    name, role, company, intent, post_or_profile
                )
            st.info("Here’s another version:")
            st.write(st.session_state.alternate_message)


# BULK UPLOAD
else:
    uploaded_file = st.file_uploader("📤 Upload File", type=["csv", "json", "txt"])
    if uploaded_file:
        # Load file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".json"):
            df = pd.DataFrame(json.load(uploaded_file))
        else:
            lines = uploaded_file.read().decode("utf-8").strip().split("\n")
            df = pd.DataFrame([l.split(",") for l in lines],
                              columns=["name", "job_role", "company", "intent", "post_or_profile"])

        # Validate required columns
        required_cols = {"name", "job_role", "company", "intent", "post_or_profile"}
        missing = required_cols - set(df.columns.str.lower())
        # Normalize column names to lower for safety
        df.columns = [c.lower() for c in df.columns]

        if not required_cols.issubset(set(df.columns)):
            st.error(
                "❌ CSV must include columns: "
                "`name, job_role, company, intent, post_or_profile`.\n\n"
                "Tip: Put either the LinkedIn post text or the profile/About text inside `post_or_profile` "
                "so the messages are truly personalized."
            )
        else:
            st.write(f"📄 Loaded {len(df)} rows.")
            chunk_size = 20
            all_results = []

            with st.spinner("⚙️ Generating messages in batches..."):
                for i in range(0, len(df), chunk_size):
                    chunk = df.iloc[i:i + chunk_size]
                    results = process_chunk(chunk)
                    all_results.extend(results)
                    st.progress(min((i + chunk_size) / len(df), 1.0))

            for idx, message in all_results:
                df.loc[idx, "generated_message"] = message

            st.success("✅ All messages generated successfully!")
            st.dataframe(df.head(20))
            st.download_button(
                "📥 Download Messages CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="linkedin_outreach_messages.csv",
                mime="text/csv",
            )
    else:
        st.info("Please upload a CSV, JSON, or TXT file to continue.")
