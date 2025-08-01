# ESF BI Project Cleanup Script
# Run this in PowerShell to clean up unnecessary files

Write-Host "🧹 Starting ESF BI Project Cleanup..." -ForegroundColor Green
Write-Host "=" * 50

# Set project directory
$projectDir = "c:\Users\35387\Desktop\BI project"
Set-Location $projectDir

# Remove download files
Write-Host "🗑️  Removing download files..." -ForegroundColor Yellow
Get-ChildItem -Name "*.download" | Remove-Item -Force -ErrorAction SilentlyContinue
Remove-Item "favicon" -Force -ErrorAction SilentlyContinue
Remove-Item "n59ae4ieqq" -Force -ErrorAction SilentlyContinue
Remove-Item "src=8406097*" -Force -ErrorAction SilentlyContinue
Remove-Item "markdow" -Force -ErrorAction SilentlyContinue
Remove-Item "index-ujTYYV9o.css" -Force -ErrorAction SilentlyContinue

# Remove duplicate and old scripts
Write-Host "🗑️  Removing duplicate scripts..." -ForegroundColor Yellow
Remove-Item "*_fixed.py" -Force -ErrorAction SilentlyContinue
Remove-Item "powerbi_dashboard_generator.py" -Force -ErrorAction SilentlyContinue
Remove-Item "data_conversion_guide.py" -Force -ErrorAction SilentlyContinue
Remove-Item "simple_analysis_script.py" -Force -ErrorAction SilentlyContinue
Remove-Item "simple_visualization_script.py" -Force -ErrorAction SilentlyContinue
Remove-Item "cleanup_project.py" -Force -ErrorAction SilentlyContinue

# Remove test files
Write-Host "🗑️  Removing test files..." -ForegroundColor Yellow
Remove-Item "test_*.py" -Force -ErrorAction SilentlyContinue
Remove-Item "dashboard_test.html" -Force -ErrorAction SilentlyContinue

# Remove old documentation (keep main ones)
Write-Host "🗑️  Removing old documentation..." -ForegroundColor Yellow
Remove-Item "ANALYSIS_STATUS_REPORT.md" -Force -ErrorAction SilentlyContinue
Remove-Item "MATPLOTLIB_INSTALLATION_SUCCESS.md" -Force -ErrorAction SilentlyContinue
Remove-Item "DASHBOARD_VIEWING_GUIDE.md" -Force -ErrorAction SilentlyContinue
Remove-Item "README_Analysis_Results.md" -Force -ErrorAction SilentlyContinue
Remove-Item "PROJECT_CLEANUP_GUIDE.md" -Force -ErrorAction SilentlyContinue

# Remove old config files
Write-Host "🗑️  Removing old config files..." -ForegroundColor Yellow
Remove-Item "*summary.json" -Force -ErrorAction SilentlyContinue
Remove-Item "run_analysis.bat" -Force -ErrorAction SilentlyContinue

# Remove cache folders
Write-Host "🗑️  Removing cache folders..." -ForegroundColor Yellow
Remove-Item "__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "esf_projects_files" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "✅ CLEANUP COMPLETED!" -ForegroundColor Green
Write-Host "=" * 50

# Show remaining files
Write-Host "📂 REMAINING PROJECT STRUCTURE:" -ForegroundColor Cyan
Write-Host "=" * 30
Get-ChildItem | Sort-Object @{Expression={$_.PSIsContainer}; Ascending=$false}, Name | ForEach-Object {
    if ($_.PSIsContainer) {
        Write-Host "📁 $($_.Name)/" -ForegroundColor Blue
    } else {
        Write-Host "📄 $($_.Name)" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "🎉 Your ESF BI project is now clean and professional!" -ForegroundColor Green
Write-Host "🚀 Ready for GitHub deployment!" -ForegroundColor Yellow
