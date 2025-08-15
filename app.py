# ai_data_validator/app.py
import streamlit as st
import pandas as pd
from difflib import get_close_matches
from srs_parser import parse_srs_file
from data_validator import validate_data_against_srs
from ollama_agent import explain_validation_results, summarize_data_sheet
from mongodb_service import MongoDBService

mongo_service = MongoDBService()

st.set_page_config(page_title="AI Data Validator", layout="wide")
st.title("📊 Multi-Sheet AI Data Validator (Pension Fund Edition)")

# MongoDB sidebar status
with st.sidebar:
    st.header("🗄️ Database Status")
    if mongo_service.client:
        st.success("✅ MongoDB Connected")
        st.subheader("📁 Recent Files")
        for file_doc in mongo_service.get_file_history(limit=5):
            st.text(f"📄 {file_doc['filename']}")
            st.caption(f"Uploaded: {file_doc['upload_date'].strftime('%Y-%m-%d %H:%M')}")
            st.caption(f"Sheets: {len(file_doc.get('sheets', []))}")
            st.divider()
    else:
        st.error("❌ MongoDB Disconnected")

srs_file = st.file_uploader("📥 Upload the SRS File (.csv or .xlsx)", type=["csv", "xlsx"], key="srs")
data_file = st.file_uploader("📥 Upload the Data File (.csv or .xlsx)", type=["csv", "xlsx"], key="data")

if srs_file and data_file:
    with st.spinner("Reading files and matching sheets..."):
        srs_dict = parse_srs_file(srs_file)
        data_dict = parse_srs_file(data_file)

    for sheet_name in data_dict:
        st.subheader(f"📄 Sheet: {sheet_name}")
        data_df = data_dict[sheet_name]

        matched_srs_name = get_close_matches(sheet_name, srs_dict.keys(), n=1, cutoff=0.6)
        if matched_srs_name:
            srs_df = srs_dict[matched_srs_name[0]]
            st.info(f"🔗 Fuzzy matched with SRS sheet: '{matched_srs_name[0]}'")
        else:
            st.warning(f"⚠️ No matching SRS sheet found for '{sheet_name}'")
            st.info(f"📊 Data Preview: {len(data_df)} rows × {len(data_df.columns)} columns")
            st.dataframe(data_df.head(), use_container_width=True)
            with st.expander("📊 AI Data Analysis (No Validation)"):
                with st.spinner("Generating AI analysis..."):
                    st.write(summarize_data_sheet(data_df, sheet_name))
            continue

        st.info(f"📊 Data Preview: {len(data_df)} rows × {len(data_df.columns)} columns")
        st.dataframe(data_df.head(), use_container_width=True)

        with st.spinner("Validating sheet..."):
            result_summary, failed_rules = validate_data_against_srs(data_df, srs_df)
            st.markdown("### ✅ Validation Summary")
            st.json(result_summary)

            if mongo_service.client:
                try:
                    mongo_service.store_validation_results(
                        file_id=None,  # You can integrate real file_id if storing files
                        sheet_name=sheet_name,
                        validation_summary=result_summary,
                        failed_rules=failed_rules
                    )
                except Exception as e:
                    st.warning(f"⚠️ Could not store validation results: {str(e)}")

            if failed_rules:
                st.markdown("### ❌ Failed Validations")
                st.table(failed_rules)
                with st.spinner("Explaining validation results via Ollama..."):
                    explanation = explain_validation_results(sheet_name, failed_rules)
                    st.markdown("### 🤖 AI-Powered Explanation")
                    st.write(explanation)
            else:
                st.success("🎉 All validations passed for this sheet!")

        with st.expander("📊 Additional Sheet Insights (via LLM)"):
            with st.spinner("Generating AI summary..."):
                st.write(summarize_data_sheet(data_df, sheet_name))