
import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Teamcenter Test Generator", layout="wide")

# ---------------- MODULES ----------------
modules = [
    "Workflow",
    "Item Management",
    "BOM Management",
    "Change Management",
    "Dataset Management",
    "Access Control",
    "Supplier Collaboration"
]

# ---------------- SESSION STATE ----------------
if "test_cases" not in st.session_state:
    st.session_state.test_cases = []

# ---------------- FUNCTION ----------------
def generate_test_cases(input_text, selected_modules):
    text = input_text.lower()
    generated = []

    for module in selected_modules:

        # Generic Case
        generated.append({
            "Title": f"{module} - Basic Validation",
            "Steps": [
                "Login to Teamcenter",
                f"Navigate to {module}",
                "Perform operation",
                "Validate outcome"
            ],
            "Expected": "System works correctly"
        })

        # Workflow detailed case (your real example)
        if module == "Workflow":
            generated.append({
                "Title": "Prototype Release Validation - DR Workflow",
                "Steps": [
                    "Use required TTT DR number (e.g., DR00000****)",
                    "Go to BW Properties tab and confirm Target Release Status = Prototype",
                    "Click More Commands → Edit → Set Sync Prototype to SAP = NO",
                    "Navigate to Attachments tab → Add required Solution items",
                    "Ensure all items have TTT Product Family attribute",
                    "Submit to Workflow → QA_TTT_Design",
                    "Complete Workflow",
                    "Verify Prototype status applied to all Solution objects",
                    "Ensure SAP workflow NOT triggered and DR closed"
                ],
                "Expected": "Prototype release without SAP transfer"
            })

    return generated


# ---------------- UI ----------------
st.title("🚀 Teamcenter Test Case Generator")

selected_modules = st.multiselect("Select Modules", modules)
requirement = st.text_area("Enter Requirement")

# Screenshot Upload
uploaded_file = st.file_uploader("Upload Screenshot (Optional)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Screenshot", use_column_width=True)

# Generate
if st.button("Generate Test Cases"):
    if requirement and selected_modules:
        st.session_state.test_cases = generate_test_cases(requirement, selected_modules)

# ---------------- DISPLAY ----------------
if st.session_state.test_cases:

    st.subheader("📝 Generated Test Cases")

    all_rows = []

    for idx, tc in enumerate(st.session_state.test_cases):

        st.markdown(f"### {tc['Title']}")

        # Table format
        table_data = []
        for i, step in enumerate(tc["Steps"], start=1):
            table_data.append({
                "S.No": i,
                "High Level Validation Steps": step
            })

            all_rows.append({
                "Test Case": tc["Title"],
                "S.No": i,
                "Step": step,
                "Expected": tc["Expected"]
            })

        df = pd.DataFrame(table_data)
        st.table(df)

        st.write(f"✅ Expected: {tc['Expected']}")
        st.markdown("---")

    # ---------------- CSV EXPORT ----------------
    export_df = pd.DataFrame(all_rows)

    csv = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="test_cases.csv",
        mime="text/csv"
    )
