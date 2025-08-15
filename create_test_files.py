import pandas as pd
import os

# Create sample SRS (System Requirements Specification) file
srs_data = {
    'Column Name': ['Employee_ID', 'Name', 'Salary', 'Department', 'Join_Date'],
    'Type': ['string', 'string', 'float', 'string', 'date'],
    'Required': ['Yes', 'Yes', 'Yes', 'No', 'Yes'],
    'Min': [None, None, 30000, None, None],
    'Max': [None, None, 500000, None, None],
    'Regex': [r'^EMP\d{3}$', None, None, None, None],
    'Description': [
        'Employee ID in format EMP###',
        'Employee full name',
        'Annual salary in INR',
        'Department name',
        'Date of joining'
    ]
}

# Create sample data file
data_sample = {
    'Employee_ID': ['EMP001', 'EMP002', 'EMP003', 'INVALID', 'EMP005'],
    'Name': ['Raj Kumar', 'Priya Sharma', 'Amit Singh', '', 'Neha Gupta'],
    'Salary': [45000, 65000, 25000, 80000, 95000],  # EMP003 has salary below min
    'Department': ['IT', 'Finance', 'HR', 'IT', None],
    'Join_Date': ['2023-01-15', '2023-02-20', '2023-03-10', '2023-04-05', '2023-05-12']
}

# Create directory for test files
os.makedirs('test_files', exist_ok=True)

# Create SRS Excel file
srs_df = pd.DataFrame(srs_data)
srs_df.to_excel('test_files/SRS_Specification.xlsx', sheet_name='Employee_SRS', index=False)
print("✅ Created SRS_Specification.xlsx")

# Create data Excel file
data_df = pd.DataFrame(data_sample)
data_df.to_excel('test_files/Employee_Data.xlsx', sheet_name='Employee_SRS', index=False)
print("✅ Created Employee_Data.xlsx")

# Create a multi-sheet version
with pd.ExcelWriter('test_files/Multi_Sheet_Data.xlsx') as writer:
    data_df.to_excel(writer, sheet_name='Employee_SRS', index=False)
    
    # Add another sheet with different data
    other_data = {
        'Project_ID': ['PRJ001', 'PRJ002', 'PRJ003'],
        'Project_Name': ['Web Portal', 'Mobile App', 'Database Migration'],
        'Budget': [150000, 200000, 100000]
    }
    other_df = pd.DataFrame(other_data)
    other_df.to_excel(writer, sheet_name='Projects', index=False)

print("✅ Created Multi_Sheet_Data.xlsx")

# Display sample data
print("\n📊 Sample SRS Data:")
print(srs_df.head())
print("\n📊 Sample Employee Data:")
print(data_df.head())
print("\n🎯 Test Features:")
print("- Employee ID validation (regex)")
print("- Salary range validation (min/max)")
print("- Required field validation")
print("- Data type validation")
print("- Date format validation")

print(f"\n📁 Test files created in: {os.path.abspath('test_files')}")
print("🚀 Upload these files to test the Excel parsing functionality!")
