#!/usr/bin/env python3
"""
Simple ESF Visualization Script
===============================
This script creates basic visualizations for ESF data analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Set style for better looking plots
plt.style.use('default')
sns.set_palette("husl")

def create_esf_visualizations():
    """Create comprehensive ESF visualizations"""
    print("🎨 Creating ESF Data Visualizations...")
    print("=" * 50)
    
    # Ensure output directory exists
    os.makedirs('cleaned_data', exist_ok=True)
    
    try:
        # Load data
        print("📊 Loading data...")
        projects_df = pd.read_csv('cleaned_data/esf_projects_cleaned.csv')
        beneficiaries_df = pd.read_csv('cleaned_data/esf_beneficiaries_cleaned.csv')
        
        print(f"✅ Loaded {len(projects_df)} projects and {len(beneficiaries_df)} beneficiaries")
        
        # 1. Project Status Distribution
        print("📈 Creating project status distribution chart...")
        plt.figure(figsize=(10, 6))
        status_counts = projects_df['status'].value_counts()
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        plt.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', 
                startangle=90, colors=colors)
        plt.title('ESF Project Status Distribution', fontsize=16, fontweight='bold', pad=20)
        plt.axis('equal')
        plt.savefig('cleaned_data/project_status_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Saved: project_status_distribution.png")
        
        # 2. Budget Analysis by Project Type
        print("💰 Creating budget analysis chart...")
        plt.figure(figsize=(14, 8))
        budget_by_type = projects_df.groupby('project_type').agg({
            'total_budget': 'sum',
            'esf_funding': 'sum'
        }).round(2)
        
        x = range(len(budget_by_type.index))
        width = 0.35
        
        plt.bar([i - width/2 for i in x], budget_by_type['total_budget'], width, 
                label='Total Budget', alpha=0.8, color='#3498DB')
        plt.bar([i + width/2 for i in x], budget_by_type['esf_funding'], width, 
                label='ESF Funding', alpha=0.8, color='#E74C3C')
        
        plt.xlabel('Project Type', fontsize=12)
        plt.ylabel('Budget (€)', fontsize=12)
        plt.title('Budget Analysis by Project Type', fontsize=16, fontweight='bold')
        plt.xticks(x, budget_by_type.index, rotation=45, ha='right')
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        plt.savefig('cleaned_data/budget_analysis_by_type.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Saved: budget_analysis_by_type.png")
        
        # 3. Demographics Overview
        print("👥 Creating demographics overview...")
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Gender distribution
        gender_counts = beneficiaries_df['gender'].value_counts()
        axes[0, 0].pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%',
                      colors=['#FF9999', '#66B2FF'])
        axes[0, 0].set_title('Gender Distribution', fontsize=14, fontweight='bold')
        
        # Age group distribution
        age_counts = beneficiaries_df['age_group'].value_counts()
        axes[0, 1].bar(age_counts.index, age_counts.values, color='#96CEB4')
        axes[0, 1].set_title('Age Group Distribution', fontsize=14, fontweight='bold')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Education level distribution
        edu_counts = beneficiaries_df['education_level'].value_counts()
        axes[1, 0].bar(edu_counts.index, edu_counts.values, color='#FFEAA7')
        axes[1, 0].set_title('Education Level Distribution', fontsize=14, fontweight='bold')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Employment outcomes
        outcome_counts = beneficiaries_df['outcome_achieved'].value_counts()
        axes[1, 1].bar(outcome_counts.index, outcome_counts.values, color='#DDA0DD')
        axes[1, 1].set_title('Employment Outcomes', fontsize=14, fontweight='bold')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('cleaned_data/beneficiaries_demographics.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Saved: beneficiaries_demographics.png")
        
        # 4. Training Hours Analysis
        print("🎓 Creating training hours analysis...")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Distribution of training hours
        ax1.hist(beneficiaries_df['training_hours'], bins=20, alpha=0.7, 
                color='#74B9FF', edgecolor='black')
        avg_hours = beneficiaries_df['training_hours'].mean()
        ax1.axvline(avg_hours, color='red', linestyle='--', linewidth=2,
                   label=f'Mean: {avg_hours:.1f} hours')
        ax1.set_xlabel('Training Hours', fontsize=12)
        ax1.set_ylabel('Number of Beneficiaries', fontsize=12)
        ax1.set_title('Distribution of Training Hours', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(alpha=0.3)
        
        # Training hours by education level
        edu_training = beneficiaries_df.groupby('education_level')['training_hours'].mean()
        ax2.bar(edu_training.index, edu_training.values, color='#A29BFE')
        ax2.set_xlabel('Education Level', fontsize=12)
        ax2.set_ylabel('Average Training Hours', fontsize=12)
        ax2.set_title('Average Training Hours by Education Level', fontsize=14, fontweight='bold')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('cleaned_data/training_hours_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Saved: training_hours_analysis.png")
        
        # 5. Regional Performance Analysis
        print("🌍 Creating regional analysis...")
        plt.figure(figsize=(14, 8))
        
        # Regional budget distribution
        region_budget = projects_df.groupby('region')['total_budget'].sum().sort_values(ascending=False)
        
        plt.bar(region_budget.index, region_budget.values, color='#00B894')
        plt.title('Total Budget by Region', fontsize=16, fontweight='bold')
        plt.xlabel('Region', fontsize=12)
        plt.ylabel('Total Budget (€)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for i, v in enumerate(region_budget.values):
            plt.text(i, v + max(region_budget.values)*0.01, f'€{v:,.0f}', 
                    ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        plt.savefig('cleaned_data/regional_budget_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ Saved: regional_budget_analysis.png")
        
        # Print summary
        print("\n" + "=" * 50)
        print("🎉 VISUALIZATION CREATION COMPLETED!")
        print("=" * 50)
        print("📁 Generated visualization files:")
        print("   📊 project_status_distribution.png")
        print("   💰 budget_analysis_by_type.png")
        print("   👥 beneficiaries_demographics.png")
        print("   🎓 training_hours_analysis.png")
        print("   🌍 regional_budget_analysis.png")
        print("\n💡 All files saved in 'cleaned_data/' folder")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating visualizations: {e}")
        return False

def print_visualization_summary():
    """Print summary of available data for visualization"""
    try:
        projects_df = pd.read_csv('cleaned_data/esf_projects_cleaned.csv')
        beneficiaries_df = pd.read_csv('cleaned_data/esf_beneficiaries_cleaned.csv')
        
        print("\n📊 DATA SUMMARY FOR VISUALIZATIONS:")
        print("=" * 50)
        print(f"Projects Dataset: {len(projects_df)} records")
        print(f"  - Total Budget: €{projects_df['total_budget'].sum():,.2f}")
        print(f"  - Date Range: {projects_df['start_date'].min()} to {projects_df['end_date'].max()}")
        print(f"  - Project Types: {projects_df['project_type'].nunique()} types")
        print(f"  - Regions: {projects_df['region'].nunique()} regions")
        
        print(f"\nBeneficiaries Dataset: {len(beneficiaries_df)} records")
        print(f"  - Gender Split: {beneficiaries_df['gender'].value_counts().to_dict()}")
        print(f"  - Age Groups: {beneficiaries_df['age_group'].nunique()} groups")
        print(f"  - Education Levels: {beneficiaries_df['education_level'].nunique()} levels")
        print(f"  - Total Training Hours: {beneficiaries_df['training_hours'].sum():,.0f}")
        
    except Exception as e:
        print(f"Error reading data: {e}")

if __name__ == "__main__":
    print("🎨 ESF DATA VISUALIZATION GENERATOR")
    print("=" * 50)
    print("📦 Testing packages...")
    
    # Test imports
    try:
        print(f"✅ Matplotlib version: {plt.matplotlib.__version__}")
        print(f"✅ Seaborn version: {sns.__version__}")
        print(f"✅ Pandas version: {pd.__version__}")
        print(f"✅ NumPy version: {np.__version__}")
    except Exception as e:
        print(f"❌ Package error: {e}")
        exit(1)
    
    # Print data summary
    print_visualization_summary()
    
    # Create visualizations
    success = create_esf_visualizations()
    
    if success:
        print("\n🚀 SUCCESS! Your ESF visualizations are ready!")
    else:
        print("\n⚠️  Some issues occurred during visualization creation.")
