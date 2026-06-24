
import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Teamcenter Test Generator", layout="wide")

modules = [
    "Workflow",
    "Item Management",
    "BOM Management",
    "Change Management",
    "Dataset Management",
    "Access Control",
    "Supplier Collaboration"
]

if "test_cases" not in st.session_state:
    st.session_state.test_cases = []

def generate_test_cases(input_text, selected_modules):
    text = input_text.lower()
    generated = []

    for module in selected_modules:
        generated.append({
            "ID": f"TC_{int(time.time())}",
            "Module": module,
            "Title": f"{module} - Basic Validation",
            "Steps": "Login -> Navigate -> Perform -> Validate",
            "Expected": "Success",
            "Priority": "High",
            "Status": "Not Run"
        })

        if module == "Workflow":
            generated.append({
                "ID": f"TC_{int(time.time())}",
                "Module": module,
                "Title": "Workflow Initiation",
                "Steps": "Start Workflow -> Verify",
                "Expected": "Workflow started",
                "Priority": "High",
                "Status": "Not Run"
            })

            if "approval" in text:
                generated.append({
                    "ID": f"TC_{int(time.time())}",
                    "Module": module,
                    "Title": "Approval Flow",
                    "Steps": "Approve Task -> Verify",
                    "Expected": "Moves forward",
                    "Priority": "High",
                    "Status": "Not Run"
                })

            if "rejection" in text:
                generated.append({
                    "ID": f"TC_{int(time.time())}",
                    "Module": module,
                    "Title": "Rejection Flow",
                    "Steps": "Reject Task -> Rollback",
                    "Expected": "Returns to initiator",
                    "Priority": "Medium",
                    "Status": "Not Run"
                })

    return generated

# UI
st.title("🚀 Teamcenter Test Case Generator")

selected_modules = st.multiselect("Select Modules", modules)
requirement = st.text_area("Enter Requirement")

if st.button("Generate Test Cases"):
    if requirement and selected_modules:
        st.session_state.test_cases = generate_test_cases(requirement, selected_modules)

# Display
if st.session_state.test_cases:
    df = pd.DataFrame(st.session_state.test_cases)

    st.subheader("📊 Dashboard")
    pass_count = len(df[df["Status"] == "Pass"])
    fail_count = len(df[df["Status"] == "Fail"])
    not_run = len(df) - pass_count - fail_count

    st.write(f"✅ Passed: {pass_count}")
    st.write(f"❌ Failed: {fail_count}")
    st.write(f"🟡 Not Run: {not_run}")

    st.subheader("📝 Test Cases")

    for i, row in df.iterrows():
        col1, col2 = st.columns([3,1])

        with col1:
            st.write(f"**{row['Title']}**")
            st.write(f"Module: {row['Module']}")
            st.write(f"Steps: {row['Steps']}")
            st.write(f"Expected: {row['Expected']}")
            st.write(f"Status: {row['Status']}")

        with col2:
            if st.button(f"Pass {i}"):
                st.session_state.test_cases[i]["Status"] = "Pass"
            if st.button(f"Fail {i}"):
                st.session_state.test_cases[i]["Status"] = "Fail"

    st.subheader("⬇️ Export")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "test_cases.csv", "text/csv")
