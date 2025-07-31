#!/usr/bin/env python3
"""
ESF Data Analysis Script (Fixed Version)
======================================

This script provides basic analysis of ESF projects and beneficiaries data.
Fixed issues:
1. Better error handling for missing packages
2. Fallback to simple analysis if pandas unavailable
3. Proper file path handling

Usage:
    python basic_analysis_script_fixed.py
"""

import sys
import csv
import json
from datetime import datetime
import os

# Try to import pandas and numpy, with fallback
try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
    print("✅ Pandas and NumPy loaded successfully")
except ImportError as e:
    PANDAS_AVAILABLE = False
    print(f"⚠️  Pandas/NumPy not available: {e}")
    print("📋 Running in basic mode without advanced analytics")

class ESFAnalyzer:
    def __init__(self, projects_file=None, beneficiaries_file=None):
        self.projects_data = []
        self.beneficiaries_data = []
        self.projects_df = None
        self.beneficiaries_df = None
        
        if projects_file:
            self.load_data(projects_file, 'projects')
        if beneficiaries_file:
            self.load_data(beneficiaries_file, 'beneficiaries')
    
    def load_data(self, file_path, data_type):
        """Load data from CSV file with error handling"""
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return
        
        try:
            if PANDAS_AVAILABLE:
                # Use pandas if available
                if data_type == 'projects':
                    self.projects_df = pd.read_csv(file_path)
                    # Convert date columns
                    date_cols = ['start_date', 'end_date']
                    for col in date_cols:
                        if col in self.projects_df.columns:
                            self.projects_df[col] = pd.to_datetime(self.projects_df[col])
                    print(f"✅ Loaded {len(self.projects_df)} project records (pandas)")
                else:
                    self.beneficiaries_df = pd.read_csv(file_path)
                    date_cols = ['participation_start', 'participation_end']
                    for col in date_cols:
                        if col in self.beneficiaries_df.columns:
                            self.beneficiaries_df[col] = pd.to_datetime(self.beneficiaries_df[col])
                    print(f"✅ Loaded {len(self.beneficiaries_df)} beneficiary records (pandas)")
            else:
                # Fallback to basic CSV reading
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    data = list(reader)
                    
                if data_type == 'projects':
                    self.projects_data = data
                    print(f"✅ Loaded {len(self.projects_data)} project records (basic)")
                else:
                    self.beneficiaries_data = data
                    print(f"✅ Loaded {len(self.beneficiaries_data)} beneficiary records (basic)")
                    
        except Exception as e:
            print(f"❌ Error loading {data_type} data: {e}")
    
    def analyze_basic_stats(self):
        """Provide basic statistics analysis"""
        print("\\n" + "="*70)
        print("BASIC STATISTICAL ANALYSIS")
        print("="*70)
        
        if PANDAS_AVAILABLE and self.projects_df is not None:
            self._analyze_with_pandas()
        else:
            self._analyze_basic_mode()
    
    def _analyze_with_pandas(self):
        """Advanced analysis using pandas"""
        print("\\n📊 PROJECTS ANALYSIS (Advanced Mode):")
        
        if self.projects_df is not None:
            total_projects = len(self.projects_df)
            total_budget = self.projects_df['total_budget'].sum()
            avg_budget = self.projects_df['total_budget'].mean()
            
            print(f"   Total Projects: {total_projects:,}")
            print(f"   Total Budget: €{total_budget:,.2f}")
            print(f"   Average Budget: €{avg_budget:,.2f}")
            
            # Status distribution
            status_dist = self.projects_df['status'].value_counts()
            print(f"\\n   📈 Status Distribution:")
            for status, count in status_dist.items():
                percentage = (count / total_projects) * 100
                print(f"     {status}: {count:,} ({percentage:.1f}%)")
            
            # Performance metrics
            if 'target_achievement_rate' in self.projects_df.columns:
                avg_achievement = self.projects_df['target_achievement_rate'].mean()
                over_target = len(self.projects_df[self.projects_df['target_achievement_rate'] > 100])
                print(f"\\n   🎯 Performance Metrics:")
                print(f"     Average Achievement: {avg_achievement:.1f}%")
                print(f"     Projects Over Target: {over_target:,}")
        
        if self.beneficiaries_df is not None:
            print(f"\\n👥 BENEFICIARIES ANALYSIS (Advanced Mode):")
            total_beneficiaries = len(self.beneficiaries_df)
            print(f"   Total Beneficiaries: {total_beneficiaries:,}")
            
            if 'satisfaction_score' in self.beneficiaries_df.columns:
                avg_satisfaction = self.beneficiaries_df['satisfaction_score'].mean()
                print(f"   Average Satisfaction: {avg_satisfaction:.2f}/5")
    
    def _analyze_basic_mode(self):
        """Basic analysis without pandas"""
        print("\\n📊 PROJECTS ANALYSIS (Basic Mode):")
        
        if self.projects_data:
            total_projects = len(self.projects_data)
            print(f"   Total Projects: {total_projects:,}")
            
            # Calculate total budget
            try:
                budgets = [float(row.get('total_budget', 0)) for row in self.projects_data if row.get('total_budget')]
                total_budget = sum(budgets)
                avg_budget = total_budget / len(budgets) if budgets else 0
                print(f"   Total Budget: €{total_budget:,.2f}")
                print(f"   Average Budget: €{avg_budget:,.2f}")
            except ValueError:
                print("   Budget data contains non-numeric values")
            
            # Status distribution
            statuses = [row.get('status', 'Unknown') for row in self.projects_data]
            status_counts = {}
            for status in statuses:
                status_counts[status] = status_counts.get(status, 0) + 1
            
            print(f"\\n   📈 Status Distribution:")
            for status, count in status_counts.items():
                percentage = (count / total_projects) * 100
                print(f"     {status}: {count:,} ({percentage:.1f}%)")
        
        if self.beneficiaries_data:
            print(f"\\n👥 BENEFICIARIES ANALYSIS (Basic Mode):")
            total_beneficiaries = len(self.beneficiaries_data)
            print(f"   Total Beneficiaries: {total_beneficiaries:,}")
            
            # Gender distribution
            genders = [row.get('gender', 'Unknown') for row in self.beneficiaries_data]
            gender_counts = {}
            for gender in genders:
                gender_counts[gender] = gender_counts.get(gender, 0) + 1
            
            print(f"\\n   👥 Gender Distribution:")
            for gender, count in gender_counts.items():
                percentage = (count / total_beneficiaries) * 100
                print(f"     {gender}: {count:,} ({percentage:.1f}%)")
    
    def generate_summary_report(self):
        """Generate comprehensive summary"""
        print("\\n" + "="*70)
        print("ESF PROGRAM SUMMARY REPORT")
        print("="*70)
        
        # Basic counts
        project_count = len(self.projects_df) if PANDAS_AVAILABLE and self.projects_df is not None else len(self.projects_data)
        beneficiary_count = len(self.beneficiaries_df) if PANDAS_AVAILABLE and self.beneficiaries_df is not None else len(self.beneficiaries_data)
        
        print(f"\\n📋 OVERVIEW:")
        print(f"   📊 Total Projects: {project_count:,}")
        print(f"   👥 Total Beneficiaries: {beneficiary_count:,}")
        print(f"   🔧 Analysis Mode: {'Advanced (Pandas)' if PANDAS_AVAILABLE else 'Basic (Built-in)'}")
        print(f"   📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Quick insights
        print(f"\\n💡 KEY INSIGHTS:")
        if project_count > 0 and beneficiary_count > 0:
            ratio = beneficiary_count / project_count
            print(f"   📈 Average Beneficiaries per Project: {ratio:.1f}")
        
        if PANDAS_AVAILABLE and self.projects_df is not None:
            total_budget = self.projects_df['total_budget'].sum()
            cost_per_beneficiary = total_budget / beneficiary_count if beneficiary_count > 0 else 0
            print(f"   💰 Cost per Beneficiary: €{cost_per_beneficiary:,.2f}")
        
        print(f"\\n✅ Analysis completed successfully!")
        
        return {
            'project_count': project_count,
            'beneficiary_count': beneficiary_count,
            'analysis_mode': 'pandas' if PANDAS_AVAILABLE else 'basic',
            'timestamp': datetime.now().isoformat()
        }

def main():
    """Main execution function"""
    print("ESF Data Analysis Tool (Fixed Version)")
    print("=" * 50)
    
    # Check for data files
    projects_file = "cleaned_data/esf_projects_cleaned.csv"
    beneficiaries_file = "cleaned_data/esf_beneficiaries_cleaned.csv"
    
    if not os.path.exists(projects_file):
        print(f"❌ Projects file not found: {projects_file}")
        print("💡 Please run the data cleaning script first!")
        return
    
    if not os.path.exists(beneficiaries_file):
        print(f"❌ Beneficiaries file not found: {beneficiaries_file}")
        print("💡 Please run the data cleaning script first!")
        return
    
    # Initialize analyzer
    analyzer = ESFAnalyzer(
        projects_file=projects_file,
        beneficiaries_file=beneficiaries_file
    )
    
    # Perform analysis
    analyzer.analyze_basic_stats()
    
    # Generate summary
    summary = analyzer.generate_summary_report()
    
    # Save summary to file
    try:
        with open('analysis_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"\\n💾 Summary saved to: analysis_summary.json")
    except Exception as e:
        print(f"⚠️  Could not save summary: {e}")
    
    print("\\n🎉 Analysis completed!")

if __name__ == "__main__":
    main()
