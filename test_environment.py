#!/usr/bin/env python3
"""
Test script to check Python environment and packages
"""

print("🐍 Testing Python Environment...")
print("=" * 40)

try:
    import sys
    print(f"✅ Python version: {sys.version}")
    print(f"✅ Python executable: {sys.executable}")
except Exception as e:
    print(f"❌ Python import error: {e}")

try:
    import pandas as pd
    print(f"✅ Pandas version: {pd.__version__}")
except Exception as e:
    print(f"❌ Pandas import error: {e}")

try:
    import numpy as np
    print(f"✅ NumPy version: {np.__version__}")
except Exception as e:
    print(f"❌ NumPy import error: {e}")

try:
    import matplotlib.pyplot as plt
    print(f"✅ Matplotlib imported successfully")
except Exception as e:
    print(f"❌ Matplotlib import error: {e}")

try:
    import seaborn as sns
    print(f"✅ Seaborn imported successfully")
except Exception as e:
    print(f"❌ Seaborn import error: {e}")

print("\n🔍 Checking data files...")
import os

if os.path.exists('cleaned_data/esf_projects_cleaned.csv'):
    print("✅ Projects data file exists")
else:
    print("❌ Projects data file missing")

if os.path.exists('cleaned_data/esf_beneficiaries_cleaned.csv'):
    print("✅ Beneficiaries data file exists")
else:
    print("❌ Beneficiaries data file missing")

print("\n" + "=" * 40)
print("🎯 Environment test completed!")
