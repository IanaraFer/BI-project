#!/usr/bin/env python3
"""
ESF Data Conversion Guide
========================

This script provides step-by-step instructions and code to convert your 
actual ESF data from various formats into clean, analyzable CSV files.

Follow this guide to prepare your real ESF projects and beneficiaries data.
"""

import pandas as pd
import os
from datetime import datetime

def step1_identify_your_data_source():
    """
    STEP 1: Identify Your Data Source
    """
    print("="*60)
    print("STEP 1: IDENTIFY YOUR DATA SOURCE")
    print("="*60)
    print("""
    Your current files contain HTML instead of CSV data. 
    To fix this, you need to:
    
    1. Export data from your ESF management system as CSV
    2. Or copy data from Excel/Google Sheets to CSV
    3. Or extract data from a database
    
    Common data sources for ESF programs:
    - ESF management software (e.g., eGrantsManagement, Salesforce)
    - Excel spreadsheets
    - Database exports (SQL Server, MySQL, PostgreSQL)
    - Web portals with export functionality
    """)

def step2_prepare_projects_data():
    """
    STEP 2: Prepare Projects Data
    """
    print("="*60)
    print("STEP 2: PREPARE PROJECTS DATA")
    print("="*60)
    print("""
    Your ESF Projects CSV should contain these columns (minimum):
    
    REQUIRED COLUMNS:
    - project_id: Unique identifier for each project
    - project_name: Name/title of the project
    - project_type: Category (e.g., Skills Development, Youth Employment)
    - status: Current status (Active, Completed, Planning, On Hold)
    - start_date: Project start date (YYYY-MM-DD format)
    - end_date: Project end date (YYYY-MM-DD format)
    - total_budget: Total project budget (numeric)
    - esf_funding: ESF contribution amount (numeric)
    - beneficiaries_target: Target number of beneficiaries
    
    OPTIONAL COLUMNS:
    - country: Country where project is implemented
    - region: Specific region/area
    - lead_organization: Organization managing the project
    - description: Project description
    - beneficiaries_actual: Actual number of beneficiaries served
    
    EXAMPLE CSV STRUCTURE:
    project_id,project_name,project_type,status,start_date,end_date,total_budget,esf_funding,beneficiaries_target
    ESF_001,Digital Skills Training,Digital Skills,Active,2023-01-15,2024-12-31,150000,120000,200
    ESF_002,Youth Employment Program,Youth Employment,Planning,2023-03-01,2025-02-28,250000,200000,150
    """)

def step3_prepare_beneficiaries_data():
    """
    STEP 3: Prepare Beneficiaries Data
    """
    print("="*60)
    print("STEP 3: PREPARE BENEFICIARIES DATA")
    print("="*60)
    print("""
    Your ESF Beneficiaries CSV should contain these columns (minimum):
    
    REQUIRED COLUMNS:
    - beneficiary_id: Unique identifier for each beneficiary
    - project_id: Links to the project (must match projects data)
    - gender: Male, Female, Other, Prefer not to say
    - age_group: Age ranges (e.g., 18-24, 25-34, 35-44, etc.)
    - education_level: Primary, Secondary, Post-Secondary, Tertiary
    
    OPTIONAL COLUMNS:
    - employment_status_before: Employment status before participation
    - employment_status_after: Employment status after participation
    - participation_start: Start date of participation
    - participation_end: End date of participation
    - training_hours: Number of training hours completed
    - outcome_achieved: Final outcome (Employed, Self-employed, etc.)
    - satisfaction_score: Satisfaction rating (1-5 scale)
    - region: Geographic region
    - vulnerable_group: Special category if applicable
    
    EXAMPLE CSV STRUCTURE:
    beneficiary_id,project_id,gender,age_group,education_level,employment_status_before,outcome_achieved
    BEN_001,ESF_001,Female,25-34,Secondary,Unemployed,Employed
    BEN_002,ESF_001,Male,18-24,Tertiary,Student,Self-employed
    """)

def step4_data_conversion_examples():
    """
    STEP 4: Data Conversion Examples
    """
    print("="*60)
    print("STEP 4: DATA CONVERSION EXAMPLES")
    print("="*60)
    print("""
    Here are common scenarios and how to handle them:
    
    SCENARIO 1: Data in Excel
    1. Open your Excel file
    2. Select all data including headers
    3. Save As > CSV (Comma delimited)
    4. Choose UTF-8 encoding if available
    
    SCENARIO 2: Data from Database
    Use SQL query like:
    SELECT project_id, project_name, project_type, status, 
           start_date, end_date, total_budget, esf_funding, 
           beneficiaries_target
    FROM projects 
    WHERE program_type = 'ESF';
    
    SCENARIO 3: Data from Web Portal
    1. Look for "Export" or "Download" buttons
    2. Choose CSV format
    3. Select all required fields
    4. Download and save to your project folder
    """)

def step5_test_your_data():
    """
    STEP 5: Test Your Data
    """
    print("="*60)
    print("STEP 5: TEST YOUR DATA")
    print("="*60)
    print("""
    Use this code to test if your CSV files are properly formatted:
    """)
    
    test_code = '''
import pandas as pd

# Test Projects Data
try:
    projects_df = pd.read_csv('esf_projects.csv')
    print(f"✅ Projects CSV loaded successfully: {len(projects_df)} records")
    print(f"Columns: {list(projects_df.columns)}")
    print(f"Sample data:")
    print(projects_df.head())
except Exception as e:
    print(f"❌ Error loading projects CSV: {e}")

# Test Beneficiaries Data  
try:
    beneficiaries_df = pd.read_csv('esf_beneficiaries.csv')
    print(f"✅ Beneficiaries CSV loaded successfully: {len(beneficiaries_df)} records")
    print(f"Columns: {list(beneficiaries_df.columns)}")
    print(f"Sample data:")
    print(beneficiaries_df.head())
except Exception as e:
    print(f"❌ Error loading beneficiaries CSV: {e}")
'''
    
    print(test_code)

def step6_run_cleaning_and_analysis():
    """
    STEP 6: Run Cleaning and Analysis
    """
    print("="*60)
    print("STEP 6: RUN CLEANING AND ANALYSIS")
    print("="*60)
    print("""
    Once your CSV files are ready:
    
    1. Replace the current HTML files with your CSV files:
       - esf_projects.csv (your projects data)
       - esf_beneficiaries.csv (your beneficiaries data)
    
    2. Run the data cleaning script:
       python data_cleaning_script.py
    
    3. Run the analysis script:
       python basic_analysis_script.py
    
    4. Check the cleaned_data/ folder for results:
       - esf_projects_cleaned.csv
       - esf_beneficiaries_cleaned.csv
       - comprehensive_esf_analysis_report.txt
       - comprehensive_esf_analysis_report_kpis.json
    """)

def create_template_csv_files():
    """
    Create template CSV files for reference
    """
    print("="*60)
    print("CREATING TEMPLATE CSV FILES")
    print("="*60)
    
    # Projects template
    projects_template = {
        'project_id': ['ESF_001', 'ESF_002', 'ESF_003'],
        'project_name': ['Digital Skills Training', 'Youth Employment Program', 'Green Skills Initiative'],
        'project_type': ['Digital Skills', 'Youth Employment', 'Green Skills'],
        'status': ['Active', 'Planning', 'Active'],
        'country': ['Ireland', 'Ireland', 'Ireland'],
        'region': ['Dublin', 'Cork', 'Galway'],
        'start_date': ['2023-01-15', '2023-03-01', '2023-02-10'],
        'end_date': ['2024-12-31', '2025-02-28', '2024-11-30'],
        'total_budget': [150000, 250000, 180000],
        'esf_funding': [120000, 200000, 144000],
        'beneficiaries_target': [200, 150, 175],
        'beneficiaries_actual': [180, 120, 165],
        'lead_organization': ['TechSkills Ireland', 'Youth Development Corp', 'Green Future Training'],
        'description': ['Digital skills training for unemployed adults', 'Employment support for young people', 'Environmental skills development']
    }
    
    projects_df = pd.DataFrame(projects_template)
    projects_df.to_csv('esf_projects_template.csv', index=False)
    print("✅ Created: esf_projects_template.csv")
    
    # Beneficiaries template
    beneficiaries_template = {
        'beneficiary_id': ['BEN_001', 'BEN_002', 'BEN_003', 'BEN_004', 'BEN_005'],
        'project_id': ['ESF_001', 'ESF_001', 'ESF_002', 'ESF_002', 'ESF_003'],
        'gender': ['Female', 'Male', 'Female', 'Male', 'Female'],
        'age_group': ['25-34', '18-24', '35-44', '18-24', '25-34'],
        'education_level': ['Secondary', 'Tertiary', 'Primary', 'Secondary', 'Post-Secondary'],
        'employment_status_before': ['Unemployed', 'Student', 'Unemployed', 'Unemployed', 'Employed'],
        'employment_status_after': ['Employed', 'Self-employed', 'Employed', 'Student', 'Employed'],
        'participation_start': ['2023-02-01', '2023-02-15', '2023-04-01', '2023-04-15', '2023-03-01'],
        'participation_end': ['2023-05-31', '2023-06-15', '2023-07-31', '2023-08-15', '2023-06-30'],
        'training_hours': [120, 80, 150, 100, 90],
        'outcome_achieved': ['Employed', 'Self-employed', 'Employed', 'Further Education', 'Employed'],
        'satisfaction_score': [5, 4, 5, 4, 4],
        'region': ['Dublin', 'Dublin', 'Cork', 'Cork', 'Galway'],
        'vulnerable_group': ['None', 'None', 'Long-term unemployed', 'Youth NEET', 'None']
    }
    
    beneficiaries_df = pd.DataFrame(beneficiaries_template)
    beneficiaries_df.to_csv('esf_beneficiaries_template.csv', index=False)
    print("✅ Created: esf_beneficiaries_template.csv")
    
    print("""
    📋 Template files created for reference!
    
    Use these as examples of the correct format for your data.
    Replace the sample data with your actual ESF program information.
    """)

def main():
    """Main guide execution"""
    print("ESF DATA CONVERSION GUIDE")
    print("=" * 30)
    print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    step1_identify_your_data_source()
    input("Press Enter to continue to Step 2...")
    
    step2_prepare_projects_data()
    input("Press Enter to continue to Step 3...")
    
    step3_prepare_beneficiaries_data()
    input("Press Enter to continue to Step 4...")
    
    step4_data_conversion_examples()
    input("Press Enter to continue to Step 5...")
    
    step5_test_your_data()
    input("Press Enter to continue to Step 6...")
    
    step6_run_cleaning_and_analysis()
    
    print("\nWould you like to create template CSV files for reference? (y/n): ", end="")
    if input().lower().startswith('y'):
        create_template_csv_files()
    
    print("\n" + "="*60)
    print("GUIDE COMPLETED!")
    print("="*60)
    print("""
    📚 Summary:
    1. ✅ Learned about required data structure
    2. ✅ Understood data conversion options
    3. ✅ Received testing code
    4. ✅ Got step-by-step instructions
    
    🚀 Next Actions:
    1. Export your real ESF data to CSV format
    2. Replace the HTML files with proper CSV files
    3. Run the cleaning and analysis scripts
    4. Review the generated reports and insights
    
    💡 Remember: The cleaning scripts will handle minor formatting issues,
    but your CSV files need to have the basic structure correct.
    """)

if __name__ == "__main__":
    main()
