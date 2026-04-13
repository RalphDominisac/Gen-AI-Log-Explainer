import streamlit as st
import re
import time
from analyzer import analyze_logs
from db import fetch_logs
from db import save_log

@st.cache_data(show_spinner=False)
def cached_analysis(logs):
    return analyze_logs(logs)

if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0


def parse_output(text):
    sections = {
        "Summary": "",
        "Root Cause": "",
        "Suggested Fix": "",
        "Severity": ""
    }

    current = None

    for line in text.splitlines():
        line = line.strip()

        if "Summary" in line:
            current = "Summary"
            sections[current] = line.split(":",1)[-1].strip()
            continue

        elif "Root Cause" in line:
            current = "Root Cause"
            sections[current] = line.split(":",1)[-1].strip()
            continue

        elif "Suggested Fix" in line:
            current = "Suggested Fix"
            sections[current] = line.split(":",1)[-1].strip()
            continue

        elif "Severity" in line:
            current = "Severity"
            sections[current] = line.split(":",1)[-1].strip()
            continue

        elif current:
            sections[current] = (sections[current] + " " + line).strip()
        
    return sections


st.set_page_config(page_title="AI Log Explainer")

st.title("🧠 AI Log Explainer")

st.markdown("""
<style>
button[kind="primary"] {
    background-color: #4CAF50 !important;
    border: none !important;
    color: white !important;
}

button[kind="primary"]:hover {
    background-color: #45a049 !important;
}
</style>
""", unsafe_allow_html=True)


logs = st.text_area("Paste logs here", height=250)


col1, col2, col3 = st.columns([1.2, 2.5, 1.2])

with col2:
    btn1, spacer, btn2 = st.columns([1, 0.4, 1])

    with btn1:
        analyze_clicked = st.button(
        "Analyze",
        use_container_width=True,
        type="primary",
        disabled=not logs.strip()
    )

    with btn2:
        history_clicked = st.button(
        "View History",
        use_container_width=True
    )

if analyze_clicked:
    
    # ✅ Rate limit ONLY when analyzing
    current_time = time.time()

    if current_time - st.session_state.last_request_time < 3:
        st.warning("⏳ Please wait before sending another request.")
        st.stop()
    
    st.session_state.last_request_time = current_time

    logs = logs.strip()

    # Limit size (prevent abuse / cost explosion)
    MAX_LOG_LENGTH = 2000
    logs = logs[:MAX_LOG_LENGTH]

    # Basic sanitization
    logs = logs.replace("\x00", "")

    if logs:
        status = st.empty()
        status.info("🔄 Sending logs to AI model...")

        start = time.time()
        result = cached_analysis(logs)
        end = time.time()

        status.success("✅ Analysis complete")
        st.caption(f"⏱ Took {round(end - start, 2)} seconds")

        st.markdown("##")   
        st.markdown("### 🔍 Results")

        # ✅ SYSTEM STATUS
        keywords = ["error", "fail", "critical", "exception", "warn", "fatal"]
        detected = list(set(k for k in keywords if k in logs.lower()))

        if detected:
            st.error(f"🚨 System Status: Issues detected ({', '.join(detected)})")
        else:
            st.success("✅ System Status: Healthy")

        # ✅ Parse AFTER result is generated
        parsed = parse_output(result)

        # ✅ FALLBACK AFTER PARSING
        if not parsed["Summary"]:
            parsed["Summary"] = "No summary generated."

        if not parsed["Root Cause"]:
            parsed["Root Cause"] = "Root cause not identified."

        if not parsed["Suggested Fix"]:
            parsed["Suggested Fix"] = "No fixes generated."

        if not parsed["Severity"]:
            parsed["Severity"] = ""

        # ✅ Structured Display (same as View History)
        st.subheader("🧾 Summary")
        st.write(parsed["Summary"] or "No significant issues detected.")

        st.divider()  

        st.subheader("🧠 Root Cause")
        st.write(parsed["Root Cause"])

        st.divider()  

        st.subheader("🛠 Suggested Fix")

        fix_text = parsed["Suggested Fix"]

        steps = re.split(r'\d+\.\s+', fix_text)
        steps = [s.strip() for s in steps if s.strip()]

        if len(steps) == 1:
            steps = re.split(r'\.\s+', fix_text)
            steps = [s.strip() for s in steps if s.strip()]

        for i, step in enumerate(steps, 1):
            step = step.rstrip(".")

            with st.container():
                st.markdown(f"**🔧 Step {i}**")
                st.write(step)

            if i < len(steps):  # ✅ prevents extra divider
                st.markdown("---")

        # ✅ SAFETY SEVERITY FALLBACK
        severity = parsed["Severity"].strip().upper()

        if not severity:
            if "error" in logs.lower() or "fatal" in logs.lower():
                severity = "HIGH"
            elif "warn" in logs.lower():
                severity = "MEDIUM"
            else:
                severity = "LOW"

        # ✅ DISPLAY
        if "HIGH" in severity:
            st.error("🚨 HIGH SEVERITY")
        elif "MEDIUM" in severity:
            st.warning("⚠️ MEDIUM SEVERITY")
        else:
            st.success("✅ LOW SEVERITY")

        # ✅ Save to DB
        try:
            save_log(logs, result)
            st.success("Saved to database ✅")
            st.markdown("---")
        except Exception as e:
            print(f"DB ERROR: {e}")  # internal only
            st.error("Database connection issue. Please try again.")

if history_clicked:
    rows = fetch_logs(limit=3)

    st.markdown("## 📊 Recent Analysis History")

    for row in rows:
        log_text = row[1]
        analysis = row[2]
        timestamp = row[3]

        parsed = parse_output(analysis)

        st.markdown("---")
        st.markdown(f"### 🕒 {timestamp}")

        st.code(log_text[:500])

        st.subheader("🧾 Summary")
        st.write(parsed["Summary"] or "No significant issues detected.")

        st.divider()  # 

        st.subheader("🧠 Root Cause")
        st.write(parsed["Root Cause"])

        st.divider()  # 

        st.subheader("🛠 Suggested Fix")


        fix_text = parsed["Suggested Fix"]

        # Splitting by numbered steps
        steps = re.split(r'\d+\.\s+', fix_text)
        steps = [s.strip() for s in steps if s.strip()]

        # Fallback: split by sentences if only one step
        if len(steps) == 1:
            steps = re.split(r'\.\s+', fix_text)
            steps = [s.strip() for s in steps if s.strip()]

        # Display
        for i, step in enumerate(steps, 1):
            step = step.rstrip(".")

            with st.container():
                st.markdown(f"**🔧 Step {i}**")
                st.write(step)

            if i < len(steps):  # Prevents extra divider
                st.markdown("---")


        severity = parsed["Severity"].strip().upper()

        if not severity:
            if "error" in log_text.lower() or "fatal" in log_text.lower():
                severity = "HIGH"
            elif "warn" in log_text.lower():
                severity = "MEDIUM"
            else:
                severity = "LOW"

        if "HIGH" in severity:
            st.error(f"🚨 HIGH SEVERITY")
        elif "MEDIUM" in severity:
            st.warning(f"⚠️ MEDIUM SEVERITY")
        else:
            st.success(f"✅ LOW SEVERITY")
