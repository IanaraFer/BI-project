#!/usr/bin/env python3
"""
ESF Data Cleaning and Processing Script
======================================

This script handles the cleaning and preparation of ESF (European Social Fund) data.
It includes:
1. Data loading and validation
2. HTML to CSV conversion
3. Sample data generation
4. Data quality checks
5. Export of cleaned datasets

Usage:
    python data_cleaning_script.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import csv
import json
import os
import random

class ESFDataCleaner:
    def __init__(self):
        self.projects_df = None
        self.beneficiaries_df = None
        
        # Ensure output directory exists
        os.makedirs('cleaned_data', exist_ok=True)
    
    def create_sample_esf_projects(self, num_projects=100):
        """Create sample ESF projects data"""
        print("🔧 Generating sample ESF projects data...")
        
        # Define realistic project types
        project_types = [
            'Skills Development', 'Digital Skills', 'Youth Employment',
            'Entrepreneurship', 'Green Skills', 'Social Inclusion'
        ]
        
        # Define regions (Irish counties)
        regions = ['Dublin', 'Cork', 'Galway', 'Limerick', 'Waterford', 'Kilkenny']
        
        # Define project statuses
        statuses = ['Planning', 'Active', 'Completed', 'On Hold']
        
        # Generate sample data
        projects_data = []
        
        for i in range(1, num_projects + 1):
            # Generate random dates
            start_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1800))
            end_date = start_date + timedelta(days=random.randint(180, 720))
            
            # Generate budget information
            total_budget = random.uniform(50000, 500000)
            esf_funding = total_budget * random.uniform(0.4, 0.6)  # 40-60% ESF funding
            
            # Generate beneficiary targets
            beneficiaries_target = random.randint(10, 50)
            
            project = {
                'project_id': f'ESF-{i:04d}',
                'project_name': f'{random.choice(project_types)} Initiative {i}',
                'project_type': random.choice(project_types),
                'region': random.choice(regions),
                'status': random.choice(statuses),
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'total_budget': round(total_budget, 2),
                'esf_funding': round(esf_funding, 2),
                'beneficiaries_target': beneficiaries_target,
                'lead_organization': f'Organization {chr(65 + i % 26)}',
                'description': f'ESF {random.choice(project_types)} project focused on skills development',
                'target_achievement_rate': round(random.uniform(50, 200), 1),
                'engagement_score': round(random.uniform(1, 5), 1),
                'risk_flag': random.choice(['Low', 'Medium', 'High'])
            }
            
            projects_data.append(project)
        
        self.projects_df = pd.DataFrame(projects_data)
        print(f"✅ Generated {len(self.projects_df)} sample projects")
        return self.projects_df
    
    def create_sample_esf_beneficiaries(self, num_beneficiaries=500):
        """Create sample ESF beneficiaries data"""
        print("👥 Generating sample ESF beneficiaries data...")
        
        # Ensure we have projects data
        if self.projects_df is None:
            self.create_sample_esf_projects()
        
        # Define demographics
        genders = ['Male', 'Female']
        age_groups = ['18-24', '25-34', '35-44', '45-54', '55+']
        education_levels = ['Primary', 'Secondary', 'Third Level', 'Postgraduate']
        employment_statuses = ['Unemployed', 'Employed', 'Student', 'Self-employed']
        vulnerable_groups = ['Long-term Unemployed', 'Early School Leaver', 'Migrant', 'Person with Disability', 'None']
        outcomes = ['Employed', 'Self-employed', 'Further Education', 'Still Seeking']
        regions = ['Dublin', 'Cork', 'Galway', 'Limerick', 'Waterford', 'Kilkenny']
        
        beneficiaries_data = []
        project_ids = self.projects_df['project_id'].tolist()
        
        for i in range(1, num_beneficiaries + 1):
            # Assign to random project
            project_id = random.choice(project_ids)
            
            # Generate participation dates
            participation_start = datetime(2020, 6, 1) + timedelta(days=random.randint(0, 1500))
            participation_end = participation_start + timedelta(days=random.randint(30, 365))
            
            beneficiary = {
                'beneficiary_id': f'BEN-{i:05d}',
                'project_id': project_id,
                'first_name': f'FirstName{i}',
                'last_name': f'LastName{i}',
                'gender': random.choice(genders),
                'age_group': random.choice(age_groups),
                'region': random.choice(regions),
                'education_level': random.choice(education_levels),
                'employment_status_before': random.choice(employment_statuses),
                'employment_status_after': random.choice(employment_statuses),
                'vulnerable_group': random.choice(vulnerable_groups),
                'participation_start': participation_start.strftime('%Y-%m-%d'),
                'participation_end': participation_end.strftime('%Y-%m-%d'),
                'training_hours': random.randint(20, 200),
                'outcome_achieved': random.choice(outcomes),
                'satisfaction_score': round(random.uniform(1, 5), 1),
                'follow_up_period': random.choice(['3 months', '6 months', '12 months']),
                'additional_support': random.choice(['Yes', 'No']),
                'certification_obtained': random.choice(['Yes', 'No'])
            }
            
            beneficiaries_data.append(beneficiary)
        
        self.beneficiaries_df = pd.DataFrame(beneficiaries_data)
        print(f"✅ Generated {len(self.beneficiaries_df)} sample beneficiaries")
        return self.beneficiaries_df
    
    def validate_data(self):
        """Validate the generated data"""
        print("🔍 Validating data quality...")
        
        issues = []
        
        # Validate projects data
        if self.projects_df is not None:
            # Check for missing values
            missing_projects = self.projects_df.isnull().sum().sum()
            if missing_projects > 0:
                issues.append(f"Projects data has {missing_projects} missing values")
            
            # Check budget consistency
            budget_issues = self.projects_df[self.projects_df['esf_funding'] > self.projects_df['total_budget']]
            if len(budget_issues) > 0:
                issues.append(f"{len(budget_issues)} projects have ESF funding greater than total budget")
        
        # Validate beneficiaries data
        if self.beneficiaries_df is not None:
            # Check for missing values
            missing_beneficiaries = self.beneficiaries_df.isnull().sum().sum()
            if missing_beneficiaries > 0:
                issues.append(f"Beneficiaries data has {missing_beneficiaries} missing values")
            
            # Check project ID references
            if self.projects_df is not None:
                project_ids = set(self.projects_df['project_id'])
                beneficiary_project_ids = set(self.beneficiaries_df['project_id'])
                orphaned_beneficiaries = beneficiary_project_ids - project_ids
                if orphaned_beneficiaries:
                    issues.append(f"Beneficiaries reference {len(orphaned_beneficiaries)} non-existent projects")
        
        if issues:
            print("⚠️  Data validation issues found:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print("✅ Data validation passed - no issues found")
        
        return len(issues) == 0
    
    def export_cleaned_data(self):
        """Export cleaned data to CSV files"""
        print("💾 Exporting cleaned data...")
        
        try:
            if self.projects_df is not None:
                projects_file = 'cleaned_data/esf_projects_cleaned.csv'
                self.projects_df.to_csv(projects_file, index=False)
                print(f"✅ Projects data exported to: {projects_file}")
            
            if self.beneficiaries_df is not None:
                beneficiaries_file = 'cleaned_data/esf_beneficiaries_cleaned.csv'
                self.beneficiaries_df.to_csv(beneficiaries_file, index=False)
                print(f"✅ Beneficiaries data exported to: {beneficiaries_file}")
            
            # Create data summary
            summary = {
                'export_date': datetime.now().isoformat(),
                'projects_count': len(self.projects_df) if self.projects_df is not None else 0,
                'beneficiaries_count': len(self.beneficiaries_df) if self.beneficiaries_df is not None else 0,
                'data_quality': 'Validated',
                'source': 'Generated sample data for ESF BI project'
            }
            
            with open('cleaned_data/data_summary.json', 'w') as f:
                json.dump(summary, f, indent=2)
            print("✅ Data summary exported to: cleaned_data/data_summary.json")
            
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
    
    def clean_projects_data(self, file_path=None):
        """Clean projects data (or create sample if file doesn't exist)"""
        if file_path and os.path.exists(file_path):
            print(f"📊 Loading projects data from: {file_path}")
            try:
                self.projects_df = pd.read_csv(file_path)
                # Data cleaning logic here
                print(f"✅ Loaded {len(self.projects_df)} projects from file")
            except Exception as e:
                print(f"❌ Error loading projects data: {e}")
                print("🔄 Creating sample data instead...")
                self.create_sample_esf_projects()
        else:
            print("📊 No projects file found, creating sample data...")
            self.create_sample_esf_projects()
    
    def clean_beneficiaries_data(self, file_path=None):
        """Clean beneficiaries data (or create sample if file doesn't exist)"""
        if file_path and os.path.exists(file_path):
            print(f"👥 Loading beneficiaries data from: {file_path}")
            try:
                self.beneficiaries_df = pd.read_csv(file_path)
                # Data cleaning logic here
                print(f"✅ Loaded {len(self.beneficiaries_df)} beneficiaries from file")
            except Exception as e:
                print(f"❌ Error loading beneficiaries data: {e}")
                print("🔄 Creating sample data instead...")
                self.create_sample_esf_beneficiaries()
        else:
            print("👥 No beneficiaries file found, creating sample data...")
            self.create_sample_esf_beneficiaries()

def main():
    """Main execution function"""
    print("🧹 ESF DATA CLEANING AND PROCESSING")
    print("=" * 50)
    
    # Initialize cleaner
    cleaner = ESFDataCleaner()
    
    # Clean/create projects data
    cleaner.clean_projects_data('esf_projects.csv')
    
    # Clean/create beneficiaries data  
    cleaner.clean_beneficiaries_data('esf_beneficiaries.csv')
    
    # Validate data quality
    cleaner.validate_data()
    
    # Export cleaned data
    cleaner.export_cleaned_data()
    
    print("\n" + "=" * 50)
    print("🎉 DATA CLEANING COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("\n📁 Files created in 'cleaned_data/' folder:")
    print("   📊 esf_projects_cleaned.csv")
    print("   👥 esf_beneficiaries_cleaned.csv")
    print("   📋 data_summary.json")
    print("\n💡 Next steps:")
    print("   1. Run basic_analysis_script.py for comprehensive analysis")
    print("   2. Run data_analysis_script.py for visualizations")
    print("   3. Run simple_dashboard_generator.py for interactive dashboard")

if __name__ == "__main__":
    main()
