import google.generativeai as genai
import os


def analyze_logs(log_text):
    try:
        # ✅ Correct API key usage
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        genai.configure(api_key=api_key)

        # ✅ Initialize model INSIDE function (prevents startup blocking)
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
You are a senior DevOps engineer.

Analyze the logs carefully.

STRICT RULES:
- Treat WARN as an issue
- Treat memory/CPU >80% as a problem
- NEVER say "No significant issues" if WARN, ERROR, or abnormal values exist
- ALWAYS fill ALL sections

Respond EXACTLY in this format:

Summary:
<one concise paragraph>

Root Cause:
<clear explanation>

Suggested Fix:
1. <step one>
2. <step two>
3. <step three>

Severity:
<LOW or MEDIUM or HIGH>

Logs:
{log_text}
"""

        response = model.generate_content(prompt)

        # ✅ Safe return
        return response.text if response.text else "No response from AI."

    except Exception as e:
        return """Summary:
                Failed to analyze logs due to an internal error.

                Root Cause:
                AI model request failed or returned an error.

                Suggested Fix:
                1. Retry the request.
                2. Check API key configuration.
                3. Ensure network connectivity.

                Severity:
                MEDIUM
                """