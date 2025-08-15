import pandas as pd
import numpy as np

def validate_data_against_srs(data_df, srs_df):
    failed_rules = []
    result_summary = {
        "total_rows": len(data_df),
        "total_columns": len(data_df.columns),
        "validation_passed": True,
        "errors": 0
    }

    for _, rule in srs_df.iterrows():
        col = rule.get("Column Name") or rule.get("column")
        dtype = str(rule.get("Type", "")).lower()
        required = str(rule.get("Required", "")).strip().lower() == "yes"
        min_val = rule.get("Min")
        max_val = rule.get("Max")
        regex = rule.get("Regex")

        if col not in data_df.columns:
            failed_rules.append({"column": col, "error": "Missing column"})
            result_summary["validation_passed"] = False
            result_summary["errors"] += 1
            continue

        series = data_df[col]

        if required and series.isnull().any():
            failed_rules.append({"column": col, "error": "Missing required values"})
            result_summary["validation_passed"] = False
            result_summary["errors"] += 1

        if dtype == "int" or dtype == "integer":
            if not pd.api.types.is_integer_dtype(series.dropna()):
                failed_rules.append({"column": col, "error": "Expected integer values"})
                result_summary["validation_passed"] = False
                result_summary["errors"] += 1

        elif dtype == "float":
            if not pd.api.types.is_float_dtype(series.dropna()) and not pd.api.types.is_integer_dtype(series.dropna()):
                failed_rules.append({"column": col, "error": "Expected float values"})
                result_summary["validation_passed"] = False
                result_summary["errors"] += 1

        elif dtype == "date":
            try:
                pd.to_datetime(series.dropna())
            except Exception:
                failed_rules.append({"column": col, "error": "Invalid date format"})
                result_summary["validation_passed"] = False
                result_summary["errors"] += 1

        if pd.notnull(min_val):
            try:
                if (series.dropna().astype(float) < float(min_val)).any():
                    failed_rules.append({"column": col, "error": f"Value below min: {min_val}"})
                    result_summary["validation_passed"] = False
                    result_summary["errors"] += 1
            except:
                pass

        if pd.notnull(max_val):
            try:
                if (series.dropna().astype(float) > float(max_val)).any():
                    failed_rules.append({"column": col, "error": f"Value above max: {max_val}"})
                    result_summary["validation_passed"] = False
                    result_summary["errors"] += 1
            except:
                pass

    return result_summary, failed_rules