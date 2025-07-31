#!/usr/bin/env python3
"""
ESF Data Analysis and Visualization Script
==========================================

This script provides comprehensive analysis and visualization of ESF projects and beneficiaries data.
It includes:
1. Data exploration and profiling
2. Statistical analysis
3. Data visualizations
4. Performance metrics calculation
5. Export of analysis results

Usage:
    python data_analysis_script.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ESFDataAnalyzer:
    def __init__(self, projects_file=None, beneficiaries_file=None):
        self.projects_df = None
        self.beneficiaries_df = None
        
        # Set plotting style
        plt.style.use('default')
        sns.set_palette("husl")
        
        if projects_file:
            self.load_projects_data(projects_file)
        if beneficiaries_file:
            self.load_beneficiaries_data(beneficiaries_file)
    
    def load_projects_data(self, file_path):
        """Load projects data from CSV file"""
        try:
            self.projects_df = pd.read_csv(file_path)
            # Convert date columns
            date_cols = ['start_date', 'end_date']
            for col in date_cols:
                if col in self.projects_df.columns:
                    self.projects_df[col] = pd.to_datetime(self.projects_df[col])
            print(f"Loaded {len(self.projects_df)} project records")
        except Exception as e:
            print(f"Error loading projects data: {e}")
    
    def load_beneficiaries_data(self, file_path):
        """Load beneficiaries data from CSV file"""
        try:
            self.beneficiaries_df = pd.read_csv(file_path)
            # Convert date columns
            date_cols = ['participation_start', 'participation_end']
            for col in date_cols:
                if col in self.beneficiaries_df.columns:
                    self.beneficiaries_df[col] = pd.to_datetime(self.beneficiaries_df[col])
            print(f"Loaded {len(self.beneficiaries_df)} beneficiary records")
        except Exception as e:
            print(f"Error loading beneficiaries data: {e}")
    
    def analyze_projects_overview(self):
        """Provide overview analysis of projects data"""
        if self.projects_df is None:
            print("No projects data available")
            return
        
        print("\\n" + "="*60)
        print("PROJECTS DATA ANALYSIS")
        print("="*60)
        
        # Basic statistics
        print(f"\\nTotal Projects: {len(self.projects_df)}")
        print(f"Date Range: {self.projects_df['start_date'].min().strftime('%Y-%m-%d')} to {self.projects_df['end_date'].max().strftime('%Y-%m-%d')}")
        
        # Financial overview
        total_budget = self.projects_df['total_budget'].sum()
        total_esf = self.projects_df['esf_funding'].sum()
        avg_budget = self.projects_df['total_budget'].mean()
        
        print(f"\\nFINANCIAL OVERVIEW:")
        print(f"Total Budget: €{total_budget:,.2f}")
        print(f"Total ESF Funding: €{total_esf:,.2f}")
        print(f"Average Project Budget: €{avg_budget:,.2f}")
        print(f"ESF Funding Rate: {(total_esf/total_budget*100):.1f}%")
        
        # Project status distribution
        print(f"\\nPROJECT STATUS DISTRIBUTION:")
        status_dist = self.projects_df['status'].value_counts()
        for status, count in status_dist.items():
            percentage = (count / len(self.projects_df)) * 100
            print(f"  {status}: {count} ({percentage:.1f}%)")
        
        # Project type distribution
        print(f"\\nPROJECT TYPE DISTRIBUTION:")
        type_dist = self.projects_df['project_type'].value_counts()
        for ptype, count in type_dist.items():
            percentage = (count / len(self.projects_df)) * 100
            print(f"  {ptype}: {count} ({percentage:.1f}%)")
        
        # Regional distribution
        print(f"\\nREGIONAL DISTRIBUTION:")
        region_dist = self.projects_df['region'].value_counts()
        for region, count in region_dist.items():
            percentage = (count / len(self.projects_df)) * 100
            print(f"  {region}: {count} ({percentage:.1f}%)")
        
        # Performance metrics
        if 'target_achievement_rate' in self.projects_df.columns:
            avg_achievement = self.projects_df['target_achievement_rate'].mean()
            over_target = len(self.projects_df[self.projects_df['target_achievement_rate'] > 100])
            print(f"\\nPERFORMANCE METRICS:")
            print(f"Average Target Achievement Rate: {avg_achievement:.1f}%")
            print(f"Projects Exceeding Target: {over_target} ({over_target/len(self.projects_df)*100:.1f}%)")
    
    def analyze_beneficiaries_overview(self):
        """Provide overview analysis of beneficiaries data"""
        if self.beneficiaries_df is None:
            print("No beneficiaries data available")
            return
        
        print("\\n" + "="*60)
        print("BENEFICIARIES DATA ANALYSIS")
        print("="*60)
        
        # Basic statistics
        print(f"\\nTotal Beneficiaries: {len(self.beneficiaries_df)}")
        
        # Demographics
        print(f"\\nDEMOGRAPHIC BREAKDOWN:")
        
        # Gender distribution
        gender_dist = self.beneficiaries_df['gender'].value_counts()
        print("Gender Distribution:")
        for gender, count in gender_dist.items():
            percentage = (count / len(self.beneficiaries_df)) * 100
            print(f"  {gender}: {count} ({percentage:.1f}%)")
        
        # Age group distribution
        age_dist = self.beneficiaries_df['age_group'].value_counts()
        print("\\nAge Group Distribution:")
        for age, count in age_dist.items():
            percentage = (count / len(self.beneficiaries_df)) * 100
            print(f"  {age}: {count} ({percentage:.1f}%)")
        
        # Education level distribution
        edu_dist = self.beneficiaries_df['education_level'].value_counts()
        print("\\nEducation Level Distribution:")
        for edu, count in edu_dist.items():
            percentage = (count / len(self.beneficiaries_df)) * 100
            print(f"  {edu}: {count} ({percentage:.1f}%)")
        
        # Employment outcomes
        if 'outcome_achieved' in self.beneficiaries_df.columns:
            outcome_dist = self.beneficiaries_df['outcome_achieved'].value_counts()
            print("\\nEMPLOYMENT OUTCOMES:")
            for outcome, count in outcome_dist.items():
                percentage = (count / len(self.beneficiaries_df)) * 100
                print(f"  {outcome}: {count} ({percentage:.1f}%)")
        
        # Vulnerable groups
        if 'vulnerable_group' in self.beneficiaries_df.columns:
            vulnerable_dist = self.beneficiaries_df['vulnerable_group'].value_counts()
            print("\\nVULNERABLE GROUPS:")
            for group, count in vulnerable_dist.items():
                percentage = (count / len(self.beneficiaries_df)) * 100
                print(f"  {group}: {count} ({percentage:.1f}%)")
        
        # Training statistics
        if 'training_hours' in self.beneficiaries_df.columns:
            avg_hours = self.beneficiaries_df['training_hours'].mean()
            total_hours = self.beneficiaries_df['training_hours'].sum()
            print(f"\\nTRAINING STATISTICS:")
            print(f"Average Training Hours per Beneficiary: {avg_hours:.1f}")
            print(f"Total Training Hours Delivered: {total_hours:,.0f}")
        
        # Satisfaction scores
        if 'satisfaction_score' in self.beneficiaries_df.columns:
            avg_satisfaction = self.beneficiaries_df['satisfaction_score'].mean()
            high_satisfaction = len(self.beneficiaries_df[self.beneficiaries_df['satisfaction_score'] >= 4])
            print(f"\\nSATISFACTION METRICS:")
            print(f"Average Satisfaction Score: {avg_satisfaction:.2f}/5")
            print(f"High Satisfaction (4-5): {high_satisfaction} ({high_satisfaction/len(self.beneficiaries_df)*100:.1f}%)")
    
    def create_visualizations(self, save_plots=True):
        """Create comprehensive visualizations"""
        print("\\n" + "="*60)
        print("CREATING VISUALIZATIONS")
        print("="*60)
        
        # Set up the plotting parameters
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        
        # Projects visualizations
        if self.projects_df is not None:
            self._create_projects_visualizations(save_plots)
        
        # Beneficiaries visualizations
        if self.beneficiaries_df is not None:
            self._create_beneficiaries_visualizations(save_plots)
        
        # Combined analysis if both datasets exist
        if self.projects_df is not None and self.beneficiaries_df is not None:
            self._create_combined_visualizations(save_plots)
    
    def _create_projects_visualizations(self, save_plots):
        """Create projects-specific visualizations"""
        
        # 1. Project Status Distribution (Pie Chart)
        plt.figure(figsize=(10, 6))
        status_counts = self.projects_df['status'].value_counts()
        plt.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
        plt.title('Project Status Distribution', fontsize=14, fontweight='bold')
        plt.axis('equal')
        if save_plots:
            plt.savefig('cleaned_data/project_status_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 2. Budget Analysis (Bar Chart)
        plt.figure(figsize=(12, 6))
        budget_by_type = self.projects_df.groupby('project_type').agg({
            'total_budget': 'sum',
            'esf_funding': 'sum'
        })
        
        x = range(len(budget_by_type.index))
        width = 0.35
        
        plt.bar([i - width/2 for i in x], budget_by_type['total_budget'], width, 
                label='Total Budget', alpha=0.8)
        plt.bar([i + width/2 for i in x], budget_by_type['esf_funding'], width, 
                label='ESF Funding', alpha=0.8)
        
        plt.xlabel('Project Type')
        plt.ylabel('Budget (€)')
        plt.title('Budget Analysis by Project Type')
        plt.xticks(x, budget_by_type.index, rotation=45)
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        
        if save_plots:
            plt.savefig('cleaned_data/budget_analysis_by_type.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 3. Target Achievement Rate Distribution
        if 'target_achievement_rate' in self.projects_df.columns:
            plt.figure(figsize=(10, 6))
            plt.hist(self.projects_df['target_achievement_rate'], bins=20, alpha=0.7, edgecolor='black')
            plt.axvline(self.projects_df['target_achievement_rate'].mean(), color='red', 
                       linestyle='--', label=f'Mean: {self.projects_df["target_achievement_rate"].mean():.1f}%')
            plt.axvline(100, color='green', linestyle='--', label='Target (100%)')
            plt.xlabel('Target Achievement Rate (%)')
            plt.ylabel('Number of Projects')
            plt.title('Distribution of Target Achievement Rates')
            plt.legend()
            plt.grid(alpha=0.3)
            
            if save_plots:
                plt.savefig('cleaned_data/target_achievement_distribution.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def _create_beneficiaries_visualizations(self, save_plots):
        """Create beneficiaries-specific visualizations"""
        
        # 1. Demographics Overview (Subplot)
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Gender distribution
        gender_counts = self.beneficiaries_df['gender'].value_counts()
        axes[0, 0].pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%')
        axes[0, 0].set_title('Gender Distribution')
        
        # Age group distribution
        age_counts = self.beneficiaries_df['age_group'].value_counts()
        axes[0, 1].bar(age_counts.index, age_counts.values)
        axes[0, 1].set_title('Age Group Distribution')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Education level distribution
        edu_counts = self.beneficiaries_df['education_level'].value_counts()
        axes[1, 0].bar(edu_counts.index, edu_counts.values)
        axes[1, 0].set_title('Education Level Distribution')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Employment outcomes
        if 'outcome_achieved' in self.beneficiaries_df.columns:
            outcome_counts = self.beneficiaries_df['outcome_achieved'].value_counts()
            axes[1, 1].bar(outcome_counts.index, outcome_counts.values)
            axes[1, 1].set_title('Employment Outcomes')
            axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        if save_plots:
            plt.savefig('cleaned_data/beneficiaries_demographics.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 2. Training Hours Analysis
        if 'training_hours' in self.beneficiaries_df.columns:
            plt.figure(figsize=(12, 6))
            
            # Create subplots for training hours analysis
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Histogram of training hours
            ax1.hist(self.beneficiaries_df['training_hours'], bins=20, alpha=0.7, edgecolor='black')
            ax1.axvline(self.beneficiaries_df['training_hours'].mean(), color='red', 
                       linestyle='--', label=f'Mean: {self.beneficiaries_df["training_hours"].mean():.1f} hours')
            ax1.set_xlabel('Training Hours')
            ax1.set_ylabel('Number of Beneficiaries')
            ax1.set_title('Distribution of Training Hours')
            ax1.legend()
            ax1.grid(alpha=0.3)
            
            # Training hours by education level
            if 'education_level' in self.beneficiaries_df.columns:
                edu_training = self.beneficiaries_df.groupby('education_level')['training_hours'].mean()
                ax2.bar(edu_training.index, edu_training.values)
                ax2.set_xlabel('Education Level')
                ax2.set_ylabel('Average Training Hours')
                ax2.set_title('Average Training Hours by Education Level')
                ax2.tick_params(axis='x', rotation=45)
                ax2.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            if save_plots:
                plt.savefig('cleaned_data/training_hours_analysis.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def _create_combined_visualizations(self, save_plots):
        """Create visualizations combining both datasets"""
        
        # Projects and beneficiaries relationship
        if 'project_id' in self.beneficiaries_df.columns:
            # Beneficiaries per project
            beneficiaries_per_project = self.beneficiaries_df['project_id'].value_counts()
            
            # Merge with projects data
            projects_with_counts = self.projects_df.merge(
                beneficiaries_per_project.to_frame('actual_beneficiaries'),
                left_on='project_id',
                right_index=True,
                how='left'
            )
            
            # Target vs Actual Beneficiaries
            plt.figure(figsize=(12, 8))
            plt.scatter(projects_with_counts['beneficiaries_target'], 
                       projects_with_counts['actual_beneficiaries'],
                       alpha=0.6, s=50)
            
            # Add diagonal line for perfect match
            max_val = max(projects_with_counts['beneficiaries_target'].max(),
                         projects_with_counts['actual_beneficiaries'].max())
            plt.plot([0, max_val], [0, max_val], 'r--', label='Perfect Match')
            
            plt.xlabel('Target Beneficiaries')
            plt.ylabel('Actual Beneficiaries')
            plt.title('Target vs Actual Beneficiaries by Project')
            plt.legend()
            plt.grid(alpha=0.3)
            
            if save_plots:
                plt.savefig('cleaned_data/target_vs_actual_beneficiaries.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def calculate_kpis(self):
        """Calculate Key Performance Indicators"""
        print("\\n" + "="*60)
        print("KEY PERFORMANCE INDICATORS (KPIs)")
        print("="*60)
        
        kpis = {}
        
        # Projects KPIs
        if self.projects_df is not None:
            kpis['total_projects'] = len(self.projects_df)
            kpis['total_budget'] = self.projects_df['total_budget'].sum()
            kpis['total_esf_funding'] = self.projects_df['esf_funding'].sum()
            kpis['avg_project_budget'] = self.projects_df['total_budget'].mean()
            kpis['esf_funding_rate'] = (kpis['total_esf_funding'] / kpis['total_budget']) * 100
            
            if 'target_achievement_rate' in self.projects_df.columns:
                kpis['avg_target_achievement'] = self.projects_df['target_achievement_rate'].mean()
                kpis['projects_over_target'] = len(self.projects_df[self.projects_df['target_achievement_rate'] > 100])
                kpis['projects_over_target_rate'] = (kpis['projects_over_target'] / len(self.projects_df)) * 100
        
        # Beneficiaries KPIs
        if self.beneficiaries_df is not None:
            kpis['total_beneficiaries'] = len(self.beneficiaries_df)
            
            if 'training_hours' in self.beneficiaries_df.columns:
                kpis['total_training_hours'] = self.beneficiaries_df['training_hours'].sum()
                kpis['avg_training_hours'] = self.beneficiaries_df['training_hours'].mean()
            
            if 'satisfaction_score' in self.beneficiaries_df.columns:
                kpis['avg_satisfaction'] = self.beneficiaries_df['satisfaction_score'].mean()
                kpis['high_satisfaction_count'] = len(self.beneficiaries_df[self.beneficiaries_df['satisfaction_score'] >= 4])
                kpis['high_satisfaction_rate'] = (kpis['high_satisfaction_count'] / len(self.beneficiaries_df)) * 100
            
            if 'outcome_achieved' in self.beneficiaries_df.columns:
                employment_outcomes = ['Employed', 'Self-employed']
                successful_outcomes = self.beneficiaries_df[self.beneficiaries_df['outcome_achieved'].isin(employment_outcomes)]
                kpis['employment_success_count'] = len(successful_outcomes)
                kpis['employment_success_rate'] = (len(successful_outcomes) / len(self.beneficiaries_df)) * 100
        
        # Display KPIs
        print("\\nPROJECT KPIs:")
        if 'total_projects' in kpis:
            print(f"  Total Projects: {kpis['total_projects']:,}")
            print(f"  Total Budget: €{kpis['total_budget']:,.2f}")
            print(f"  Total ESF Funding: €{kpis['total_esf_funding']:,.2f}")
            print(f"  Average Project Budget: €{kpis['avg_project_budget']:,.2f}")
            print(f"  ESF Funding Rate: {kpis['esf_funding_rate']:.1f}%")
            
            if 'avg_target_achievement' in kpis:
                print(f"  Average Target Achievement: {kpis['avg_target_achievement']:.1f}%")
                print(f"  Projects Over Target: {kpis['projects_over_target']} ({kpis['projects_over_target_rate']:.1f}%)")
        
        print("\\nBENEFICIARY KPIs:")
        if 'total_beneficiaries' in kpis:
            print(f"  Total Beneficiaries: {kpis['total_beneficiaries']:,}")
            
            if 'total_training_hours' in kpis:
                print(f"  Total Training Hours: {kpis['total_training_hours']:,.0f}")
                print(f"  Average Training Hours per Beneficiary: {kpis['avg_training_hours']:.1f}")
            
            if 'avg_satisfaction' in kpis:
                print(f"  Average Satisfaction Score: {kpis['avg_satisfaction']:.2f}/5")
                print(f"  High Satisfaction Rate: {kpis['high_satisfaction_rate']:.1f}%")
            
            if 'employment_success_rate' in kpis:
                print(f"  Employment Success Rate: {kpis['employment_success_rate']:.1f}%")
        
        return kpis
    
    def export_analysis_report(self, filename="esf_analysis_report.txt"):
        """Export comprehensive analysis report"""
        import sys
        from io import StringIO
        
        # Capture all print output
        old_stdout = sys.stdout
        sys.stdout = buffer = StringIO()
        
        # Run all analyses
        self.analyze_projects_overview()
        self.analyze_beneficiaries_overview()
        kpis = self.calculate_kpis()
        
        # Get the captured output
        output = buffer.getvalue()
        sys.stdout = old_stdout
        
        # Write to file
        try:
            with open(f"cleaned_data/{filename}", 'w', encoding='utf-8') as f:
                f.write(f"ESF DATA ANALYSIS REPORT\\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
                f.write("="*80 + "\\n\\n")
                f.write(output)
            
            print(f"Analysis report exported to: cleaned_data/{filename}")
        except Exception as e:
            print(f"Error exporting report: {e}")

def main():
    """Main execution function"""
    print("ESF Data Analysis and Visualization Tool")
    print("=" * 50)
    
    # Initialize analyzer with cleaned data files
    analyzer = ESFDataAnalyzer(
        projects_file="cleaned_data/esf_projects_cleaned.csv",
        beneficiaries_file="cleaned_data/esf_beneficiaries_cleaned.csv"
    )
    
    # Perform comprehensive analysis
    analyzer.analyze_projects_overview()
    analyzer.analyze_beneficiaries_overview()
    
    # Calculate KPIs
    kpis = analyzer.calculate_kpis()
    
    # Create visualizations
    analyzer.create_visualizations(save_plots=True)
    
    # Export analysis report
    analyzer.export_analysis_report()
    
    print("\\n" + "="*60)
    print("ANALYSIS COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\\nFiles generated:")
    print("  - cleaned_data/esf_analysis_report.txt")
    print("  - cleaned_data/project_status_distribution.png")
    print("  - cleaned_data/budget_analysis_by_type.png")
    print("  - cleaned_data/target_achievement_distribution.png")
    print("  - cleaned_data/beneficiaries_demographics.png")
    print("  - cleaned_data/training_hours_analysis.png")
    print("  - cleaned_data/target_vs_actual_beneficiaries.png")

if __name__ == "__main__":
    main()
