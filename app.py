import streamlit as st
import pandas as pd
import io
import os
from utils.processor import generate_report

# --------------------------------------
# Page Config
# --------------------------------------
st.set_page_config(
    page_title="CodeChef Sincerity Score",
    layout="centered"
)

st.title("📊 CodeChef Contest Report Generator")

# --------------------------------------
# Paths
# --------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

ALL_STUDENTS_FILE = os.path.join(DATA_DIR, "All Student Details.xlsx")
DEFAULT_FEEDBACK_FILE = os.path.join(DATA_DIR, "RollNo_Reason.xlsx")

# --------------------------------------
# Batch Dropdown
# --------------------------------------
BATCHES = [
    "SNIST-Y23-PHASE-2",
    "GNITS-Y23-P2-B2",
    "GNITS-Y23-P2-B1",
    "BI-VITB-Y23-P2",
    "KLH-Y23-B2-P2",
    "BVRITH-Y23-P3-ALL",
    "KLH-Y23-B1-P3",
    "MGIT-Y23-P1-ALL",
    "ACE-Y23-P1-B1",
    "KLH-Y23-B6-P2-FDN",
    "CMRCET-Y23-P3",
    "KLH-Y23-B7-WEB-DEV",
    "ACE-Y23-P1-B2",
    "KLH-Y23-B5-P2-FDN",
    "KLH-Y23-B4-P2-FDN",
    "KLH-Y23-B3-P2-FDN",
    "BZ-INTERNAL_TEAM"
]

batch = st.selectbox("Select Batch", BATCHES)

# --------------------------------------
# Feedback Option
# --------------------------------------
has_feedback = st.radio(
    "Is Feedback Available?",
    ["Yes", "No"],
    horizontal=True
)

feedback_df = None

if has_feedback == "Yes":
    feedback_file = st.file_uploader(
        "Upload RollNo_Reason.xlsx",
        type=["xlsx"]
    )
    if feedback_file:
        feedback_df = pd.read_excel(feedback_file, engine="openpyxl")

else:
    st.info("Using default feedback file from repository")
    if os.path.exists(DEFAULT_FEEDBACK_FILE):
        feedback_df = pd.read_excel(DEFAULT_FEEDBACK_FILE, engine="openpyxl")
    else:
        st.error("Default feedback file not found")

# --------------------------------------
# Generate Button
# --------------------------------------
if st.button("⚙️ Generate Report"):
    if has_feedback == "Yes" and feedback_df is None:
        st.error("Please upload feedback file")
    else:
        try:
            with st.spinner("Processing data..."):
                if not os.path.exists(ALL_STUDENTS_FILE):
                    st.error("All Student Details file not found")
                    st.stop()

                data_df = pd.read_excel(
                    ALL_STUDENTS_FILE,
                    engine="openpyxl"
                )

                final_df = generate_report(
                    data=data_df,
                    feedback=feedback_df,
                    batch=batch,
                    hasfb=(has_feedback == "Yes")
                )

                output = io.BytesIO()
                final_df.to_excel(output, engine="openpyxl")
                output.seek(0)

                st.success("Report generated successfully")

                st.download_button(
                    label="⬇️ Download Excel Report",
                    data=output,
                    file_name=f"{batch}_CodeChef_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                st.subheader("🔍 Preview (First 10 rows)")
                st.dataframe(final_df.head(10), use_container_width=True)

        except Exception as e:
            st.error("An error occurred while processing")
            st.exception(e)
