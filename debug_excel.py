#!/usr/bin/env python3
"""
Excel File Debugging Utility for PFRDA AI Validator
"""

import pandas as pd
import sys
import os
from pathlib import Path

def debug_excel_file(file_path):
    """
    Debug an Excel file to identify potential issues
    """
    print(f"🔍 Debugging Excel file: {file_path}")
    print("=" * 60)
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        # Basic file info
        file_size = os.path.getsize(file_path)
        print(f"📁 File size: {file_size:,} bytes")
        
        # Try reading with pandas
        print("\n🔄 Attempting to read Excel file...")
        
        try:
            # Method 1: Default engine
            print("📊 Method 1: Default pandas engine...")
            xls = pd.ExcelFile(file_path)
            print(f"✅ Successfully opened with default engine")
            print(f"📋 Found {len(xls.sheet_names)} sheets: {xls.sheet_names}")
            
            # Try to parse each sheet
            for i, sheet_name in enumerate(xls.sheet_names):
                try:
                    df = xls.parse(sheet_name)
                    print(f"  ✅ Sheet '{sheet_name}': {len(df)} rows × {len(df.columns)} columns")
                    
                    # Show column info
                    if len(df.columns) > 0:
                        print(f"     Columns: {list(df.columns)}")
                        
                    # Show sample data
                    if len(df) > 0:
                        print("     Sample data:")
                        print(df.head(2).to_string(index=False))
                        
                    if i >= 2:  # Limit to first 3 sheets for brevity
                        remaining = len(xls.sheet_names) - i - 1
                        if remaining > 0:
                            print(f"     ... and {remaining} more sheets")
                        break
                        
                except Exception as sheet_error:
                    print(f"  ❌ Sheet '{sheet_name}' error: {str(sheet_error)}")
            
        except Exception as e1:
            print(f"❌ Default engine failed: {str(e1)}")
            
            # Method 2: openpyxl engine
            print("\n📊 Method 2: openpyxl engine...")
            try:
                xls = pd.ExcelFile(file_path, engine='openpyxl')
                print(f"✅ Successfully opened with openpyxl engine")
                print(f"📋 Found {len(xls.sheet_names)} sheets: {xls.sheet_names}")
                
                for sheet_name in xls.sheet_names[:3]:  # First 3 sheets
                    try:
                        df = xls.parse(sheet_name)
                        print(f"  ✅ Sheet '{sheet_name}': {len(df)} rows × {len(df.columns)} columns")
                    except Exception as sheet_error:
                        print(f"  ❌ Sheet '{sheet_name}' error: {str(sheet_error)}")
                        
            except Exception as e2:
                print(f"❌ openpyxl engine failed: {str(e2)}")
                
                # Method 3: xlrd engine (for older .xls files)
                if file_path.endswith('.xls'):
                    print("\n📊 Method 3: xlrd engine (for .xls files)...")
                    try:
                        xls = pd.ExcelFile(file_path, engine='xlrd')
                        print(f"✅ Successfully opened with xlrd engine")
                        print(f"📋 Found {len(xls.sheet_names)} sheets: {xls.sheet_names}")
                    except Exception as e3:
                        print(f"❌ xlrd engine failed: {str(e3)}")
                        return False
                else:
                    return False
        
        print(f"\n✅ File debugging completed successfully!")
        return True
        
    except Exception as critical_error:
        print(f"❌ Critical error: {str(critical_error)}")
        return False

def main():
    """
    Main function for debugging Excel files
    """
    print("🏦 PFRDA AI Validator - Excel File Debugger")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        debug_excel_file(file_path)
    else:
        print("💡 Usage: python debug_excel.py <path_to_excel_file>")
        print("\n🎯 Example:")
        print("python debug_excel.py test_files/SRS_Specification.xlsx")
        
        # List available test files
        test_dir = Path("test_files")
        if test_dir.exists():
            test_files = list(test_dir.glob("*.xlsx")) + list(test_dir.glob("*.xls"))
            if test_files:
                print(f"\n📁 Available test files in {test_dir}:")
                for file in test_files:
                    print(f"  - {file}")

if __name__ == "__main__":
    main()
