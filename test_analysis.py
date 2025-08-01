#!/usr/bin/env python3
"""
Test script to validate ESF analysis functionality
"""

import pandas as pd
import numpy as np
from datetime import datetime
import csv
import json
import os

def test_imports():
    """Test all required imports"""
    try:
        print("✅ Testing imports...")
        import pandas as pd
        import numpy as np
        from datetime import datetime
        import csv
        import json
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_files():
    """Test if sample data files exist"""
    print("✅ Testing data files...")
    
    required_files = [
        'cleaned_data/esf_projects_cleaned.csv',
        'cleaned_data/esf_beneficiaries_cleaned.csv'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files found!")
        return True

def test_basic_analysis():
    """Test basic analysis functionality"""
    print("✅ Testing basic analysis...")
    
    try:
        # Import the analyzer
        from basic_analysis_script import ESFBasicAnalyzer
        
        # Create analyzer instance
        analyzer = ESFBasicAnalyzer(
            'cleaned_data/esf_projects_cleaned.csv',
            'cleaned_data/esf_beneficiaries_cleaned.csv'
        )
        
        # Test basic functionality
        projects_analysis = analyzer.analyze_projects_overview()
        beneficiaries_analysis = analyzer.analyze_beneficiaries_overview()
        cross_analysis = analyzer.analyze_cross_dataset_relationships()
        
        print("✅ Basic analysis test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 ESF ANALYSIS FUNCTIONALITY TEST")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Data Files Test", test_data_files),
        ("Basic Analysis Test", test_basic_analysis)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📋 TEST RESULTS SUMMARY:")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Your ESF analysis setup is working correctly.")
    else:
        print("⚠️  SOME TESTS FAILED. Please check the errors above.")
    print("=" * 50)

if __name__ == "__main__":
    main()
