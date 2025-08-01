#!/usr/bin/env python3
"""
Project Cleanup Script
======================
This script removes unnecessary files and organizes the ESF BI project structure.
"""

import os
import shutil
from pathlib import Path

def cleanup_project():
    """Clean up the ESF BI project directory"""
    project_root = Path("c:/Users/35387/Desktop/BI project")
    
    print("🧹 CLEANING UP ESF BI PROJECT")
    print("=" * 50)
    
    # Files to keep (core project files)
    keep_files = {
        # Core Python scripts
        'data_cleaning_script.py',
        'basic_analysis_script.py', 
        'data_analysis_script.py',
        'simple_dashboard_generator.py',
        'simple_analysis_script.py',
        'simple_visualization_script.py',
        
        # Main dashboard and data
        'esf_dashboard.html',
        'esf_projects.csv',
        'esf_beneficiaries.csv',
        
        # Documentation
        'README.md',
        'DAX_MEASURES_REFERENCE.md',
        'POWER_BI_SETUP_GUIDE.md',
        'INSTALLATION_SUCCESS.md'
    }
    
    # Folders to keep
    keep_folders = {
        '.conda',
        '.git', 
        'cleaned_data'
    }
    
    # Get all items in project directory
    all_items = list(project_root.iterdir())
    
    removed_count = 0
    kept_count = 0
    
    for item in all_items:
        if item.is_file():
            if item.name in keep_files:
                print(f"✅ KEEP: {item.name}")
                kept_count += 1
            else:
                try:
                    item.unlink()
                    print(f"🗑️  REMOVED: {item.name}")
                    removed_count += 1
                except Exception as e:
                    print(f"❌ ERROR removing {item.name}: {e}")
        
        elif item.is_dir():
            if item.name in keep_folders:
                print(f"📁 KEEP: {item.name}/")
                kept_count += 1
            else:
                try:
                    shutil.rmtree(item)
                    print(f"🗑️  REMOVED: {item.name}/")
                    removed_count += 1
                except Exception as e:
                    print(f"❌ ERROR removing {item.name}/: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 CLEANUP COMPLETED!")
    print("=" * 50)
    print(f"📁 Files/Folders Kept: {kept_count}")
    print(f"🗑️  Files/Folders Removed: {removed_count}")
    
    # Show final structure
    print(f"\n📂 FINAL PROJECT STRUCTURE:")
    print("=" * 30)
    remaining_items = sorted(project_root.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
    for item in remaining_items:
        if item.is_dir():
            print(f"📁 {item.name}/")
        else:
            print(f"📄 {item.name}")

if __name__ == "__main__":
    cleanup_project()
