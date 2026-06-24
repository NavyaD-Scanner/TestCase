
import streamlit as st
import pandas as pd

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Test Case Generator", layout="wide")

st.title("🚀 AI Test Case Generator (Teamcenter Modules)")
st.markdown("Generate structured test cases based on requirements")

# -------------------------------
# Inputs
# -------------------------------
modules = [
    "Item Management",
    "Workflow",
    "Change Management",
    "Supplier Collaboration",
    "Access Control",
    "BOM Management"
]

selected_module = st.selectbox("Select Module", modules)

requirement = st.text_area("Enter Requirement", height=150)

conditions = st.multiselect(
    "Select Conditions",
    ["Positive", "Negative", "Edge Case", "Security", "Performance"]
)

num_cases = st.slider("Number of Test Cases", 1, 10, 5)

generate_btn = st.button("Generate Test Cases")

# -------------------------------
# Logic
# -------------------------------
def generate_test_cases(module, requirement, conditions, n):
    test_cases = []

    for i in range(1, n + 1):
        condition = conditions[i % len(conditions)] if conditions else "General"

        test_cases.append({
            "Test Case ID": f"TC_{module[:3].upper()}_{i}",
            "Module": module,
            "Scenario": f"{condition} scenario for {requirement[:40]}",
            "Precondition": f"User logged into {module}",
            "Steps": f"1. Open {module}\n2. Perform action\n3. Validate result",
            "Expected Result": f"System behaves correctly under {condition} condition",
            "Priority": ["High", "Medium", "Low"][i % 3]
        })

    return pd.DataFrame(test_cases)

# -------------------------------
# Output
# -------------------------------
if generate_btn:
    if not requirement.strip():
        st.error("Please enter requirement")
    else:
        df = generate_test_cases(selected_module, requirement, conditions, num_cases)

        st.success("✅ Test Cases Generated!")

        st.dataframe(df, use_container_width=True)

        # Download option
        csv = df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="test_cases.csv",
            mime='text/csv'
        )
``
