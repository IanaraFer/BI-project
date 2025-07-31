# Dashboard Viewing Guide
## How to See Your ESF Dashboard

### 🔍 **Quick Troubleshooting Steps**

#### Option 1: Open in File Explorer
1. Open File Explorer (Windows + E)
2. Navigate to: `C:\Users\35387\Desktop\BI project`
3. Find the file: `esf_dashboard.html`
4. **Double-click** on `esf_dashboard.html`

#### Option 2: Open with Browser
1. Right-click on `esf_dashboard.html`
2. Select "Open with"
3. Choose your preferred browser:
   - Google Chrome
   - Microsoft Edge
   - Firefox
   - Safari

#### Option 3: Drag and Drop
1. Open your web browser (Chrome, Edge, Firefox)
2. Open File Explorer
3. Navigate to your project folder
4. **Drag** the `esf_dashboard.html` file
5. **Drop** it into the browser window

#### Option 4: Browser Address Bar
1. Open your web browser
2. Press **Ctrl + L** (to focus address bar)
3. Type: `file:///C:/Users/35387/Desktop/BI%20project/esf_dashboard.html`
4. Press Enter

#### Option 5: Browser File Menu
1. Open your web browser
2. Press **Ctrl + O** (Open File)
3. Navigate to: `C:\Users\35387\Desktop\BI project`
4. Select `esf_dashboard.html`
5. Click "Open"

### 🛠️ **If You Still Can't See It:**

#### Check 1: Test Dashboard
Try opening the test dashboard first:
- File: `dashboard_test.html` (simpler version)
- This will confirm if your browser works with HTML files

#### Check 2: Browser Issues
**Common Problems:**
- **Internet required**: The dashboard uses Chart.js from CDN
- **JavaScript disabled**: Enable JavaScript in browser settings
- **Pop-up blocked**: Allow local files in browser settings

**Solutions:**
1. **Chrome**: Enable "Allow access to file URLs" in settings
2. **Edge**: Should work by default
3. **Firefox**: May need to enable local file access

#### Check 3: File Permissions
1. Right-click on `esf_dashboard.html`
2. Select "Properties"
3. Check that you have "Read" permissions
4. If blocked, click "Unblock" button

### 📊 **What You Should See:**

When the dashboard loads correctly, you'll see:

**🏆 Header Section:**
- Blue gradient header with "ESF Program Dashboard" title

**📊 KPI Cards (4 cards across the top):**
- Total Projects: 100
- Total Budget: €27,652,455
- Total Beneficiaries: 500  
- Average Engagement Score: 4.0/5.0

**📍 Left Sidebar:**
- Filter controls for Region, Project Type, Status, etc.

**📈 Main Charts Area:**
- Budget vs Spend bar chart
- Regional distribution doughnut chart
- Gender breakdown pie chart
- Age groups stacked chart
- Project details table

### 🔧 **Alternative Viewing Methods:**

#### Method A: Simple Browser View
If the main dashboard doesn't work, use:
- `dashboard_test.html` - Basic version without charts

#### Method B: View Source Data
Open these files in Excel or text editor:
- `cleaned_data/esf_projects_cleaned.csv`
- `cleaned_data/esf_beneficiaries_cleaned.csv`

#### Method C: JSON Summary
Open `dashboard_summary.json` to see the KPI data:
```json
{
  "dashboard_kpis": {
    "total_projects": 100,
    "total_budget": 27652454.59,
    "total_beneficiaries": 500,
    "avg_engagement": 4.0
  }
}
```

### 📱 **Mobile/Tablet Viewing:**
If viewing on mobile device:
1. Save the HTML file to your device
2. Open with mobile browser
3. Dashboard is responsive and mobile-friendly

### 🆘 **Still Having Issues?**

**Try this step-by-step:**

1. **Open Command Prompt:**
   - Press Windows + R
   - Type `cmd` and press Enter

2. **Navigate to your folder:**
   ```cmd
   cd "C:\Users\35387\Desktop\BI project"
   ```

3. **List files to confirm:**
   ```cmd
   dir *.html
   ```

4. **Open with default browser:**
   ```cmd
   start esf_dashboard.html
   ```

### 📋 **Files You Should Have:**
- ✅ `esf_dashboard.html` (1,590 lines) - Main dashboard
- ✅ `dashboard_test.html` (80 lines) - Test version  
- ✅ `dashboard_summary.json` - Data summary
- ✅ `POWER_BI_SETUP_GUIDE.md` - Power BI guide

### 🎯 **Success Indicators:**
When it works, you'll see:
- Colorful header with blue gradient
- 4 KPI cards with large numbers
- Interactive charts that respond to mouse hover
- Filter controls on the left side
- Professional business dashboard layout

**Your dashboard is ready - just need to get it displaying properly in your browser!** 🚀
