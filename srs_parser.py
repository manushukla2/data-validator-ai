import pandas as pd
import streamlit as st
import traceback

def parse_srs_file(file):
    """Loads CSV or XLSX and returns a dict of {sheet_name: dataframe}"""
    try:
        if file.name.endswith(".csv"):
            st.info(f"📄 Parsing CSV file: {file.name}")
            df = pd.read_csv(file)
            st.success(f"✅ CSV loaded successfully: {len(df)} rows, {len(df.columns)} columns")
            return {"Sheet1": df}
        
        elif file.name.endswith(".xlsx") or file.name.endswith(".xls"):
            st.info(f"📊 Parsing Excel file: {file.name}")
            
            # Reset file pointer to beginning
            file.seek(0)
            
            # Try to read Excel file
            try:
                xls = pd.ExcelFile(file)
                st.info(f"📋 Found {len(xls.sheet_names)} sheets: {', '.join(xls.sheet_names)}")
                
                result = {}
                for sheet_name in xls.sheet_names:
                    try:
                        df = xls.parse(sheet_name)
                        result[sheet_name] = df
                        st.success(f"✅ Sheet '{sheet_name}' loaded: {len(df)} rows, {len(df.columns)} columns")
                    except Exception as sheet_error:
                        st.error(f"❌ Error parsing sheet '{sheet_name}': {str(sheet_error)}")
                        continue
                
                if not result:
                    raise ValueError("No sheets could be parsed from the Excel file")
                
                return result
                
            except Exception as excel_error:
                st.error(f"❌ Error reading Excel file: {str(excel_error)}")
                
                # Try alternative method with openpyxl engine
                st.info("🔄 Trying alternative Excel reading method...")
                try:
                    file.seek(0)
                    xls = pd.ExcelFile(file, engine='openpyxl')
                    result = {}
                    for sheet_name in xls.sheet_names:
                        df = xls.parse(sheet_name)
                        result[sheet_name] = df
                        st.success(f"✅ Sheet '{sheet_name}' loaded with openpyxl: {len(df)} rows, {len(df.columns)} columns")
                    return result
                except Exception as alt_error:
                    st.error(f"❌ Alternative method also failed: {str(alt_error)}")
                    raise excel_error
        
        else:
            error_msg = f"Unsupported file type: {file.name}. Please upload .csv, .xlsx, or .xls files."
            st.error(error_msg)
            raise ValueError(error_msg)
    
    except Exception as e:
        st.error(f"❌ Critical error parsing file {file.name}: {str(e)}")
        st.error("🔍 Full error details:")
        st.code(traceback.format_exc())
        raise e
