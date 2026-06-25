
import streamlit as st
import pandas as pd
from io import BytesIO

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Enterprise Test Case Generator", layout="wide")

st.title("🚀 Enterprise AI Test Case Generator (Teamcenter)")
st.markdown("Generate consulting-level structured test cases")

# -------------------------------
# Input Section
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
# AI-like Requirement Parser
# -------------------------------
def parse_requirement(requirement):
    req = requirement.lower()
    return {
        "has_workflow": "workflow" in req or "approve" in req,
        "has_dataset": "dataset" in req or "file" in req,
        "has_item": "item" in req,
        "has_bom": "bom" in req or "structure" in req,
        "has_release": "release" in req or "status" in req,
    }

# -------------------------------
# Core Generator (Enterprise Logic)
# -------------------------------
def generate_test_cases(module, requirement, conditions, n):

    parsed = parse_requirement(requirement)
    test_cases = []

    for i in range(n):

        condition = conditions[i % len(conditions)] if conditions else "Positive"

        scenario = f"[{module}] {condition} scenario: {requirement}"

        precondition = """User logged into Teamcenter AWC
User has correct role (Engineer/Reviewer)
Required objects exist in system"""

        steps = ["1. Login to Teamcenter Active Workspace (AWC)"]
        step_no = 2

        # ---------------- ITEM ----------------
        if parsed["has_item"]:
            steps.append(f"{step_no}. Search and open Item")
            step_no += 1

        # ---------------- DATASET ----------------
        if parsed["has_dataset"]:
            steps.extend([
                f"{step_no}. Navigate to Dataset tab",
                f"{step_no+1}. Upload dataset file",
                f"{step_no+2}. Validate named references"
            ])
            step_no += 3

        # ---------------- WORKFLOW (EPM) ----------------
        if parsed["has_workflow"]:
            steps.extend([
                f"{step_no}. Open Workflow tab",
                f"{step_no+1}. Click 'Start Workflow'",
                f"{step_no+2}. Select workflow template",
                f"{step_no+3}. Assign signoff users",
                f"{step_no+4}. Submit workflow",
                f"{step_no+5}. Open Inbox",
                f"{step_no+6}. Execute EPMDoTask",
                f"{step_no+7}. Approve task"
            ])
            step_no += 8

            if condition == "Negative":
                steps.extend([
                    f"{step_no}. Reject task",
                    f"{step_no+1}. Verify workflow loops back"
                ])
                step_no += 2

        # ---------------- BOM ----------------
        if parsed["has_bom"]:
            steps.extend([
                f"{step_no}. Open Structure Manager",
                f"{step_no+1}. Expand BOM",
                f"{step_no+2}. Apply Revision Rule (Latest)",
                f"{step_no+3}. Modify components",
                f"{step_no+4}. Save BOM",
                f"{step_no+5}. Verify revision"
            ])
            step_no += 6

        # ---------------- RELEASE ----------------
        if parsed["has_release"]:
            steps.extend([
                f"{step_no}. Check release status",
                f"{step_no+1}. Promote lifecycle state",
                f"{step_no+2}. Verify status change"
            ])
            step_no += 3

        # ---------------- CONDITIONS ----------------
        if condition == "Security":
            steps.extend([
                f"{step_no}. Login with unauthorized user",
                f"{step_no+1}. Try restricted access",
                f"{step_no+2}. Verify access denied"
            ])
            step_no += 3

        elif condition == "Performance":
            steps.extend([
                f"{step_no}. Perform repeated operations",
                f"{step_no+1}. Monitor response time"
            ])
            step_no += 2

        elif condition == "Edge Case":
            steps.extend([
                f"{step_no}. Use boundary inputs",
                f"{step_no+1}. Validate system handling"
            ])
            step_no += 2

        # ---------------- OUTPUT FIELDS ----------------
        expected = """System should:
- Execute workflow correctly
- Maintain data integrity
- Handle failures gracefully
- Update lifecycle and revision properly"""

        test_data = f"""Item ID: TC_ITEM_{i}
Dataset: sample.pdf
Workflow: Standard Approval
Revision Rule: Latest Working
User Role: Engineer"""

        priority = "High" if condition in ["Negative", "Security"] else "Medium"

        test_cases.append({
            "Test Case ID": f"TC_{i+1:03}",
            "Module": module,
            "Condition": condition,
            "Scenario": scenario,
            "Precondition": precondition,
            "Steps": "\n".join(steps),
            "Test Data": test_data,
            "Expected Result": expected,
            "Priority": priority
        })

    return pd.DataFrame(test_cases)

# -------------------------------
# Output Section
# -------------------------------
if generate_btn:
    if not requirement.strip():
        st.error("⚠️ Please enter a requirement")
    else:
        df = generate_test_cases(selected_module, requirement, conditions, num_cases)

        st.success("✅ Test Cases Generated Successfully")
        st.dataframe(df, use_container_width=True)

        # CSV Download
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", csv, "test_cases.csv", "text/csv")

        
# Excel Download (SAFE)
try:
    from io import BytesIO
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, engine="openpyxl")

    st.download_button(
        "📥 Download Excel",
        excel_buffer.getvalue(),
        "test_cases.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
except ImportError:
    st.warning("⚠️ openpyxl not installed. Please check requirements.txt")
except Exception as e:
    st.warning(f"⚠️ Excel export failed: {str(e)}")
