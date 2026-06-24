
import streamlit as st
import pandas as pd

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="AI Test Case Generator", layout="wide")

st.title("🚀 AI Test Case Generator (Teamcenter Ready)")
st.markdown("Generate detailed, module-specific test cases")

# -------------------------------
# Module Options
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
    "Select Test Case Types",
    ["Positive", "Negative", "Edge Case", "Security", "Performance"]
)

num_cases = st.slider("Number of Test Cases", 1, 20, 6)

generate_btn = st.button("Generate Test Cases")

# -------------------------------
# Core Logic
# -------------------------------
def generate_test_cases(module, requirement, conditions, n):

    test_cases = []

    # Module-specific steps
    module_steps = {
        "Item Management": [
            "Login to Teamcenter AWC",
            "Navigate to Item Creation",
            "Enter mandatory attributes",
            "Save item"
        ],
        "Workflow": [
            "Login to Teamcenter",
            "Create workflow process",
            "Attach target object",
            "Start workflow",
            "Complete assigned task"
        ],
        "Change Management": [
            "Create Change Request",
            "Add affected items",
            "Submit for approval",
            "Approve change"
        ],
        "Supplier Collaboration": [
            "Login as Supplier",
            "Access shared object",
            "Download dataset",
            "Upload updated dataset"
        ],
        "Access Control": [
            "Login with specific role",
            "Access restricted object",
            "Attempt modify/delete action"
        ],
        "BOM Management": [
            "Open BOM structure",
            "Add/remove components",
            "Save BOM"
        ]
    }

    base_steps = module_steps.get(module, ["Open system", "Perform action", "Validate result"])

    for i in range(n):

        condition = conditions[i % len(conditions)] if conditions else "Positive"

        # Scenario generation
        if condition == "Positive":
            scenario = f"[{module}] Verify successful execution of: {requirement}"
            expected = "Operation completed successfully with correct data saved"

        elif condition == "Negative":
            scenario = f"[{module}] Validate system behavior with invalid input for: {requirement}"
            expected = "Appropriate error message should be displayed"

        elif condition == "Edge Case":
            scenario = f"[{module}] Validate boundary values and maximum limits for: {requirement}"
            expected = "System should handle edge conditions without failure"

        elif condition == "Security":
            scenario = f"[{module}] Verify role-based access restriction for: {requirement}"
            expected = "Unauthorized users should not be allowed to perform action"

        elif condition == "Performance":
            scenario = f"[{module}] Validate system performance under heavy load for: {requirement}"
            expected = "System should respond within SLA time"

        # Steps generation
        steps = []
        for idx, step in enumerate(base_steps):
            steps.append(f"{idx+1}. {step}")

        # Add condition-specific steps
        if condition == "Negative":
            steps.append(f"{len(steps)+1}. Provide invalid or missing input data")

        if condition == "Security":
            steps.append(f"{len(steps)+1}. Login with unauthorized role")

        if condition == "Performance":
            steps.append(f"{len(steps)+1}. Execute same operation multiple times concurrently")

        # Precondition
        precondition = f"User logged into {module} module with required access"

        test_cases.append({
            "Test Case ID": f"TC_{module[:3].upper()}_{i+1}",
            "Module": module,
            "Condition": condition,
            "Scenario": scenario,
            "Precondition": precondition,
            "Steps": "\n".join(steps),
            "Expected Result": expected,
            "Priority": ["High", "Medium", "Low"][i % 3]
        })

    return pd.DataFrame(test_cases)

# -------------------------------
# UI Output
# -------------------------------
if generate_btn:
    if not requirement.strip():
        st.error("⚠️ Please enter requirement")
    else:
        df = generate_test_cases(selected_module, requirement, conditions, num_cases)

        st.success("✅ Test Cases Generated Successfully")

        st.dataframe(df, use_container_width=True)

        # Download options
        csv = df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="teamcenter_test_cases.csv",
            mime='text/csv'
        )

        # Excel Download
        excel_file = "test_cases.xlsx"
        df.to_excel(excel_file, index=False)

        with open(excel_file, "rb") as f:
            st.download_button(
                label="📥 Download Excel",
                data=f,
                file_name=excel_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
