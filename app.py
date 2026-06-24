
import streamlit as st
import pandas as pd
import openai

# ---------------- CONFIG ----------------
openai.api_key = "YOUR_OPENAI_API_KEY"

st.set_page_config(page_title="AI Test Case Generator", layout="wide")

modules = [
    "Workflow",
    "Item Management",
    "BOM Management",
    "Change Management",
    "Dataset Management",
    "Access Control",
    "Supplier Collaboration"
]

# ---------------- SESSION ----------------
if "test_cases" not in st.session_state:
    st.session_state.test_cases = []

# ---------------- AI FUNCTION ----------------
def generate_ai_test_cases(requirement, modules):

    prompt = f"""
You are a Teamcenter QA expert.

Requirement:
{requirement}

Modules:
{modules}

Generate test cases in this format:

- Title
- Steps (numbered)
- Expected Result

Make steps detailed and realistic for Teamcenter workflows.

Return output in structured format.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]


# ---------------- PARSER ----------------
def parse_ai_output(text):
    test_cases = []
    lines = text.split("\n")

    current = None

    for line in lines:
        line = line.strip()

        if line.lower().startswith("title"):
            if current:
                test_cases.append(current)

            current = {
                "title": line.replace("Title:", "").strip(),
                "steps": [],
                "expected": ""
            }

        elif line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
            current["steps"].append(line)

        elif "expected" in line.lower():
            current["expected"] = line

    if current:
        test_cases.append(current)

    return test_cases


# ---------------- UI ----------------
st.title("🚀 AI Teamcenter Test Case Generator")

selected_modules = st.multiselect("Select Modules", modules)
requirement = st.text_area("Enter Requirement")

# Screenshot
uploaded_file = st.file_uploader("Upload Screenshot (Optional)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Reference Screenshot")

# Generate AI
if st.button("Generate AI Test Cases"):
    if requirement and selected_modules:
        with st.spinner("AI generating test cases..."):
            ai_output = generate_ai_test_cases(requirement, selected_modules)
            parsed = parse_ai_output(ai_output)

            st.session_state.test_cases = parsed


# ---------------- DISPLAY ----------------
if st.session_state.test_cases:
    st.subheader("📝 AI Generated Test Cases")

    export_rows = []

    for tc in st.session_state.test_cases:

        st.markdown(f"### {tc['title']}")

        table_data = []

        for i, step in enumerate(tc["steps"], start=1):
            table_data.append({
                "S.No": i,
                "High Level Validation Steps": step
            })

            export_rows.append({
                "Test Case": tc["title"],
                "S.No": i,
                "Step": step,
                "Expected": tc["expected"]
            })

        df = pd.DataFrame(table_data)
        st.table(df)

        st.write(f"✅ Expected: {tc['expected']}")
        st.markdown("---")

    # CSV DOWNLOAD
    export_df = pd.DataFrame(export_rows)

    csv = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download CSV",
        data=csv,
        file_name="ai_test_cases.csv",
        mime="text/csv"
    )
``
