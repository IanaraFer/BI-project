#!/usr/bin/env python3
"""
ESF Data Analysis Script (Basic Version)
=======================================

This script provides basic analysis of ESF projects and beneficiaries data without requiring
additional visualization libraries. It focuses on:
1. Data exploration and statistics
2. Performance metrics calculation
3. Comprehensive reporting
4. Data quality assessment

Usage:
    python basic_analysis_script.py
"""

import pandas as pd
import numpy as np
from datetime import datetime
import csv
import json

class ESFBasicAnalyzer:
    def __init__(self, projects_file=None, beneficiaries_file=None):
        self.projects_df = None
        self.beneficiaries_df = None
        
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
        """Provide comprehensive overview analysis of projects data"""
        if self.projects_df is None:
            print("No projects data available")
            return {}
        
        print("\\n" + "="*70)
        print("COMPREHENSIVE PROJECTS DATA ANALYSIS")
        print("="*70)
        
        analysis = {}
        
        # Basic statistics
        analysis['total_projects'] = len(self.projects_df)
        analysis['date_range'] = {
            'start': self.projects_df['start_date'].min().strftime('%Y-%m-%d'),
            'end': self.projects_df['end_date'].max().strftime('%Y-%m-%d')
        }
        
        print(f"\\n📊 BASIC STATISTICS:")
        print(f"   Total Projects: {analysis['total_projects']:,}")
        print(f"   Date Range: {analysis['date_range']['start']} to {analysis['date_range']['end']}")
        
        # Financial analysis
        financial_stats = {
            'total_budget': self.projects_df['total_budget'].sum(),
            'total_esf_funding': self.projects_df['esf_funding'].sum(),
            'avg_budget': self.projects_df['total_budget'].mean(),
            'median_budget': self.projects_df['total_budget'].median(),
            'min_budget': self.projects_df['total_budget'].min(),
            'max_budget': self.projects_df['total_budget'].max()
        }
        
        financial_stats['esf_funding_rate'] = (financial_stats['total_esf_funding'] / financial_stats['total_budget']) * 100
        analysis['financial'] = financial_stats
        
        print(f"\\n💰 FINANCIAL OVERVIEW:")
        print(f"   Total Budget: €{financial_stats['total_budget']:,.2f}")
        print(f"   Total ESF Funding: €{financial_stats['total_esf_funding']:,.2f}")
        print(f"   ESF Funding Rate: {financial_stats['esf_funding_rate']:.1f}%")
        print(f"   Average Project Budget: €{financial_stats['avg_budget']:,.2f}")
        print(f"   Median Project Budget: €{financial_stats['median_budget']:,.2f}")
        print(f"   Budget Range: €{financial_stats['min_budget']:,.2f} - €{financial_stats['max_budget']:,.2f}")
        
        # Project status analysis
        status_dist = self.projects_df['status'].value_counts()
        analysis['status_distribution'] = status_dist.to_dict()
        
        print(f"\\n📈 PROJECT STATUS DISTRIBUTION:")
        for status, count in status_dist.items():
            percentage = (count / len(self.projects_df)) * 100
            print(f"   {status}: {count:,} ({percentage:.1f}%)")
        
        # Project type analysis
        type_dist = self.projects_df['project_type'].value_counts()
        analysis['type_distribution'] = type_dist.to_dict()
        
        print(f"\\n🎯 PROJECT TYPE DISTRIBUTION:")
        for ptype, count in type_dist.items():
            percentage = (count / len(self.projects_df)) * 100
            print(f"   {ptype}: {count:,} ({percentage:.1f}%)")
        
        # Regional analysis
        region_dist = self.projects_df['region'].value_counts()
        analysis['regional_distribution'] = region_dist.to_dict()
        
        print(f"\\n🌍 REGIONAL DISTRIBUTION:")
        for region, count in region_dist.items():
            percentage = (count / len(self.projects_df)) * 100
            print(f"   {region}: {count:,} ({percentage:.1f}%)")
        
        # Performance metrics
        if 'target_achievement_rate' in self.projects_df.columns:
            performance_stats = {
                'avg_achievement': self.projects_df['target_achievement_rate'].mean(),
                'median_achievement': self.projects_df['target_achievement_rate'].median(),
                'over_target_count': len(self.projects_df[self.projects_df['target_achievement_rate'] > 100]),
                'under_target_count': len(self.projects_df[self.projects_df['target_achievement_rate'] < 100]),
                'exactly_target_count': len(self.projects_df[self.projects_df['target_achievement_rate'] == 100])
            }
            
            performance_stats['over_target_rate'] = (performance_stats['over_target_count'] / len(self.projects_df)) * 100
            performance_stats['under_target_rate'] = (performance_stats['under_target_count'] / len(self.projects_df)) * 100
            analysis['performance'] = performance_stats
            
            print(f"\\n🎯 PERFORMANCE METRICS:")
            print(f"   Average Target Achievement: {performance_stats['avg_achievement']:.1f}%")
            print(f"   Median Target Achievement: {performance_stats['median_achievement']:.1f}%")
            print(f"   Projects Exceeding Target: {performance_stats['over_target_count']:,} ({performance_stats['over_target_rate']:.1f}%)")
            print(f"   Projects Below Target: {performance_stats['under_target_count']:,} ({performance_stats['under_target_rate']:.1f}%)")
            print(f"   Projects Meeting Exact Target: {performance_stats['exactly_target_count']:,}")
        
        # Budget efficiency analysis
        budget_by_type = self.projects_df.groupby('project_type').agg({
            'total_budget': ['sum', 'mean', 'count'],
            'esf_funding': ['sum', 'mean']
        }).round(2)
        
        print(f"\\n💼 BUDGET ANALYSIS BY PROJECT TYPE:")
        for ptype in budget_by_type.index:
            total_budget = budget_by_type.loc[ptype, ('total_budget', 'sum')]
            avg_budget = budget_by_type.loc[ptype, ('total_budget', 'mean')]
            project_count = budget_by_type.loc[ptype, ('total_budget', 'count')]
            esf_funding = budget_by_type.loc[ptype, ('esf_funding', 'sum')]
            
            print(f"   {ptype}:")
            print(f"     Projects: {project_count:,}")
            print(f"     Total Budget: €{total_budget:,.2f}")
            print(f"     Average Budget: €{avg_budget:,.2f}")
            print(f"     ESF Funding: €{esf_funding:,.2f}")
        
        return analysis
    
    def analyze_beneficiaries_overview(self):
        """Provide comprehensive overview analysis of beneficiaries data"""
        if self.beneficiaries_df is None:
            print("No beneficiaries data available")
            return {}
        
        print("\\n" + "="*70)
        print("COMPREHENSIVE BENEFICIARIES DATA ANALYSIS")
        print("="*70)
        
        analysis = {}
        
        # Basic statistics
        analysis['total_beneficiaries'] = len(self.beneficiaries_df)
        
        print(f"\\n📊 BASIC STATISTICS:")
        print(f"   Total Beneficiaries: {analysis['total_beneficiaries']:,}")
        
        # Demographics analysis
        print(f"\\n👥 DEMOGRAPHIC BREAKDOWN:")
        
        # Gender distribution
        gender_dist = self.beneficiaries_df['gender'].value_counts()
        analysis['gender_distribution'] = gender_dist.to_dict()
        
        print("   Gender Distribution:")
        for gender, count in gender_dist.items():
            percentage = (count / len(self.beneficiaries_df)) * 100
            print(f"     {gender}: {count:,} ({percentage:.1f}%)")
        
        # Age group distribution
        age_dist = self.beneficiaries_df['age_group'].value_counts()
        analysis['age_distribution'] = age_dist.to_dict()
        
        print("\\n   Age Group Distribution:")
        for age, count in age_dist.items():
            percentage = (count / len(self.beneficiaries_df)) * 100
            print(f"     {age}: {count:,} ({percentage:.1f}%)")
        
        # Education level distribution
        edu_dist = self.beneficiaries_df['education_level'].value_counts()
        analysis['education_distribution'] = edu_dist.to_dict()
        
        print("\\n   Education Level Distribution:")
        for edu, count in edu_dist.items():
            percentage = (count / len(self.beneficiaries_df)) * 100
            print(f"     {edu}: {count:,} ({percentage:.1f}%)")
        
        # Employment status analysis
        if 'employment_status_before' in self.beneficiaries_df.columns and 'employment_status_after' in self.beneficiaries_df.columns:
            before_dist = self.beneficiaries_df['employment_status_before'].value_counts()
            after_dist = self.beneficiaries_df['employment_status_after'].value_counts()
            
            analysis['employment_before'] = before_dist.to_dict()
            analysis['employment_after'] = after_dist.to_dict()
            
            print(f"\\n💼 EMPLOYMENT STATUS ANALYSIS:")
            print("   Before Participation:")
            for status, count in before_dist.items():
                percentage = (count / len(self.beneficiaries_df)) * 100
                print(f"     {status}: {count:,} ({percentage:.1f}%)")
            
            print("\\n   After Participation:")
            for status, count in after_dist.items():
                percentage = (count / len(self.beneficiaries_df)) * 100
                print(f"     {status}: {count:,} ({percentage:.1f}%)")
        
        # Employment outcomes
        if 'outcome_achieved' in self.beneficiaries_df.columns:
            outcome_dist = self.beneficiaries_df['outcome_achieved'].value_counts()
            analysis['outcome_distribution'] = outcome_dist.to_dict()
            
            print(f"\\n🎯 EMPLOYMENT OUTCOMES:")
            for outcome, count in outcome_dist.items():
                percentage = (count / len(self.beneficiaries_df)) * 100
                print(f"   {outcome}: {count:,} ({percentage:.1f}%)")
        
        # Vulnerable groups analysis
        if 'vulnerable_group' in self.beneficiaries_df.columns:
            vulnerable_dist = self.beneficiaries_df['vulnerable_group'].value_counts()
            analysis['vulnerable_groups'] = vulnerable_dist.to_dict()
            
            print(f"\\n🏥 VULNERABLE GROUPS:")
            for group, count in vulnerable_dist.items():
                percentage = (count / len(self.beneficiaries_df)) * 100
                print(f"   {group}: {count:,} ({percentage:.1f}%)")
        
        # Training statistics
        if 'training_hours' in self.beneficiaries_df.columns:
            training_stats = {
                'total_hours': self.beneficiaries_df['training_hours'].sum(),
                'avg_hours': self.beneficiaries_df['training_hours'].mean(),
                'median_hours': self.beneficiaries_df['training_hours'].median(),
                'min_hours': self.beneficiaries_df['training_hours'].min(),
                'max_hours': self.beneficiaries_df['training_hours'].max()
            }
            analysis['training_stats'] = training_stats
            
            print(f"\\n📚 TRAINING STATISTICS:")
            print(f"   Total Training Hours Delivered: {training_stats['total_hours']:,.0f}")
            print(f"   Average Hours per Beneficiary: {training_stats['avg_hours']:.1f}")
            print(f"   Median Hours per Beneficiary: {training_stats['median_hours']:.1f}")
            print(f"   Training Hours Range: {training_stats['min_hours']:.0f} - {training_stats['max_hours']:.0f}")
        
        # Satisfaction analysis
        if 'satisfaction_score' in self.beneficiaries_df.columns:
            satisfaction_stats = {
                'avg_satisfaction': self.beneficiaries_df['satisfaction_score'].mean(),
                'median_satisfaction': self.beneficiaries_df['satisfaction_score'].median(),
                'high_satisfaction_count': len(self.beneficiaries_df[self.beneficiaries_df['satisfaction_score'] >= 4]),
                'low_satisfaction_count': len(self.beneficiaries_df[self.beneficiaries_df['satisfaction_score'] <= 2])
            }
            
            satisfaction_stats['high_satisfaction_rate'] = (satisfaction_stats['high_satisfaction_count'] / len(self.beneficiaries_df)) * 100
            satisfaction_stats['low_satisfaction_rate'] = (satisfaction_stats['low_satisfaction_count'] / len(self.beneficiaries_df)) * 100
            analysis['satisfaction_stats'] = satisfaction_stats
            
            print(f"\\n😊 SATISFACTION METRICS:")
            print(f"   Average Satisfaction Score: {satisfaction_stats['avg_satisfaction']:.2f}/5")
            print(f"   Median Satisfaction Score: {satisfaction_stats['median_satisfaction']:.2f}/5")
            print(f"   High Satisfaction (4-5): {satisfaction_stats['high_satisfaction_count']:,} ({satisfaction_stats['high_satisfaction_rate']:.1f}%)")
            print(f"   Low Satisfaction (1-2): {satisfaction_stats['low_satisfaction_count']:,} ({satisfaction_stats['low_satisfaction_rate']:.1f}%)")
        
        # Regional analysis for beneficiaries
        if 'region' in self.beneficiaries_df.columns:
            beneficiary_region_dist = self.beneficiaries_df['region'].value_counts()
            analysis['beneficiary_regional_distribution'] = beneficiary_region_dist.to_dict()
            
            print(f"\\n🌍 REGIONAL DISTRIBUTION (BENEFICIARIES):")
            for region, count in beneficiary_region_dist.items():
                percentage = (count / len(self.beneficiaries_df)) * 100
                print(f"   {region}: {count:,} ({percentage:.1f}%)")
        
        return analysis
    
    def analyze_cross_dataset_relationships(self):
        """Analyze relationships between projects and beneficiaries"""
        if self.projects_df is None or self.beneficiaries_df is None:
            print("Both datasets required for cross-analysis")
            return {}
        
        print("\\n" + "="*70)
        print("CROSS-DATASET RELATIONSHIP ANALYSIS")
        print("="*70)
        
        analysis = {}
        
        # Beneficiaries per project
        if 'project_id' in self.beneficiaries_df.columns:
            beneficiaries_per_project = self.beneficiaries_df['project_id'].value_counts()
            
            # Merge with projects data
            projects_with_counts = self.projects_df.merge(
                beneficiaries_per_project.to_frame('actual_beneficiaries'),
                left_on='project_id',
                right_index=True,
                how='left'
            )
            
            # Fill NaN values with 0 for projects with no beneficiaries
            projects_with_counts['actual_beneficiaries'] = projects_with_counts['actual_beneficiaries'].fillna(0)
            
            # Calculate achievement rates
            projects_with_counts['achievement_rate'] = (
                projects_with_counts['actual_beneficiaries'] / 
                projects_with_counts['beneficiaries_target'] * 100
            ).round(2)
            
            analysis['projects_with_beneficiaries'] = len(projects_with_counts[projects_with_counts['actual_beneficiaries'] > 0])
            analysis['projects_without_beneficiaries'] = len(projects_with_counts[projects_with_counts['actual_beneficiaries'] == 0])
            
            print(f"\\n🔗 PROJECT-BENEFICIARY RELATIONSHIPS:")
            print(f"   Projects with Beneficiaries: {analysis['projects_with_beneficiaries']:,}")
            print(f"   Projects without Beneficiaries: {analysis['projects_without_beneficiaries']:,}")
            
            # Performance by project type
            performance_by_type = projects_with_counts.groupby('project_type').agg({
                'achievement_rate': ['mean', 'median', 'count'],
                'actual_beneficiaries': ['sum', 'mean'],
                'total_budget': 'sum'
            }).round(2)
            
            print(f"\\n📊 PERFORMANCE BY PROJECT TYPE:")
            for ptype in performance_by_type.index:
                avg_achievement = performance_by_type.loc[ptype, ('achievement_rate', 'mean')]
                total_beneficiaries = performance_by_type.loc[ptype, ('actual_beneficiaries', 'sum')]
                avg_beneficiaries = performance_by_type.loc[ptype, ('actual_beneficiaries', 'mean')]
                project_count = performance_by_type.loc[ptype, ('achievement_rate', 'count')]
                total_budget = performance_by_type.loc[ptype, ('total_budget', 'sum')]
                
                print(f"   {ptype}:")
                print(f"     Projects: {project_count:.0f}")
                print(f"     Average Achievement Rate: {avg_achievement:.1f}%")
                print(f"     Total Beneficiaries: {total_beneficiaries:.0f}")
                print(f"     Avg Beneficiaries per Project: {avg_beneficiaries:.1f}")
                print(f"     Total Budget: €{total_budget:,.2f}")
                
                if total_beneficiaries > 0:
                    cost_per_beneficiary = total_budget / total_beneficiaries
                    print(f"     Cost per Beneficiary: €{cost_per_beneficiary:,.2f}")
        
        return analysis
    
    def calculate_comprehensive_kpis(self):
        """Calculate comprehensive Key Performance Indicators"""
        print("\\n" + "="*70)
        print("COMPREHENSIVE KEY PERFORMANCE INDICATORS (KPIs)")
        print("="*70)
        
        kpis = {}
        
        # Projects KPIs
        if self.projects_df is not None:
            project_kpis = {
                'total_projects': len(self.projects_df),
                'total_budget': self.projects_df['total_budget'].sum(),
                'total_esf_funding': self.projects_df['esf_funding'].sum(),
                'avg_project_budget': self.projects_df['total_budget'].mean(),
                'median_project_budget': self.projects_df['total_budget'].median(),
            }
            
            project_kpis['esf_funding_rate'] = (project_kpis['total_esf_funding'] / project_kpis['total_budget']) * 100
            
            if 'target_achievement_rate' in self.projects_df.columns:
                project_kpis['avg_target_achievement'] = self.projects_df['target_achievement_rate'].mean()
                project_kpis['projects_over_target'] = len(self.projects_df[self.projects_df['target_achievement_rate'] > 100])
                project_kpis['projects_over_target_rate'] = (project_kpis['projects_over_target'] / len(self.projects_df)) * 100
            
            # Status-based KPIs
            status_counts = self.projects_df['status'].value_counts()
            for status in status_counts.index:
                project_kpis[f'{status.lower()}_projects_count'] = status_counts[status]
                project_kpis[f'{status.lower()}_projects_rate'] = (status_counts[status] / len(self.projects_df)) * 100
            
            kpis['projects'] = project_kpis
        
        # Beneficiaries KPIs
        if self.beneficiaries_df is not None:
            beneficiary_kpis = {
                'total_beneficiaries': len(self.beneficiaries_df),
            }
            
            if 'training_hours' in self.beneficiaries_df.columns:
                beneficiary_kpis['total_training_hours'] = self.beneficiaries_df['training_hours'].sum()
                beneficiary_kpis['avg_training_hours'] = self.beneficiaries_df['training_hours'].mean()
                beneficiary_kpis['median_training_hours'] = self.beneficiaries_df['training_hours'].median()
            
            if 'satisfaction_score' in self.beneficiaries_df.columns:
                beneficiary_kpis['avg_satisfaction'] = self.beneficiaries_df['satisfaction_score'].mean()
                beneficiary_kpis['high_satisfaction_count'] = len(self.beneficiaries_df[self.beneficiaries_df['satisfaction_score'] >= 4])
                beneficiary_kpis['high_satisfaction_rate'] = (beneficiary_kpis['high_satisfaction_count'] / len(self.beneficiaries_df)) * 100
            
            if 'outcome_achieved' in self.beneficiaries_df.columns:
                employment_outcomes = ['Employed', 'Self-employed']
                successful_outcomes = self.beneficiaries_df[self.beneficiaries_df['outcome_achieved'].isin(employment_outcomes)]
                beneficiary_kpis['employment_success_count'] = len(successful_outcomes)
                beneficiary_kpis['employment_success_rate'] = (len(successful_outcomes) / len(self.beneficiaries_df)) * 100
            
            # Gender diversity KPIs
            if 'gender' in self.beneficiaries_df.columns:
                gender_counts = self.beneficiaries_df['gender'].value_counts()
                for gender in gender_counts.index:
                    beneficiary_kpis[f'{gender.lower()}_count'] = gender_counts[gender]
                    beneficiary_kpis[f'{gender.lower()}_rate'] = (gender_counts[gender] / len(self.beneficiaries_df)) * 100
            
            kpis['beneficiaries'] = beneficiary_kpis
        
        # Combined KPIs
        if self.projects_df is not None and self.beneficiaries_df is not None:
            combined_kpis = {}
            
            if 'total_budget' in kpis['projects'] and 'total_beneficiaries' in kpis['beneficiaries']:
                combined_kpis['cost_per_beneficiary'] = kpis['projects']['total_budget'] / kpis['beneficiaries']['total_beneficiaries']
            
            if 'total_esf_funding' in kpis['projects'] and 'total_beneficiaries' in kpis['beneficiaries']:
                combined_kpis['esf_cost_per_beneficiary'] = kpis['projects']['total_esf_funding'] / kpis['beneficiaries']['total_beneficiaries']
            
            if 'total_training_hours' in kpis['beneficiaries'] and 'total_beneficiaries' in kpis['beneficiaries']:
                combined_kpis['avg_training_hours_per_beneficiary'] = kpis['beneficiaries']['total_training_hours'] / kpis['beneficiaries']['total_beneficiaries']
            
            kpis['combined'] = combined_kpis
        
        # Display KPIs
        print("\\n📊 PROJECT KPIs:")
        if 'projects' in kpis:
            for key, value in kpis['projects'].items():
                if 'rate' in key or 'achievement' in key:
                    print(f"   {key.replace('_', ' ').title()}: {value:.1f}%")
                elif 'budget' in key or 'funding' in key:
                    print(f"   {key.replace('_', ' ').title()}: €{value:,.2f}")
                else:
                    print(f"   {key.replace('_', ' ').title()}: {value:,}")
        
        print("\\n👥 BENEFICIARY KPIs:")
        if 'beneficiaries' in kpis:
            for key, value in kpis['beneficiaries'].items():
                if 'rate' in key:
                    print(f"   {key.replace('_', ' ').title()}: {value:.1f}%")
                elif 'satisfaction' in key and 'avg' in key:
                    print(f"   {key.replace('_', ' ').title()}: {value:.2f}/5")
                elif 'hours' in key and ('avg' in key or 'median' in key):
                    print(f"   {key.replace('_', ' ').title()}: {value:.1f}")
                else:
                    print(f"   {key.replace('_', ' ').title()}: {value:,}")
        
        print("\\n🔗 COMBINED KPIs:")
        if 'combined' in kpis:
            for key, value in kpis['combined'].items():
                if 'cost' in key:
                    print(f"   {key.replace('_', ' ').title()}: €{value:,.2f}")
                else:
                    print(f"   {key.replace('_', ' ').title()}: {value:.1f}")
        
        return kpis
    
    def export_comprehensive_report(self, filename="comprehensive_esf_analysis_report.txt"):
        """Export comprehensive analysis report"""
        import sys
        from io import StringIO
        
        # Capture all print output
        old_stdout = sys.stdout
        sys.stdout = buffer = StringIO()
        
        try:
            # Run all analyses
            projects_analysis = self.analyze_projects_overview()
            beneficiaries_analysis = self.analyze_beneficiaries_overview()
            cross_analysis = self.analyze_cross_dataset_relationships()
            kpis = self.calculate_comprehensive_kpis()
            
            # Get the captured output
            output = buffer.getvalue()
            sys.stdout = old_stdout
            
            # Write to file
            with open(f"cleaned_data/{filename}", 'w', encoding='utf-8') as f:
                f.write(f"COMPREHENSIVE ESF DATA ANALYSIS REPORT\\n")
                f.write(f"{'='*80}\\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
                f.write(f"{'='*80}\\n\\n")
                f.write(output)
                f.write("\\n\\nEND OF REPORT")
            
            print(f"\\n✅ Comprehensive analysis report exported to: cleaned_data/{filename}")
            
            # Also export KPIs as JSON for further processing
            kpi_filename = filename.replace('.txt', '_kpis.json')
            with open(f"cleaned_data/{kpi_filename}", 'w', encoding='utf-8') as f:
                # Convert any numpy types to Python types for JSON serialization
                def convert_numpy(obj):
                    if isinstance(obj, np.integer):
                        return int(obj)
                    elif isinstance(obj, np.floating):
                        return float(obj)
                    elif isinstance(obj, np.ndarray):
                        return obj.tolist()
                    else:
                        return obj
                
                json_kpis = {}
                for category, metrics in kpis.items():
                    json_kpis[category] = {k: convert_numpy(v) for k, v in metrics.items()}
                
                json.dump(json_kpis, f, indent=2, default=str)
            
            print(f"✅ KPIs exported as JSON to: cleaned_data/{kpi_filename}")
            
        except Exception as e:
            sys.stdout = old_stdout
            print(f"❌ Error exporting report: {e}")
        
        return kpis
    
    def generate_summary_dashboard_text(self):
        """Generate a text-based dashboard summary"""
        print("\\n" + "="*70)
        print("ESF PROGRAM DASHBOARD SUMMARY")
        print("="*70)
        
        if self.projects_df is None and self.beneficiaries_df is None:
            print("❌ No data available for dashboard")
            return
        
        # Quick stats
        print("\\n📋 QUICK OVERVIEW:")
        if self.projects_df is not None:
            total_projects = len(self.projects_df)
            total_budget = self.projects_df['total_budget'].sum()
            active_projects = len(self.projects_df[self.projects_df['status'] == 'Active'])
            print(f"   📊 Total Projects: {total_projects:,}")
            print(f"   💰 Total Budget: €{total_budget:,.2f}")
            print(f"   ✅ Active Projects: {active_projects:,}")
        
        if self.beneficiaries_df is not None:
            total_beneficiaries = len(self.beneficiaries_df)
            print(f"   👥 Total Beneficiaries: {total_beneficiaries:,}")
            
            if 'training_hours' in self.beneficiaries_df.columns:
                total_training = self.beneficiaries_df['training_hours'].sum()
                print(f"   📚 Total Training Hours: {total_training:,.0f}")
            
            if 'satisfaction_score' in self.beneficiaries_df.columns:
                avg_satisfaction = self.beneficiaries_df['satisfaction_score'].mean()
                print(f"   😊 Average Satisfaction: {avg_satisfaction:.1f}/5")
        
        # Performance indicators
        print("\\n🎯 KEY PERFORMANCE INDICATORS:")
        
        if self.projects_df is not None and 'target_achievement_rate' in self.projects_df.columns:
            avg_achievement = self.projects_df['target_achievement_rate'].mean()
            over_target = len(self.projects_df[self.projects_df['target_achievement_rate'] > 100])
            over_target_rate = (over_target / len(self.projects_df)) * 100
            
            print(f"   📈 Average Target Achievement: {avg_achievement:.1f}%")
            print(f"   🏆 Projects Exceeding Targets: {over_target:,} ({over_target_rate:.1f}%)")
        
        if self.beneficiaries_df is not None and 'outcome_achieved' in self.beneficiaries_df.columns:
            employment_outcomes = ['Employed', 'Self-employed']
            successful = self.beneficiaries_df[self.beneficiaries_df['outcome_achieved'].isin(employment_outcomes)]
            success_rate = (len(successful) / len(self.beneficiaries_df)) * 100
            print(f"   💼 Employment Success Rate: {success_rate:.1f}%")
        
        # Alerts and recommendations
        print("\\n⚠️ ALERTS & RECOMMENDATIONS:")
        alerts = []
        
        if self.projects_df is not None:
            # Check for projects with very low achievement rates
            if 'target_achievement_rate' in self.projects_df.columns:
                low_performers = self.projects_df[self.projects_df['target_achievement_rate'] < 50]
                if len(low_performers) > 0:
                    alerts.append(f"🔴 {len(low_performers)} projects have achievement rates below 50%")
            
            # Check for projects without beneficiaries
            if self.beneficiaries_df is not None and 'project_id' in self.beneficiaries_df.columns:
                project_ids_with_beneficiaries = set(self.beneficiaries_df['project_id'].unique())
                projects_without_beneficiaries = self.projects_df[~self.projects_df['project_id'].isin(project_ids_with_beneficiaries)]
                if len(projects_without_beneficiaries) > 0:
                    alerts.append(f"🟡 {len(projects_without_beneficiaries)} projects have no recorded beneficiaries")
        
        if self.beneficiaries_df is not None:
            # Check satisfaction scores
            if 'satisfaction_score' in self.beneficiaries_df.columns:
                low_satisfaction = self.beneficiaries_df[self.beneficiaries_df['satisfaction_score'] <= 2]
                if len(low_satisfaction) > 0:
                    low_sat_rate = (len(low_satisfaction) / len(self.beneficiaries_df)) * 100
                    alerts.append(f"🔴 {len(low_satisfaction)} beneficiaries ({low_sat_rate:.1f}%) have low satisfaction scores (≤2)")
        
        if alerts:
            for alert in alerts:
                print(f"   {alert}")
        else:
            print("   ✅ No major issues detected")
        
        print("\\n" + "="*70)

def main():
    """Main execution function"""
    print("ESF Data Analysis Tool (Basic Version)")
    print("=" * 50)
    
    # Initialize analyzer with cleaned data files
    analyzer = ESFBasicAnalyzer(
        projects_file="cleaned_data/esf_projects_cleaned.csv",
        beneficiaries_file="cleaned_data/esf_beneficiaries_cleaned.csv"
    )
    
    # Generate dashboard summary
    analyzer.generate_summary_dashboard_text()
    
    # Perform comprehensive analysis
    analyzer.analyze_projects_overview()
    analyzer.analyze_beneficiaries_overview()
    analyzer.analyze_cross_dataset_relationships()
    
    # Calculate comprehensive KPIs
    kpis = analyzer.calculate_comprehensive_kpis()
    
    # Export comprehensive report
    analyzer.export_comprehensive_report()
    
    print("\\n" + "="*70)
    print("🎉 COMPREHENSIVE ANALYSIS COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\\n📁 Files generated in 'cleaned_data/' folder:")
    print("   📄 comprehensive_esf_analysis_report.txt")
    print("   📊 comprehensive_esf_analysis_report_kpis.json")
    print("\\n💡 Next steps:")
    print("   1. Review the comprehensive analysis report")
    print("   2. Use the KPI JSON file for dashboard creation")
    print("   3. Replace sample data with your actual ESF datasets")
    print("   4. Run the analysis again with real data")
    print("   5. Set up regular monitoring using these scripts")

if __name__ == "__main__":
    main()
