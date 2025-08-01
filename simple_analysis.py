#!/usr/bin/env python3
"""
Simple ESF Data Analysis Script (No External Dependencies)
==========================================================

This script performs basic data analysis without requiring matplotlib/seaborn.
It will show what data we have and provide text-based analysis.
"""

import os
import csv
from datetime import datetime

def analyze_esf_data():
    """Analyze ESF data without external packages"""
    print("📊 ESF DATA ANALYSIS (Simple Version)")
    print("=" * 50)
    
    # Check data files
    projects_file = 'cleaned_data/esf_projects_cleaned.csv'
    beneficiaries_file = 'cleaned_data/esf_beneficiaries_cleaned.csv'
    
    if not os.path.exists(projects_file):
        print("❌ Projects data file not found!")
        return
    
    if not os.path.exists(beneficiaries_file):
        print("❌ Beneficiaries data file not found!")
        return
    
    # Read projects data
    projects = []
    with open(projects_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        projects = list(reader)
    
    print(f"✅ Loaded {len(projects)} projects")
    
    # Read beneficiaries data
    beneficiaries = []
    with open(beneficiaries_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        beneficiaries = list(reader)
    
    print(f"✅ Loaded {len(beneficiaries)} beneficiaries")
    
    # Analyze projects
    print("\n📈 PROJECT ANALYSIS:")
    print("-" * 30)
    
    # Project status counts
    status_counts = {}
    total_budget = 0
    
    for project in projects:
        status = project.get('status', 'Unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
        
        try:
            budget = float(project.get('total_budget', 0))
            total_budget += budget
        except:
            pass
    
    print("Project Status Distribution:")
    for status, count in status_counts.items():
        percentage = (count / len(projects)) * 100
        print(f"  {status}: {count} ({percentage:.1f}%)")
    
    print(f"\nTotal Budget: €{total_budget:,.0f}")
    print(f"Average Budget per Project: €{total_budget/len(projects):,.0f}")
    
    # Region analysis
    regions = {}
    for project in projects:
        region = project.get('region', 'Unknown')
        regions[region] = regions.get(region, 0) + 1
    
    print(f"\nProjects by Region:")
    for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True):
        print(f"  {region}: {count} projects")
    
    # Analyze beneficiaries
    print("\n👥 BENEFICIARY ANALYSIS:")
    print("-" * 30)
    
    # Gender distribution
    genders = {}
    total_training_hours = 0
    satisfaction_scores = []
    
    for beneficiary in beneficiaries:
        gender = beneficiary.get('gender', 'Unknown')
        genders[gender] = genders.get(gender, 0) + 1
        
        try:
            hours = float(beneficiary.get('training_hours', 0))
            total_training_hours += hours
        except:
            pass
        
        try:
            score = float(beneficiary.get('satisfaction_score', 0))
            satisfaction_scores.append(score)
        except:
            pass
    
    print("Gender Distribution:")
    for gender, count in genders.items():
        percentage = (count / len(beneficiaries)) * 100
        print(f"  {gender}: {count} ({percentage:.1f}%)")
    
    print(f"\nTotal Training Hours: {total_training_hours:,.0f}")
    print(f"Average Training Hours: {total_training_hours/len(beneficiaries):.1f}")
    
    if satisfaction_scores:
        avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores)
        print(f"Average Satisfaction Score: {avg_satisfaction:.1f}/10")
    
    # Outcomes analysis
    outcomes = {}
    for beneficiary in beneficiaries:
        outcome = beneficiary.get('outcome_achieved', 'Unknown')
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
    
    print(f"\nEmployment Outcomes:")
    for outcome, count in outcomes.items():
        percentage = (count / len(beneficiaries)) * 100
        print(f"  {outcome}: {count} ({percentage:.1f}%)")
    
    # Summary
    print("\n🎯 KEY INSIGHTS:")
    print("-" * 30)
    
    # Success rate (assuming projects with >=100% achievement are successful)
    successful_projects = 0
    for project in projects:
        try:
            achievement = float(project.get('target_achievement_rate', 0))
            if achievement >= 100:
                successful_projects += 1
        except:
            pass
    
    success_rate = (successful_projects / len(projects)) * 100
    print(f"• Project Success Rate: {success_rate:.1f}%")
    print(f"• Average Project Size: €{total_budget/len(projects):,.0f}")
    print(f"• Total Investment: €{total_budget:,.0f}")
    print(f"• Beneficiaries Served: {len(beneficiaries)}")
    
    if satisfaction_scores:
        print(f"• Average Satisfaction: {avg_satisfaction:.1f}/10")
    
    print(f"\n📁 Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

if __name__ == "__main__":
    analyze_esf_data()
