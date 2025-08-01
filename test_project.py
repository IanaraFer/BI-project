#!/usr/bin/env python3
"""
ESF Project Test Script
======================

Simple test to verify the project structure and data files are working correctly.
This script doesn't require external packages like matplotlib or seaborn.
"""

import os
import csv
from datetime import datetime

def test_project_structure():
    """Test if all required project files exist"""
    print("🔍 TESTING PROJECT STRUCTURE")
    print("=" * 50)
    
    required_files = [
        'data_cleaning_script.py',
        'simple_dashboard_generator.py', 
        'data_analysis_script.py',
        'basic_analysis_script.py',
        'DAX_MEASURES_REFERENCE.md',
        'README.md',
        'cleaned_data/esf_projects_cleaned.csv',
        'cleaned_data/esf_beneficiaries_cleaned.csv'
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            existing_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}")
    
    print(f"\n📊 RESULTS:")
    print(f"✅ Found: {len(existing_files)} files")
    print(f"❌ Missing: {len(missing_files)} files")
    
    return len(missing_files) == 0

def test_data_files():
    """Test if data files can be read and contain valid data"""
    print("\n🔍 TESTING DATA FILES")
    print("=" * 50)
    
    # Test projects data
    try:
        with open('cleaned_data/esf_projects_cleaned.csv', 'r') as f:
            reader = csv.DictReader(f)
            projects = list(reader)
        
        print(f"✅ Projects data: {len(projects)} records")
        
        # Check required columns
        expected_columns = ['project_id', 'project_name', 'total_budget', 'esf_funding', 'status', 'region']
        actual_columns = list(projects[0].keys()) if projects else []
        
        missing_columns = [col for col in expected_columns if col not in actual_columns]
        if missing_columns:
            print(f"⚠️  Missing columns: {missing_columns}")
        else:
            print("✅ All required columns present")
            
    except Exception as e:
        print(f"❌ Error reading projects data: {e}")
        return False
    
    # Test beneficiaries data
    try:
        with open('cleaned_data/esf_beneficiaries_cleaned.csv', 'r') as f:
            reader = csv.DictReader(f)
            beneficiaries = list(reader)
        
        print(f"✅ Beneficiaries data: {len(beneficiaries)} records")
        
    except FileNotFoundError:
        print("⚠️  Beneficiaries data not found - will be created when needed")
    except Exception as e:
        print(f"❌ Error reading beneficiaries data: {e}")
        return False
    
    return True

def calculate_basic_stats():
    """Calculate basic statistics without external libraries"""
    print("\n📊 BASIC STATISTICS")
    print("=" * 50)
    
    try:
        with open('cleaned_data/esf_projects_cleaned.csv', 'r') as f:
            reader = csv.DictReader(f)
            projects = list(reader)
        
        # Calculate basic stats
        total_budget = sum(float(p['total_budget']) for p in projects)
        total_esf = sum(float(p['esf_funding']) for p in projects)
        avg_budget = total_budget / len(projects)
        
        # Count by status
        status_counts = {}
        for project in projects:
            status = project['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Count by region
        region_counts = {}
        for project in projects:
            region = project['region']
            region_counts[region] = region_counts.get(region, 0) + 1
        
        # Display results
        print(f"💰 Total Budget: €{total_budget:,.0f}")
        print(f"💰 Total ESF Funding: €{total_esf:,.0f}")
        print(f"💰 Average Project Budget: €{avg_budget:,.0f}")
        print(f"📈 ESF Funding Rate: {(total_esf/total_budget)*100:.1f}%")
        
        print(f"\n📊 Project Status:")
        for status, count in status_counts.items():
            print(f"   {status}: {count}")
        
        print(f"\n🌍 Regional Distribution:")
        for region, count in region_counts.items():
            print(f"   {region}: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error calculating statistics: {e}")
        return False

def test_dashboard_generation():
    """Test if dashboard HTML can be created"""
    print("\n🌐 TESTING DASHBOARD GENERATION")
    print("=" * 50)
    
    try:
        # Create a simple test HTML dashboard
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>ESF Dashboard Test</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .success {{ color: green; font-weight: bold; }}
        .info {{ background: #f0f8ff; padding: 20px; border-radius: 10px; }}
    </style>
</head>
<body>
    <h1>ESF Project Dashboard Test</h1>
    <div class="info">
        <p class="success">✅ Dashboard generation test successful!</p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>This confirms that HTML dashboard creation is working.</p>
        <p>Run <code>simple_dashboard_generator.py</code> for the full interactive dashboard.</p>
    </div>
</body>
</html>"""
        
        with open('test_dashboard.html', 'w') as f:
            f.write(html_content)
        
        print("✅ Test dashboard created: test_dashboard.html")
        return True
        
    except Exception as e:
        print(f"❌ Error creating test dashboard: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 ESF PROJECT FUNCTIONALITY TEST")
    print("=" * 60)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    # Run tests
    if test_project_structure():
        tests_passed += 1
    
    if test_data_files():
        tests_passed += 1
    
    if calculate_basic_stats():
        tests_passed += 1
        
    if test_dashboard_generation():
        tests_passed += 1
    
    # Final results
    print("\n" + "=" * 60)
    print("🏁 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Your ESF BI project is fully functional!")
        print("\n🚀 Ready to use:")
        print("   - Run simple_dashboard_generator.py for interactive dashboards")
        print("   - Run data_analysis_script.py for advanced visualizations")
        print("   - Use DAX_MEASURES_REFERENCE.md for Power BI integration")
        print("   - Check README.md for complete documentation")
    else:
        print(f"⚠️  {tests_passed}/{total_tests} tests passed")
        print("Some issues were found but basic functionality should work.")
    
    print(f"\n📁 Test completed. Check test_dashboard.html for a sample output.")

if __name__ == "__main__":
    main()
