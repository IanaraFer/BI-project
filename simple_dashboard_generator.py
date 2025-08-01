#!/usr/bin/env python3
"""
ESF Dashboard Generator
======================

This script creates an interactive web dashboard for ESF (European Social Fund) data analysis.
It generates a Power BI style dashboard using HTML, CSS, and Chart.js.

Features:
- Interactive charts and KPI cards
- Responsive design
- Professional styling
- No external dependencies (all assets embedded)

Usage:
    python simple_dashboard_generator.py
"""

import pandas as pd
import json
import os
from datetime import datetime

class PowerBIDashboardGenerator:
    def __init__(self):
        self.projects_df = None
        self.beneficiaries_df = None
        self.kpis = {}
    
    def load_data(self):
        """Load cleaned ESF data"""
        try:
            # Try to load cleaned data
            if os.path.exists('cleaned_data/esf_projects_cleaned.csv'):
                self.projects_df = pd.read_csv('cleaned_data/esf_projects_cleaned.csv')
                print(f"✅ Loaded {len(self.projects_df)} projects")
            else:
                print("❌ No projects data found. Please run data_cleaning_script.py first.")
                return False
            
            if os.path.exists('cleaned_data/esf_beneficiaries_cleaned.csv'):
                self.beneficiaries_df = pd.read_csv('cleaned_data/esf_beneficiaries_cleaned.csv')
                print(f"✅ Loaded {len(self.beneficiaries_df)} beneficiaries")
            else:
                print("❌ No beneficiaries data found. Please run data_cleaning_script.py first.")
                return False
                
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def calculate_kpis(self):
        """Calculate key performance indicators"""
        print("📊 Calculating KPIs...")
        
        # Project KPIs
        if self.projects_df is not None:
            self.kpis['total_projects'] = len(self.projects_df)
            self.kpis['total_budget'] = self.projects_df['total_budget'].sum()
            self.kpis['total_esf_funding'] = self.projects_df['esf_funding'].sum()
            self.kpis['esf_funding_rate'] = (self.kpis['total_esf_funding'] / self.kpis['total_budget']) * 100
            
            # Project status
            status_counts = self.projects_df['status'].value_counts()
            self.kpis['active_projects'] = status_counts.get('Active', 0)
            self.kpis['completed_projects'] = status_counts.get('Completed', 0)
            
            # Performance
            if 'target_achievement_rate' in self.projects_df.columns:
                self.kpis['avg_target_achievement'] = self.projects_df['target_achievement_rate'].mean()
                self.kpis['projects_over_target'] = len(self.projects_df[self.projects_df['target_achievement_rate'] > 100])
        
        # Beneficiary KPIs
        if self.beneficiaries_df is not None:
            self.kpis['total_beneficiaries'] = len(self.beneficiaries_df)
            
            if 'training_hours' in self.beneficiaries_df.columns:
                self.kpis['total_training_hours'] = self.beneficiaries_df['training_hours'].sum()
                self.kpis['avg_training_hours'] = self.beneficiaries_df['training_hours'].mean()
            
            if 'satisfaction_score' in self.beneficiaries_df.columns:
                self.kpis['avg_satisfaction'] = self.beneficiaries_df['satisfaction_score'].mean()
            
            if 'outcome_achieved' in self.beneficiaries_df.columns:
                employment_outcomes = ['Employed', 'Self-employed']
                successful = self.beneficiaries_df[self.beneficiaries_df['outcome_achieved'].isin(employment_outcomes)]
                self.kpis['employment_success_rate'] = (len(successful) / len(self.beneficiaries_df)) * 100
        
        # Combined KPIs
        if self.kpis.get('total_budget') and self.kpis.get('total_beneficiaries'):
            self.kpis['cost_per_beneficiary'] = self.kpis['total_budget'] / self.kpis['total_beneficiaries']
        
        print(f"✅ Calculated {len(self.kpis)} KPIs")
    
    def generate_chart_data(self):
        """Generate data for charts"""
        chart_data = {}
        
        # Project status pie chart
        if self.projects_df is not None:
            status_counts = self.projects_df['status'].value_counts()
            chart_data['project_status'] = {
                'labels': status_counts.index.tolist(),
                'data': status_counts.values.tolist(),
                'colors': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
            }
            
            # Regional distribution
            region_counts = self.projects_df['region'].value_counts()
            chart_data['regional_distribution'] = {
                'labels': region_counts.index.tolist(),
                'data': region_counts.values.tolist()
            }
            
            # Budget by project type
            budget_by_type = self.projects_df.groupby('project_type')['total_budget'].sum()
            chart_data['budget_by_type'] = {
                'labels': budget_by_type.index.tolist(),
                'data': budget_by_type.values.tolist()
            }
        
        # Demographics charts
        if self.beneficiaries_df is not None:
            # Gender distribution
            gender_counts = self.beneficiaries_df['gender'].value_counts()
            chart_data['gender_distribution'] = {
                'labels': gender_counts.index.tolist(),
                'data': gender_counts.values.tolist(),
                'colors': ['#FF9999', '#66B2FF']
            }
            
            # Employment outcomes
            if 'outcome_achieved' in self.beneficiaries_df.columns:
                outcome_counts = self.beneficiaries_df['outcome_achieved'].value_counts()
                chart_data['employment_outcomes'] = {
                    'labels': outcome_counts.index.tolist(),
                    'data': outcome_counts.values.tolist()
                }
        
        return chart_data
    
    def create_dashboard_html(self):
        """Create the interactive dashboard HTML"""
        chart_data = self.generate_chart_data()
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESF Program Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .dashboard-container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .kpi-section {{
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .kpi-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            border-left: 4px solid;
            transition: transform 0.3s ease;
        }}
        
        .kpi-card:hover {{
            transform: translateY(-5px);
        }}
        
        .kpi-card.primary {{ border-color: #3498db; }}
        .kpi-card.success {{ border-color: #27ae60; }}
        .kpi-card.warning {{ border-color: #f39c12; }}
        .kpi-card.info {{ border-color: #9b59b6; }}
        
        .kpi-value {{
            font-size: 2.2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .kpi-label {{
            color: #666;
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .charts-section {{
            padding: 30px;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
        }}
        
        .chart-container {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }}
        
        .chart-title {{
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 20px;
            color: #2c3e50;
            text-align: center;
        }}
        
        .chart-canvas {{
            max-height: 300px;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}
            
            .kpi-grid {{
                grid-template-columns: 1fr;
            }}
            
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
            
            .chart-container {{
                padding: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="header">
            <h1>🌟 ESF Program Dashboard</h1>
            <p>European Social Fund Performance Analytics</p>
            <p style="font-size: 0.9em; margin-top: 10px;">Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
        </div>
        
        <div class="kpi-section">
            <h2 style="color: #2c3e50; margin-bottom: 15px;">📊 Key Performance Indicators</h2>
            <div class="kpi-grid">
                <div class="kpi-card primary">
                    <div class="kpi-value">{self.kpis.get('total_projects', 0):,}</div>
                    <div class="kpi-label">Total Projects</div>
                </div>
                <div class="kpi-card success">
                    <div class="kpi-value">€{self.kpis.get('total_budget', 0):,.0f}</div>
                    <div class="kpi-label">Total Budget</div>
                </div>
                <div class="kpi-card warning">
                    <div class="kpi-value">{self.kpis.get('total_beneficiaries', 0):,}</div>
                    <div class="kpi-label">Total Beneficiaries</div>
                </div>
                <div class="kpi-card info">
                    <div class="kpi-value">{self.kpis.get('employment_success_rate', 0):.1f}%</div>
                    <div class="kpi-label">Employment Success Rate</div>
                </div>
                <div class="kpi-card primary">
                    <div class="kpi-value">{self.kpis.get('esf_funding_rate', 0):.1f}%</div>
                    <div class="kpi-label">ESF Funding Rate</div>
                </div>
                <div class="kpi-card success">
                    <div class="kpi-value">{self.kpis.get('avg_target_achievement', 0):.1f}%</div>
                    <div class="kpi-label">Avg Target Achievement</div>
                </div>
                <div class="kpi-card warning">
                    <div class="kpi-value">{self.kpis.get('total_training_hours', 0):,.0f}</div>
                    <div class="kpi-label">Training Hours Delivered</div>
                </div>
                <div class="kpi-card info">
                    <div class="kpi-value">€{self.kpis.get('cost_per_beneficiary', 0):,.0f}</div>
                    <div class="kpi-label">Cost per Beneficiary</div>
                </div>
            </div>
        </div>
        
        <div class="charts-section">
            <h2 style="color: #2c3e50; margin-bottom: 25px;">📈 Performance Analytics</h2>
            <div class="charts-grid">
                <div class="chart-container">
                    <div class="chart-title">Project Status Distribution</div>
                    <canvas id="statusChart" class="chart-canvas"></canvas>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">Regional Distribution</div>
                    <canvas id="regionChart" class="chart-canvas"></canvas>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">Budget by Project Type</div>
                    <canvas id="budgetChart" class="chart-canvas"></canvas>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">Employment Outcomes</div>
                    <canvas id="outcomeChart" class="chart-canvas"></canvas>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>ESF Business Intelligence Dashboard | Generated by ESF BI Project | Data as of {datetime.now().strftime('%Y-%m-%d')}</p>
        </div>
    </div>

    <script>
        // Chart configuration
        Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
        Chart.defaults.color = '#2c3e50';
        
        // Project Status Chart
        const statusCtx = document.getElementById('statusChart').getContext('2d');
        new Chart(statusCtx, {{
            type: 'doughnut',
            data: {{
                labels: {chart_data.get('project_status', {}).get('labels', [])},
                datasets: [{{
                    data: {chart_data.get('project_status', {}).get('data', [])},
                    backgroundColor: {chart_data.get('project_status', {}).get('colors', ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])},
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 20,
                            usePointStyle: true
                        }}
                    }}
                }}
            }}
        }});
        
        // Regional Distribution Chart
        const regionCtx = document.getElementById('regionChart').getContext('2d');
        new Chart(regionCtx, {{
            type: 'bar',
            data: {{
                labels: {chart_data.get('regional_distribution', {}).get('labels', [])},
                datasets: [{{
                    label: 'Projects',
                    data: {chart_data.get('regional_distribution', {}).get('data', [])},
                    backgroundColor: 'rgba(52, 152, 219, 0.8)',
                    borderColor: 'rgba(52, 152, 219, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 1
                        }}
                    }}
                }}
            }}
        }});
        
        // Budget by Type Chart
        const budgetCtx = document.getElementById('budgetChart').getContext('2d');
        new Chart(budgetCtx, {{
            type: 'bar',
            data: {{
                labels: {chart_data.get('budget_by_type', {}).get('labels', [])},
                datasets: [{{
                    label: 'Budget (€)',
                    data: {chart_data.get('budget_by_type', {}).get('data', [])},
                    backgroundColor: 'rgba(46, 204, 113, 0.8)',
                    borderColor: 'rgba(46, 204, 113, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return '€' + value.toLocaleString();
                            }}
                        }}
                    }}
                }}
            }}
        }});
        
        // Employment Outcomes Chart
        const outcomeCtx = document.getElementById('outcomeChart').getContext('2d');
        new Chart(outcomeCtx, {{
            type: 'pie',
            data: {{
                labels: {chart_data.get('employment_outcomes', {}).get('labels', [])},
                datasets: [{{
                    data: {chart_data.get('employment_outcomes', {}).get('data', [])},
                    backgroundColor: ['#9b59b6', '#e74c3c', '#f39c12', '#1abc9c'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 20,
                            usePointStyle: true
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
        
        return html_content
    
    def save_dashboard(self, filename='esf_dashboard.html'):
        """Save the dashboard to HTML file"""
        try:
            html_content = self.create_dashboard_html()
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ Dashboard saved as: {filename}")
            print(f"🌐 Open the file in your browser to view the dashboard")
            
            # Save KPIs as JSON for reference
            with open('cleaned_data/dashboard_kpis.json', 'w') as f:
                json.dump(self.kpis, f, indent=2, default=str)
            print("✅ KPIs saved to: cleaned_data/dashboard_kpis.json")
            
        except Exception as e:
            print(f"❌ Error saving dashboard: {e}")

def main():
    """Main execution function"""
    print("🎨 ESF DASHBOARD GENERATOR")
    print("=" * 50)
    
    # Create dashboard generator
    generator = PowerBIDashboardGenerator()
    
    # Load data
    if not generator.load_data():
        print("❌ Cannot proceed without data. Please run data_cleaning_script.py first.")
        return
    
    # Calculate KPIs
    generator.calculate_kpis()
    
    # Generate and save dashboard
    generator.save_dashboard()
    
    print("\n" + "=" * 50)
    print("🎉 DASHBOARD GENERATION COMPLETED!")
    print("=" * 50)
    print("\n📁 Files created:")
    print("   🌐 esf_dashboard.html - Interactive dashboard")
    print("   📊 cleaned_data/dashboard_kpis.json - KPI data")
    print("\n💡 Next steps:")
    print("   1. Open esf_dashboard.html in your web browser")
    print("   2. Share the dashboard file for presentations")
    print("   3. Use the KPI data for Power BI integration")

if __name__ == "__main__":
    main()
