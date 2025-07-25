# File: dashboard.py

import os
import streamlit as st
import numpy as np
import json
import hashlib
from datetime import datetime
import base64
import pandas as pd
import tenseal as ts

st.set_page_config(page_title="Confidential Student Dashboard", layout="centered")
st.title("🔐 Confidential Student Score Input Dashboard")

BLOCKCHAIN_FILE = "student_chain.json"
SCHOOL_NAME = "Greenfield High"
CONTEXT_FILE = "C:/Users/Hevert/AppData/Local/Programs/Python/Python312/encryption/tenseal_context.tenseal"


# Blockchain Functions

def calculate_hash(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def load_chain():
    if not os.path.exists(BLOCKCHAIN_FILE):
        return []
    with open(BLOCKCHAIN_FILE, "r") as f:
        return json.load(f)

def save_chain(chain):
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=4)

def add_block(student_id, term, data):
    chain = load_chain()
    prev_hash = chain[-1]['hash'] if chain else "0" * 64
    block = {
        "timestamp": str(datetime.utcnow()),
        "student_id": student_id,
        "term": term,
        "data": data,
        "prev_hash": prev_hash
    }
    block['hash'] = calculate_hash(block)
    chain.append(block)
    save_chain(chain)


# HE Context Setup

def get_context():
    with open(CONTEXT_FILE, "rb") as f:
        return ts.context_from(f.read())


# Dashboard Form

st.header("✏️ Enter Student Data")
st.markdown("🔒 **All submissions are encrypted before analysis and blockchain logging.**")

# Use session state to reset inputs after submission
if "submitted_once" not in st.session_state:
    st.session_state.submitted_once = False

with st.form("student_input_form"):
    st.text(f"🏫 School: {SCHOOL_NAME}")
    student_id = st.text_input("🎓 Student ID", "" if st.session_state.submitted_once else "student1")

    terms = ["Term 1", "Term 2"]
    term_scores = {}
    term_engagements = {}

    st.caption("ℹ️ All subject scores are out of **100**.")

    for term in terms:
        st.subheader(f"📅 {term} Scores")
        scores = []
        for i in range(5):
            default_score = 50.0 if not st.session_state.submitted_once else 0.0
            score = st.number_input(f"📚 {term} - Subject {i+1} Score", min_value=0.0, max_value=100.0, value=default_score, key=f"{term}_score_{i}")
            scores.append(score)
        engagement = st.slider(f"🧠 {term} Engagement Level (%)", min_value=0, max_value=100, value=75 if not st.session_state.submitted_once else 0, key=f"{term}_engagement")

        term_scores[term] = scores
        term_engagements[term] = engagement

    submitted = st.form_submit_button("🔍 Analyze and Submit")

if submitted:
    context = get_context()

    for term in terms:
        scores = term_scores[term]
        engagement = term_engagements[term]
        avg_score = round(np.mean(scores), 2)
        engagement_percent = round(engagement, 2)

        st.success(f"✅ {term} Submitted Scores")
        st.write("**Scores:**")
        st.dataframe({"Subject": [f"Subject {i+1}" for i in range(5)], "Score": scores})
        st.write(f"📈 **Average Score**: {avg_score}")
        st.write(f"🧠 **Engagement Level**: {engagement_percent}%")
        st.bar_chart(scores)

        # Risk Assessment
        risk_label = ""
        risk_color = ""
        risk_reason = ""

        if avg_score < 50 and engagement_percent < 60:
            risk_label = "High Risk"
            risk_color = "🔴"
            risk_reason = "Low average and poor engagement."
        elif avg_score < 60 or engagement_percent < 70:
            risk_label = "Medium Risk"
            risk_color = "🟠"
            risk_reason = "Moderate academic or engagement issues observed."
        else:
            risk_label = "Low Risk"
            risk_color = "🟢"
            if avg_score >= 70 and engagement_percent >= 80:
                risk_reason = "Good performance and strong engagement."
            elif avg_score >= 70:
                risk_reason = "Above-average academic performance."
            elif engagement_percent >= 80:
                risk_reason = "Highly engaged student."
            else:
                risk_reason = "No significant academic or behavioral concern."

        st.warning(f"⚠️ **Risk Assessment ({term})**: {risk_color} {risk_label}")
        st.info(f"📝 *Reason*: {risk_reason}")

        enc_vector = ts.ckks_vector(context, scores)
        encrypted_bytes = enc_vector.serialize()
        encoded = base64.b64encode(encrypted_bytes).decode()
        student_data = {
            "scores": encoded,
            "average_score": avg_score,
            "engagement": engagement_percent,
            "risk": risk_label,
            "reason": risk_reason
        }

        add_block(student_id, term, student_data)

    st.success("📦 **Student data for both terms encrypted and recorded in blockchain log.**")
    st.caption("🔐 Note: This submission is permanently recorded on the blockchain (secure, tamper-proof log). View full log using `blockchain_viewer.py`.")
    st.session_state.submitted_once = True


# Student Progress Viewer

st.header("📊 View Student Progress")
st.markdown("Compare how a student's scores and risk level changed over time.")

chain = load_chain()
all_ids = sorted(set(block.get('student_id') for block in chain if 'student_id' in block))
if all_ids:
    selected_id = st.selectbox("🔎 Select Student ID", all_ids)
    student_blocks = [b for b in chain if b.get('student_id') == selected_id]

    if student_blocks:
        student_blocks.sort(key=lambda b: b['term'])
        terms = [b['term'] for b in student_blocks]
        averages = [b['data']['average_score'] for b in student_blocks]
        engagement = [b['data']['engagement'] for b in student_blocks]
        risks = [b['data']['risk'] for b in student_blocks]

        st.subheader(f"📈 Average Scores Over Time for {selected_id}")
        avg_df = pd.DataFrame({"Term": terms, "Average Score": averages}).set_index("Term")
        st.line_chart(avg_df)

        st.subheader(f"🧠 Engagement Trends")
        eng_df = pd.DataFrame({"Term": terms, "Engagement (%)": engagement}).set_index("Term")
        st.line_chart(eng_df)

        st.subheader(f"⚠️ Risk Levels Per Term")
        risk_details = [
            {
                "Term": block["term"],
                "Risk Level": block["data"]["risk"],
                "Icon": "🟢" if block["data"]["risk"] == "Low Risk" else "🟠" if block["data"]["risk"] == "Medium Risk" else "🔴",
                "Reason": block["data"]["reason"]
            }
            for block in student_blocks
        ]
        risk_df = pd.DataFrame(risk_details)
        st.dataframe(risk_df)

        # Compute average risk level
        risk_score_map = {"Low Risk": 1, "Medium Risk": 2, "High Risk": 3}
        numeric_scores = [risk_score_map.get(risk, 0) for risk in risks]

        if numeric_scores:
            avg_score = round(sum(numeric_scores) / len(numeric_scores), 2)

            if avg_score < 1.5:
                overall_risk = "🟢 Low Risk"
            elif avg_score < 2.5:
                overall_risk = "🟠 Medium Risk"
            else:
                overall_risk = "🔴 High Risk"

            st.subheader("📊 Overall Risk Level Across Terms")
            st.info(f"**{overall_risk}** (based on average across all terms)")
else:
    st.info("No student data available yet. Please submit entries first.")
