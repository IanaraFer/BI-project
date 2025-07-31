#!/usr/bin/env python3
"""
ESF Data Analysis Script (No Dependencies Version)
==================================================

This script provides basic analysis of ESF projects and beneficiaries data
using only Python built-in libraries. No pandas or numpy required!

It focuses on:
1. Data exploration and statistics
2. Performance metrics calculation
3. Comprehensive reporting
4. Data quality assessment

Usage:
    python simple_analysis_script.py
"""

import csv
import json
from datetime import datetime
from collections import defaultdict, Counter
import os

class SimpleESFAnalyzer:
    def __init__(self, projects_file=None, beneficiaries_file=None):
        self.projects_data = []
        self.beneficiaries_data = []
        
        if projects_file and os.path.exists(projects_file):
            self.load_projects_data(projects_file)
        else:
            print("⚠️ Projects file not found, creating sample data...")
            self.create_sample_projects()
            
        if beneficiaries_file and os.path.exists(beneficiaries_file):
            self.load_beneficiaries_data(beneficiaries_file)
        else:
            print("⚠️ Beneficiaries file not found, creating sample data...")
            self.create_sample_beneficiaries()
    
    def load_projects_data(self, file_path):
        """Load projects data from CSV file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.projects_data = list(reader)
            print(f"✅ Loaded {len(self.projects_data)} project records")
        except Exception as e:
            print(f"❌ Error loading projects data: {e}")
            self.create_sample_projects()
    
    def load_beneficiaries_data(self, file_path):
        """Load beneficiaries data from CSV file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.beneficiaries_data = list(reader)
            print(f"✅ Loaded {len(self.beneficiaries_data)} beneficiary records")
        except Exception as e:
            print(f"❌ Error loading beneficiaries data: {e}")
            self.create_sample_beneficiaries()
    
    def create_sample_projects(self):
        """Create sample project data"""
        import random
        
        regions = ['Dublin', 'Cork', 'Galway', 'Limerick', 'Waterford', 'Kilkenny']
        project_types = ['Digital Skills', 'Youth Employment', 'Green Skills', 'Social Innovation', 'Rural Development']
        statuses = ['Active', 'Completed', 'Planning', 'On Hold']
        risk_levels = ['Low', 'Medium', 'High']
        
        self.projects_data = []
        for i in range(50):
            budget = random.randint(50000, 500000)
            actual_spend = int(budget * random.uniform(0.7, 1.1))
            esf_funding = int(budget * 0.8)
            target_beneficiaries = random.randint(50, 200)
            actual_beneficiaries = random.randint(40, 220)
            
            project = {
                'project_id': f'ESF_{str(i+1).zfill(3)}',
                'project_name': f'ESF Project {i+1}',
                'project_type': random.choice(project_types),
                'status': random.choice(statuses),
                'region': random.choice(regions),
                'total_budget': str(budget),
                'actual_spend': str(actual_spend),
                'esf_funding': str(esf_funding),
                'beneficiaries_target': str(target_beneficiaries),
                'beneficiaries_actual': str(actual_beneficiaries),
                'engagement_score': str(round(random.uniform(3.0, 5.0), 1)),
                'risk_flag': random.choice(risk_levels),
                'start_date': '2023-01-01',
                'end_date': '2024-12-31',
                'target_achievement_rate': str(round((actual_beneficiaries / target_beneficiaries) * 100, 1))
            }
            self.projects_data.append(project)
        
        print(f"✅ Created {len(self.projects_data)} sample projects")
    
    def create_sample_beneficiaries(self):
        """Create sample beneficiary data"""
        import random
        
        genders = ['Male', 'Female', 'Other', 'Prefer not to say']
        age_groups = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        education_levels = ['Primary', 'Secondary', 'Post-Secondary', 'Tertiary']
        regions = ['Dublin', 'Cork', 'Galway', 'Limerick', 'Waterford', 'Kilkenny']
        employment_before = ['Unemployed', 'Student', 'Employed', 'Self-employed']
        employment_after = ['Employed', 'Self-employed', 'Student', 'Still Seeking']
        outcomes = ['Employed', 'Self-employed', 'Further Education', 'Still Seeking']
        
        self.beneficiaries_data = []
        project_ids = [p['project_id'] for p in self.projects_data]
        
        for i in range(200):
            beneficiary = {
                'beneficiary_id': f'BEN_{str(i+1).zfill(4)}',
                'project_id': random.choice(project_ids),
                'gender': random.choice(genders),
                'age_group': random.choice(age_groups),
                'education_level': random.choice(education_levels),
                'region': random.choice(regions),
                'employment_status_before': random.choice(employment_before),
                'employment_status_after': random.choice(employment_after),
                'satisfaction_score': str(random.randint(1, 5)),
                'training_hours': str(random.randint(20, 200)),
                'outcome_achieved': random.choice(outcomes),
                'vulnerable_group': random.choice(['None', 'Long-term unemployed', 'Youth NEET', 'Disabled', 'Migrant'])
            }
            self.beneficiaries_data.append(beneficiary)
        
        print(f"✅ Created {len(self.beneficiaries_data)} sample beneficiaries")
    
    def safe_float(self, value, default=0.0):
        """Safely convert value to float"""
        try:
            return float(value) if value else default
        except (ValueError, TypeError):
            return default
    
    def safe_int(self, value, default=0):
        """Safely convert value to int"""
        try:
            return int(float(value)) if value else default
        except (ValueError, TypeError):
            return default
    
    def calculate_stats(self, values):
        """Calculate basic statistics for a list of values"""
        if not values:
            return {'count': 0, 'sum': 0, 'mean': 0, 'median': 0, 'min': 0, 'max': 0}
        
        values = sorted([v for v in values if v is not None])
        count = len(values)
        total = sum(values)
        mean = total / count if count > 0 else 0
        
        # Calculate median
        if count % 2 == 0:
            median = (values[count//2 - 1] + values[count//2]) / 2
        else:
            median = values[count//2]
        
        return {
            'count': count,
            'sum': total,
            'mean': mean,
            'median': median,
            'min': values[0] if values else 0,
            'max': values[-1] if values else 0
        }
    
    def analyze_projects_overview(self):
        """Provide comprehensive overview analysis of projects data"""
        print("\n" + "="*70)
        print("COMPREHENSIVE PROJECTS DATA ANALYSIS")
        print("="*70)
        
        analysis = {}
        
        # Basic statistics
        analysis['total_projects'] = len(self.projects_data)
        
        print(f"\n📊 BASIC STATISTICS:")
        print(f"   Total Projects: {analysis['total_projects']:,}")
        
        # Financial analysis
        budgets = [self.safe_float(p.get('total_budget', 0)) for p in self.projects_data]
        esf_funding = [self.safe_float(p.get('esf_funding', 0)) for p in self.projects_data]
        
        budget_stats = self.calculate_stats(budgets)
        esf_stats = self.calculate_stats(esf_funding)
        
        esf_funding_rate = (esf_stats['sum'] / budget_stats['sum']) * 100 if budget_stats['sum'] > 0 else 0
        
        analysis['financial'] = {
            'total_budget': budget_stats['sum'],
            'total_esf_funding': esf_stats['sum'],
            'avg_budget': budget_stats['mean'],
            'median_budget': budget_stats['median'],
            'min_budget': budget_stats['min'],
            'max_budget': budget_stats['max'],
            'esf_funding_rate': esf_funding_rate
        }
        
        print(f"\n💰 FINANCIAL OVERVIEW:")
        print(f"   Total Budget: €{budget_stats['sum']:,.2f}")
        print(f"   Total ESF Funding: €{esf_stats['sum']:,.2f}")
        print(f"   ESF Funding Rate: {esf_funding_rate:.1f}%")
        print(f"   Average Project Budget: €{budget_stats['mean']:,.2f}")
        print(f"   Median Project Budget: €{budget_stats['median']:,.2f}")
        print(f"   Budget Range: €{budget_stats['min']:,.2f} - €{budget_stats['max']:,.2f}")
        
        # Project status analysis
        statuses = [p.get('status', 'Unknown') for p in self.projects_data]
        status_counts = Counter(statuses)
        analysis['status_distribution'] = dict(status_counts)
        
        print(f"\n📈 PROJECT STATUS DISTRIBUTION:")
        for status, count in status_counts.most_common():
            percentage = (count / len(self.projects_data)) * 100
            print(f"   {status}: {count:,} ({percentage:.1f}%)")
        
        # Project type analysis
        types = [p.get('project_type', 'Unknown') for p in self.projects_data]
        type_counts = Counter(types)
        analysis['type_distribution'] = dict(type_counts)
        
        print(f"\n🎯 PROJECT TYPE DISTRIBUTION:")
        for ptype, count in type_counts.most_common():
            percentage = (count / len(self.projects_data)) * 100
            print(f"   {ptype}: {count:,} ({percentage:.1f}%)")
        
        # Regional analysis
        regions = [p.get('region', 'Unknown') for p in self.projects_data]
        region_counts = Counter(regions)
        analysis['regional_distribution'] = dict(region_counts)
        
        print(f"\n🌍 REGIONAL DISTRIBUTION:")
        for region, count in region_counts.most_common():
            percentage = (count / len(self.projects_data)) * 100
            print(f"   {region}: {count:,} ({percentage:.1f}%)")
        
        # Performance metrics
        achievement_rates = [self.safe_float(p.get('target_achievement_rate', 0)) for p in self.projects_data]
        achievement_stats = self.calculate_stats(achievement_rates)
        
        over_target = len([rate for rate in achievement_rates if rate > 100])
        under_target = len([rate for rate in achievement_rates if rate < 100])
        exactly_target = len([rate for rate in achievement_rates if rate == 100])
        
        analysis['performance'] = {
            'avg_achievement': achievement_stats['mean'],
            'median_achievement': achievement_stats['median'],
            'over_target_count': over_target,
            'under_target_count': under_target,
            'exactly_target_count': exactly_target,
            'over_target_rate': (over_target / len(self.projects_data)) * 100,
            'under_target_rate': (under_target / len(self.projects_data)) * 100
        }
        
        print(f"\n🎯 PERFORMANCE METRICS:")
        print(f"   Average Target Achievement: {achievement_stats['mean']:.1f}%")
        print(f"   Median Target Achievement: {achievement_stats['median']:.1f}%")
        print(f"   Projects Exceeding Target: {over_target:,} ({analysis['performance']['over_target_rate']:.1f}%)")
        print(f"   Projects Below Target: {under_target:,} ({analysis['performance']['under_target_rate']:.1f}%)")
        print(f"   Projects Meeting Exact Target: {exactly_target:,}")
        
        return analysis
    
    def analyze_beneficiaries_overview(self):
        """Provide comprehensive overview analysis of beneficiaries data"""
        print("\n" + "="*70)
        print("COMPREHENSIVE BENEFICIARIES DATA ANALYSIS")
        print("="*70)
        
        analysis = {}
        
        # Basic statistics
        analysis['total_beneficiaries'] = len(self.beneficiaries_data)
        
        print(f"\n📊 BASIC STATISTICS:")
        print(f"   Total Beneficiaries: {analysis['total_beneficiaries']:,}")
        
        # Demographics analysis
        print(f"\n👥 DEMOGRAPHIC BREAKDOWN:")
        
        # Gender distribution
        genders = [b.get('gender', 'Unknown') for b in self.beneficiaries_data]
        gender_counts = Counter(genders)
        analysis['gender_distribution'] = dict(gender_counts)
        
        print("   Gender Distribution:")
        for gender, count in gender_counts.most_common():
            percentage = (count / len(self.beneficiaries_data)) * 100
            print(f"     {gender}: {count:,} ({percentage:.1f}%)")
        
        # Age group distribution
        ages = [b.get('age_group', 'Unknown') for b in self.beneficiaries_data]
        age_counts = Counter(ages)
        analysis['age_distribution'] = dict(age_counts)
        
        print("\n   Age Group Distribution:")
        for age, count in age_counts.most_common():
            percentage = (count / len(self.beneficiaries_data)) * 100
            print(f"     {age}: {count:,} ({percentage:.1f}%)")
        
        # Education level distribution
        education = [b.get('education_level', 'Unknown') for b in self.beneficiaries_data]
        edu_counts = Counter(education)
        analysis['education_distribution'] = dict(edu_counts)
        
        print("\n   Education Level Distribution:")
        for edu, count in edu_counts.most_common():
            percentage = (count / len(self.beneficiaries_data)) * 100
            print(f"     {edu}: {count:,} ({percentage:.1f}%)")
        
        # Employment outcomes
        outcomes = [b.get('outcome_achieved', 'Unknown') for b in self.beneficiaries_data]
        outcome_counts = Counter(outcomes)
        analysis['outcome_distribution'] = dict(outcome_counts)
        
        print(f"\n🎯 EMPLOYMENT OUTCOMES:")
        for outcome, count in outcome_counts.most_common():
            percentage = (count / len(self.beneficiaries_data)) * 100
            print(f"   {outcome}: {count:,} ({percentage:.1f}%)")
        
        # Training statistics
        training_hours = [self.safe_int(b.get('training_hours', 0)) for b in self.beneficiaries_data]
        training_stats = self.calculate_stats(training_hours)
        
        analysis['training_stats'] = {
            'total_hours': training_stats['sum'],
            'avg_hours': training_stats['mean'],
            'median_hours': training_stats['median'],
            'min_hours': training_stats['min'],
            'max_hours': training_stats['max']
        }
        
        print(f"\n📚 TRAINING STATISTICS:")
        print(f"   Total Training Hours Delivered: {training_stats['sum']:,.0f}")
        print(f"   Average Hours per Beneficiary: {training_stats['mean']:.1f}")
        print(f"   Median Hours per Beneficiary: {training_stats['median']:.1f}")
        print(f"   Training Hours Range: {training_stats['min']:.0f} - {training_stats['max']:.0f}")
        
        # Satisfaction analysis
        satisfaction_scores = [self.safe_int(b.get('satisfaction_score', 0)) for b in self.beneficiaries_data]
        satisfaction_stats = self.calculate_stats(satisfaction_scores)
        
        high_satisfaction = len([score for score in satisfaction_scores if score >= 4])
        low_satisfaction = len([score for score in satisfaction_scores if score <= 2])
        
        analysis['satisfaction_stats'] = {
            'avg_satisfaction': satisfaction_stats['mean'],
            'median_satisfaction': satisfaction_stats['median'],
            'high_satisfaction_count': high_satisfaction,
            'low_satisfaction_count': low_satisfaction,
            'high_satisfaction_rate': (high_satisfaction / len(self.beneficiaries_data)) * 100,
            'low_satisfaction_rate': (low_satisfaction / len(self.beneficiaries_data)) * 100
        }
        
        print(f"\n😊 SATISFACTION METRICS:")
        print(f"   Average Satisfaction Score: {satisfaction_stats['mean']:.2f}/5")
        print(f"   Median Satisfaction Score: {satisfaction_stats['median']:.2f}/5")
        print(f"   High Satisfaction (4-5): {high_satisfaction:,} ({analysis['satisfaction_stats']['high_satisfaction_rate']:.1f}%)")
        print(f"   Low Satisfaction (1-2): {low_satisfaction:,} ({analysis['satisfaction_stats']['low_satisfaction_rate']:.1f}%)")
        
        return analysis
    
    def calculate_comprehensive_kpis(self):
        """Calculate comprehensive Key Performance Indicators"""
        print("\n" + "="*70)
        print("COMPREHENSIVE KEY PERFORMANCE INDICATORS (KPIs)")
        print("="*70)
        
        kpis = {}
        
        # Projects KPIs
        budgets = [self.safe_float(p.get('total_budget', 0)) for p in self.projects_data]
        esf_funding = [self.safe_float(p.get('esf_funding', 0)) for p in self.projects_data]
        
        budget_stats = self.calculate_stats(budgets)
        esf_stats = self.calculate_stats(esf_funding)
        
        project_kpis = {
            'total_projects': len(self.projects_data),
            'total_budget': budget_stats['sum'],
            'total_esf_funding': esf_stats['sum'],
            'avg_project_budget': budget_stats['mean'],
            'median_project_budget': budget_stats['median'],
            'esf_funding_rate': (esf_stats['sum'] / budget_stats['sum']) * 100 if budget_stats['sum'] > 0 else 0
        }
        
        # Achievement rates
        achievement_rates = [self.safe_float(p.get('target_achievement_rate', 0)) for p in self.projects_data]
        achievement_stats = self.calculate_stats(achievement_rates)
        
        project_kpis.update({
            'avg_target_achievement': achievement_stats['mean'],
            'projects_over_target': len([rate for rate in achievement_rates if rate > 100]),
            'projects_over_target_rate': (len([rate for rate in achievement_rates if rate > 100]) / len(self.projects_data)) * 100
        })
        
        # Status counts
        statuses = [p.get('status', 'Unknown') for p in self.projects_data]
        status_counts = Counter(statuses)
        for status, count in status_counts.items():
            project_kpis[f'{status.lower()}_projects_count'] = count
            project_kpis[f'{status.lower()}_projects_rate'] = (count / len(self.projects_data)) * 100
        
        kpis['projects'] = project_kpis
        
        # Beneficiaries KPIs
        training_hours = [self.safe_int(b.get('training_hours', 0)) for b in self.beneficiaries_data]
        training_stats = self.calculate_stats(training_hours)
        
        satisfaction_scores = [self.safe_int(b.get('satisfaction_score', 0)) for b in self.beneficiaries_data]
        satisfaction_stats = self.calculate_stats(satisfaction_scores)
        
        beneficiary_kpis = {
            'total_beneficiaries': len(self.beneficiaries_data),
            'total_training_hours': training_stats['sum'],
            'avg_training_hours': training_stats['mean'],
            'median_training_hours': training_stats['median'],
            'avg_satisfaction': satisfaction_stats['mean'],
            'high_satisfaction_count': len([score for score in satisfaction_scores if score >= 4]),
            'high_satisfaction_rate': (len([score for score in satisfaction_scores if score >= 4]) / len(self.beneficiaries_data)) * 100
        }
        
        # Employment success
        employment_outcomes = ['Employed', 'Self-employed']
        outcomes = [b.get('outcome_achieved', '') for b in self.beneficiaries_data]
        successful_outcomes = [o for o in outcomes if o in employment_outcomes]
        
        beneficiary_kpis.update({
            'employment_success_count': len(successful_outcomes),
            'employment_success_rate': (len(successful_outcomes) / len(self.beneficiaries_data)) * 100
        })
        
        kpis['beneficiaries'] = beneficiary_kpis
        
        # Combined KPIs
        combined_kpis = {}
        if budget_stats['sum'] > 0 and len(self.beneficiaries_data) > 0:
            combined_kpis['cost_per_beneficiary'] = budget_stats['sum'] / len(self.beneficiaries_data)
            combined_kpis['esf_cost_per_beneficiary'] = esf_stats['sum'] / len(self.beneficiaries_data)
        
        if training_stats['sum'] > 0 and len(self.beneficiaries_data) > 0:
            combined_kpis['avg_training_hours_per_beneficiary'] = training_stats['sum'] / len(self.beneficiaries_data)
        
        kpis['combined'] = combined_kpis
        
        # Display KPIs
        print("\n📊 PROJECT KPIs:")
        for key, value in project_kpis.items():
            if 'rate' in key or 'achievement' in key:
                print(f"   {key.replace('_', ' ').title()}: {value:.1f}%")
            elif 'budget' in key or 'funding' in key:
                print(f"   {key.replace('_', ' ').title()}: €{value:,.2f}")
            else:
                print(f"   {key.replace('_', ' ').title()}: {value:,}")
        
        print("\n👥 BENEFICIARY KPIs:")
        for key, value in beneficiary_kpis.items():
            if 'rate' in key:
                print(f"   {key.replace('_', ' ').title()}: {value:.1f}%")
            elif 'satisfaction' in key and 'avg' in key:
                print(f"   {key.replace('_', ' ').title()}: {value:.2f}/5")
            elif 'hours' in key and ('avg' in key or 'median' in key):
                print(f"   {key.replace('_', ' ').title()}: {value:.1f}")
            else:
                print(f"   {key.replace('_', ' ').title()}: {value:,}")
        
        print("\n🔗 COMBINED KPIs:")
        for key, value in combined_kpis.items():
            if 'cost' in key:
                print(f"   {key.replace('_', ' ').title()}: €{value:,.2f}")
            else:
                print(f"   {key.replace('_', ' ').title()}: {value:.1f}")
        
        return kpis
    
    def export_comprehensive_report(self, filename="comprehensive_esf_analysis_report.txt"):
        """Export comprehensive analysis report"""
        # Create output directory if it doesn't exist
        os.makedirs("cleaned_data", exist_ok=True)
        
        try:
            # Capture analysis results
            projects_analysis = self.analyze_projects_overview()
            beneficiaries_analysis = self.analyze_beneficiaries_overview()
            kpis = self.calculate_comprehensive_kpis()
            
            # Write to file
            with open(f"cleaned_data/{filename}", 'w', encoding='utf-8') as f:
                f.write(f"COMPREHENSIVE ESF DATA ANALYSIS REPORT\n")
                f.write(f"{'='*80}\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*80}\n\n")
                
                f.write("SUMMARY DASHBOARD\n")
                f.write("-" * 40 + "\n")
                f.write(f"Total Projects: {len(self.projects_data):,}\n")
                f.write(f"Total Beneficiaries: {len(self.beneficiaries_data):,}\n")
                
                if self.projects_data:
                    total_budget = sum(self.safe_float(p.get('total_budget', 0)) for p in self.projects_data)
                    f.write(f"Total Budget: €{total_budget:,.2f}\n")
                
                f.write(f"\nData Quality:\n")
                f.write(f"- Projects data: ✅ {len(self.projects_data)} records loaded\n")
                f.write(f"- Beneficiaries data: ✅ {len(self.beneficiaries_data)} records loaded\n")
                
                f.write("\n\nEND OF REPORT")
            
            print(f"\n✅ Comprehensive analysis report exported to: cleaned_data/{filename}")
            
            # Export KPIs as JSON
            kpi_filename = filename.replace('.txt', '_kpis.json')
            with open(f"cleaned_data/{kpi_filename}", 'w', encoding='utf-8') as f:
                json.dump(kpis, f, indent=2)
            
            print(f"✅ KPIs exported as JSON to: cleaned_data/{kpi_filename}")
            
        except Exception as e:
            print(f"❌ Error exporting report: {e}")
        
        return kpis

def main():
    """Main execution function"""
    print("🎯 ESF Data Analysis Tool (No Dependencies Version)")
    print("=" * 60)
    print("✅ Uses only Python built-in libraries!")
    print("✅ No pandas or numpy required!")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = SimpleESFAnalyzer(
        projects_file="cleaned_data/esf_projects_cleaned.csv",
        beneficiaries_file="cleaned_data/esf_beneficiaries_cleaned.csv"
    )
    
    # Perform comprehensive analysis
    print("\n🔍 Starting comprehensive analysis...")
    
    projects_analysis = analyzer.analyze_projects_overview()
    beneficiaries_analysis = analyzer.analyze_beneficiaries_overview()
    kpis = analyzer.calculate_comprehensive_kpis()
    
    # Export comprehensive report
    analyzer.export_comprehensive_report()
    
    print("\n" + "="*70)
    print("🎉 COMPREHENSIVE ANALYSIS COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\n📁 Files generated in 'cleaned_data/' folder:")
    print("   📄 comprehensive_esf_analysis_report.txt")
    print("   📊 comprehensive_esf_analysis_report_kpis.json")
    print("\n💡 Next steps:")
    print("   1. Review the comprehensive analysis report")
    print("   2. Open the generated dashboard: esf_dashboard.html")
    print("   3. Replace sample data with your actual ESF datasets")
    print("   4. Run the analysis again with real data")
    
    print(f"\n🎯 Quick Summary:")
    print(f"   📊 Total Projects Analyzed: {len(analyzer.projects_data):,}")
    print(f"   👥 Total Beneficiaries Analyzed: {len(analyzer.beneficiaries_data):,}")
    
    if analyzer.projects_data:
        total_budget = sum(analyzer.safe_float(p.get('total_budget', 0)) for p in analyzer.projects_data)
        print(f"   💰 Total Program Budget: €{total_budget:,.2f}")
    
    print("\n✅ Analysis complete! Your dashboard and reports are ready to view.")

if __name__ == "__main__":
    main()
