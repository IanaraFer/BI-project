#!/usr/bin/env python3
"""
Quick test for matplotlib and seaborn installation
"""

def test_visualization_packages():
    """Test if visualization packages are working"""
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd
        import numpy as np
        
        print("✅ All visualization packages imported successfully!")
        print(f"✅ Matplotlib version: {plt.matplotlib.__version__}")
        print(f"✅ Seaborn version: {sns.__version__}")
        print(f"✅ Pandas version: {pd.__version__}")
        print(f"✅ NumPy version: {np.__version__}")
        
        # Test basic plotting functionality
        plt.figure(figsize=(6, 4))
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        plt.plot(x, y)
        plt.title("Test Plot")
        plt.close()  # Close without showing
        
        print("✅ Basic plotting functionality works!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TESTING VISUALIZATION PACKAGES")
    print("=" * 40)
    success = test_visualization_packages()
    print("=" * 40)
    if success:
        print("🎉 Ready to run data_analysis_script.py!")
    else:
        print("⚠️  Issues detected with visualization packages")
