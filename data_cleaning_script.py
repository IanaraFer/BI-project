#!/usr/bin/env python3
"""
ESF Projects and Beneficiaries Data Cleaning Script
==================================================

This script helps clean and fix ESF (European Social Fund) project and beneficiary datasets.
It provides functions to:
1. Create sample datasets if none exist
2. Clean and standardize data
3. Perform data quality checks
4. Export cleaned data

Usage:
    python data_cleaning_script.py
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class ESFDataCleaner:
    def __init__(self):
        self.projects_df = None
        self.beneficiaries_df = None
        
    def create_sample_esf_projects(self, num_records=100):
        """Create sample ESF projects dataset"""
        print("Creating sample ESF projects dataset...")
        
        # Sample data generation
        np.random.seed(42)
        
        project_types = ['Skills Development', 'Youth Employment', 'Digital Skills', 
                        'Entrepreneurship', 'Green Skills', 'Social Inclusion']
        statuses = ['Active', 'Completed', 'On Hold', 'Planning']
        countries = ['Ireland', 'Spain', 'Italy', 'Portugal', 'Germany', 'France']
        regions = ['Dublin', 'Cork', 'Galway', 'Limerick', 'Waterford', 'Kilkenny']
        
        data = {
            'project_id': [f'ESF_{str(i).zfill(4)}' for i in range(1, num_records + 1)],
            'project_name': [f'Project {i}: {np.random.choice(project_types)} Initiative' 
                           for i in range(1, num_records + 1)],
            'project_type': np.random.choice(project_types, num_records),
            'status': np.random.choice(statuses, num_records),
            'country': np.random.choice(countries, num_records),
            'region': np.random.choice(regions, num_records),
            'start_date': pd.date_range('2020-01-01', '2023-12-31', periods=num_records),
            'end_date': pd.date_range('2021-01-01', '2025-12-31', periods=num_records),
            'total_budget': np.random.uniform(50000, 500000, num_records).round(2),
            'esf_funding': np.random.uniform(20000, 300000, num_records).round(2),
            'beneficiaries_target': np.random.randint(50, 1000, num_records),
            'beneficiaries_actual': np.random.randint(30, 1200, num_records),
            'lead_organization': [f'Organization {chr(65 + i % 26)}' for i in range(num_records)],
            'description': [f'This project focuses on {np.random.choice(project_types).lower()} for participants' 
                          for _ in range(num_records)]
        }
        
        self.projects_df = pd.DataFrame(data)
        return self.projects_df
    
    def create_sample_esf_beneficiaries(self, num_records=500):
        """Create sample ESF beneficiaries dataset"""
        print("Creating sample ESF beneficiaries dataset...")
        
        np.random.seed(42)
        
        genders = ['Male', 'Female', 'Other', 'Prefer not to say']
        age_groups = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        education_levels = ['Primary', 'Secondary', 'Post-Secondary', 'Tertiary', 'Other']
        employment_status = ['Unemployed', 'Employed', 'Self-employed', 'Student', 'Inactive']
        outcomes = ['Employed', 'Self-employed', 'Further Education', 'Still Seeking', 'Unknown']
        
        data = {
            'beneficiary_id': [f'BEN_{str(i).zfill(5)}' for i in range(1, num_records + 1)],
            'project_id': np.random.choice([f'ESF_{str(i).zfill(4)}' for i in range(1, 101)], num_records),
            'gender': np.random.choice(genders, num_records),
            'age_group': np.random.choice(age_groups, num_records),
            'education_level': np.random.choice(education_levels, num_records),
            'employment_status_before': np.random.choice(employment_status, num_records),
            'employment_status_after': np.random.choice(employment_status, num_records),
            'participation_start': pd.date_range('2020-01-01', '2024-06-30', periods=num_records),
            'participation_end': pd.date_range('2020-06-01', '2024-12-31', periods=num_records),
            'training_hours': np.random.randint(20, 200, num_records),
            'outcome_achieved': np.random.choice(outcomes, num_records),
            'satisfaction_score': np.random.randint(1, 6, num_records),  # 1-5 scale
            'region': np.random.choice(['Dublin', 'Cork', 'Galway', 'Limerick', 'Waterford', 'Kilkenny'], num_records),
            'vulnerable_group': np.random.choice(['None', 'Disability', 'Migrant', 'Long-term unemployed', 
                                                'Youth NEET', 'Roma'], num_records, p=[0.6, 0.1, 0.1, 0.1, 0.05, 0.05])
        }
        
        self.beneficiaries_df = pd.DataFrame(data)
        return self.beneficiaries_df
    
    def load_existing_data(self, projects_file=None, beneficiaries_file=None):
        """Load existing CSV files if they exist"""
        try:
            if projects_file:
                print(f"Loading projects data from {projects_file}")
                self.projects_df = pd.read_csv(projects_file)
                print(f"Loaded {len(self.projects_df)} project records")
            
            if beneficiaries_file:
                print(f"Loading beneficiaries data from {beneficiaries_file}")
                self.beneficiaries_df = pd.read_csv(beneficiaries_file)
                print(f"Loaded {len(self.beneficiaries_df)} beneficiary records")
                
        except FileNotFoundError as e:
            print(f"File not found: {e}")
            print("Creating sample data instead...")
            
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def clean_projects_data(self):
        """Clean and standardize projects data"""
        if self.projects_df is None:
            print("No projects data to clean")
            return
        
        print("Cleaning projects data...")
        df = self.projects_df.copy()
        
        # Clean project names
        df['project_name'] = df['project_name'].str.strip()
        df['project_name'] = df['project_name'].str.title()
        
        # Standardize status values
        status_mapping = {
            'active': 'Active',
            'completed': 'Completed', 
            'on hold': 'On Hold',
            'planning': 'Planning',
            'cancelled': 'Cancelled',
            'suspended': 'On Hold'
        }
        df['status'] = df['status'].str.lower().map(status_mapping).fillna(df['status'])
        
        # Clean date columns
        date_cols = ['start_date', 'end_date']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Clean numeric columns
        numeric_cols = ['total_budget', 'esf_funding', 'beneficiaries_target', 'beneficiaries_actual']
        for col in numeric_cols:
            if col in df.columns:
                # Remove currency symbols and convert to numeric
                if df[col].dtype == 'object':
                    df[col] = df[col].astype(str).str.replace(r'[€$£,]', '', regex=True)
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Ensure ESF funding doesn't exceed total budget
        if 'total_budget' in df.columns and 'esf_funding' in df.columns:
            df.loc[df['esf_funding'] > df['total_budget'], 'esf_funding'] = df['total_budget'] * 0.8
        
        # Clean organization names
        if 'lead_organization' in df.columns:
            df['lead_organization'] = df['lead_organization'].str.strip().str.title()
        
        # Add derived columns
        if 'start_date' in df.columns and 'end_date' in df.columns:
            df['project_duration_days'] = (df['end_date'] - df['start_date']).dt.days
        
        if 'beneficiaries_target' in df.columns and 'beneficiaries_actual' in df.columns:
            df['target_achievement_rate'] = (df['beneficiaries_actual'] / df['beneficiaries_target'] * 100).round(2)
        
        self.projects_df = df
        print(f"Projects data cleaned. Shape: {df.shape}")
        
    def clean_beneficiaries_data(self):
        """Clean and standardize beneficiaries data"""
        if self.beneficiaries_df is None:
            print("No beneficiaries data to clean")
            return
        
        print("Cleaning beneficiaries data...")
        df = self.beneficiaries_df.copy()
        
        # Standardize gender values
        gender_mapping = {
            'm': 'Male', 'male': 'Male', 'man': 'Male',
            'f': 'Female', 'female': 'Female', 'woman': 'Female',
            'other': 'Other', 'non-binary': 'Other',
            'prefer not to say': 'Prefer not to say', 'unknown': 'Prefer not to say'
        }
        if 'gender' in df.columns:
            df['gender'] = df['gender'].str.lower().map(gender_mapping).fillna(df['gender'])
        
        # Clean age groups
        if 'age_group' in df.columns:
            df['age_group'] = df['age_group'].str.replace(' ', '').str.replace('years', '').str.replace('yrs', '')
        
        # Standardize education levels
        education_mapping = {
            'primary': 'Primary',
            'secondary': 'Secondary', 'high school': 'Secondary',
            'post-secondary': 'Post-Secondary', 'college': 'Post-Secondary',
            'tertiary': 'Tertiary', 'university': 'Tertiary', 'degree': 'Tertiary',
            'other': 'Other', 'unknown': 'Other'
        }
        if 'education_level' in df.columns:
            df['education_level'] = df['education_level'].str.lower().map(education_mapping).fillna(df['education_level'])
        
        # Clean date columns
        date_cols = ['participation_start', 'participation_end']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Clean numeric columns
        numeric_cols = ['training_hours', 'satisfaction_score']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Validate satisfaction scores (should be 1-5)
        if 'satisfaction_score' in df.columns:
            df.loc[df['satisfaction_score'] > 5, 'satisfaction_score'] = 5
            df.loc[df['satisfaction_score'] < 1, 'satisfaction_score'] = np.nan
        
        # Add derived columns
        if 'participation_start' in df.columns and 'participation_end' in df.columns:
            df['participation_duration_days'] = (df['participation_end'] - df['participation_start']).dt.days
        
        self.beneficiaries_df = df
        print(f"Beneficiaries data cleaned. Shape: {df.shape}")
    
    def perform_data_quality_checks(self):
        """Perform data quality checks and report issues"""
        print("\n" + "="*50)
        print("DATA QUALITY REPORT")
        print("="*50)
        
        # Projects data quality checks
        if self.projects_df is not None:
            print("\nPROJECTS DATA QUALITY:")
            print("-" * 30)
            
            # Check for duplicates
            duplicates = self.projects_df.duplicated().sum()
            print(f"Duplicate rows: {duplicates}")
            
            # Check for missing values
            missing_data = self.projects_df.isnull().sum()
            if missing_data.sum() > 0:
                print("\nMissing values per column:")
                for col, count in missing_data[missing_data > 0].items():
                    print(f"  {col}: {count} ({count/len(self.projects_df)*100:.1f}%)")
            
            # Check data ranges
            if 'total_budget' in self.projects_df.columns:
                budget_issues = self.projects_df[self.projects_df['total_budget'] <= 0]
                if len(budget_issues) > 0:
                    print(f"Projects with invalid budget: {len(budget_issues)}")
            
            # Check date consistency
            if all(col in self.projects_df.columns for col in ['start_date', 'end_date']):
                date_issues = self.projects_df[self.projects_df['start_date'] >= self.projects_df['end_date']]
                if len(date_issues) > 0:
                    print(f"Projects with end date before start date: {len(date_issues)}")
        
        # Beneficiaries data quality checks
        if self.beneficiaries_df is not None:
            print("\nBENEFICIARIES DATA QUALITY:")
            print("-" * 30)
            
            # Check for duplicates
            duplicates = self.beneficiaries_df.duplicated().sum()
            print(f"Duplicate rows: {duplicates}")
            
            # Check for missing values
            missing_data = self.beneficiaries_df.isnull().sum()
            if missing_data.sum() > 0:
                print("\nMissing values per column:")
                for col, count in missing_data[missing_data > 0].items():
                    print(f"  {col}: {count} ({count/len(self.beneficiaries_df)*100:.1f}%)")
            
            # Check for orphaned beneficiaries (if projects data exists)
            if self.projects_df is not None and 'project_id' in self.beneficiaries_df.columns:
                valid_projects = set(self.projects_df['project_id'])
                orphaned = self.beneficiaries_df[~self.beneficiaries_df['project_id'].isin(valid_projects)]
                if len(orphaned) > 0:
                    print(f"Beneficiaries with invalid project_id: {len(orphaned)}")
    
    def generate_summary_statistics(self):
        """Generate summary statistics for both datasets"""
        print("\n" + "="*50)
        print("SUMMARY STATISTICS")
        print("="*50)
        
        # Projects summary
        if self.projects_df is not None:
            print("\nPROJECTS SUMMARY:")
            print("-" * 20)
            print(f"Total projects: {len(self.projects_df)}")
            
            if 'status' in self.projects_df.columns:
                print("\nProject status distribution:")
                status_counts = self.projects_df['status'].value_counts()
                for status, count in status_counts.items():
                    print(f"  {status}: {count}")
            
            if 'total_budget' in self.projects_df.columns:
                total_budget = self.projects_df['total_budget'].sum()
                print(f"\nTotal budget: €{total_budget:,.2f}")
            
            if 'esf_funding' in self.projects_df.columns:
                total_esf = self.projects_df['esf_funding'].sum()
                print(f"Total ESF funding: €{total_esf:,.2f}")
        
        # Beneficiaries summary
        if self.beneficiaries_df is not None:
            print("\nBENEFICIARIES SUMMARY:")
            print("-" * 25)
            print(f"Total beneficiaries: {len(self.beneficiaries_df)}")
            
            if 'gender' in self.beneficiaries_df.columns:
                print("\nGender distribution:")
                gender_counts = self.beneficiaries_df['gender'].value_counts()
                for gender, count in gender_counts.items():
                    print(f"  {gender}: {count}")
            
            if 'age_group' in self.beneficiaries_df.columns:
                print("\nAge group distribution:")
                age_counts = self.beneficiaries_df['age_group'].value_counts()
                for age, count in age_counts.items():
                    print(f"  {age}: {count}")
    
    def export_cleaned_data(self, output_dir="cleaned_data"):
        """Export cleaned data to CSV files"""
        import os
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        if self.projects_df is not None:
            projects_file = os.path.join(output_dir, "esf_projects_cleaned.csv")
            self.projects_df.to_csv(projects_file, index=False)
            print(f"Cleaned projects data exported to: {projects_file}")
        
        if self.beneficiaries_df is not None:
            beneficiaries_file = os.path.join(output_dir, "esf_beneficiaries_cleaned.csv")
            self.beneficiaries_df.to_csv(beneficiaries_file, index=False)
            print(f"Cleaned beneficiaries data exported to: {beneficiaries_file}")

def main():
    """Main execution function"""
    print("ESF Data Cleaning and Processing Tool")
    print("=" * 40)
    
    # Initialize the cleaner
    cleaner = ESFDataCleaner()
    
    # Try to load existing data first
    # Since the current files are HTML, we'll create sample data
    print("Current CSV files contain HTML content instead of data.")
    print("Creating sample datasets for demonstration...")
    
    # Create sample datasets
    cleaner.create_sample_esf_projects(100)
    cleaner.create_sample_esf_beneficiaries(500)
    
    # Clean the data
    cleaner.clean_projects_data()
    cleaner.clean_beneficiaries_data()
    
    # Perform quality checks
    cleaner.perform_data_quality_checks()
    
    # Generate summary statistics
    cleaner.generate_summary_statistics()
    
    # Export cleaned data
    cleaner.export_cleaned_data()
    
    print("\n" + "="*50)
    print("DATA CLEANING COMPLETED SUCCESSFULLY!")
    print("="*50)
    print("\nNext steps:")
    print("1. Replace the sample data with your actual ESF data")
    print("2. Run this script again to clean your real data")
    print("3. Review the quality report and fix any issues")
    print("4. Use the cleaned data for analysis and reporting")

if __name__ == "__main__":
    main()
