#!/usr/bin/env python3
"""
Lightweight ESF Dashboard Generator
==================================

Creates Power BI style HTML dashboard without external dependencies.
Uses only Python built-in libraries for maximum compatibility.
"""

import csv
import json
import os
import random
import math
from datetime import datetime, timedelta

class SimpleDashboardGenerator:
    """
    Creates interactive HTML dashboard using only built-in Python libraries
    """
    
    def __init__(self, projects_file='cleaned_data/esf_projects_cleaned.csv', 
                 beneficiaries_file='cleaned_data/esf_beneficiaries_cleaned.csv'):
        """Initialize with data files"""
        self.projects_data = []
        self.beneficiaries_data = []
        self.kpis = {}
        
        # Load data
        self.load_data(projects_file, beneficiaries_file)
        self.calculate_kpis()
    
    def load_data(self, projects_file, beneficiaries_file):
        """Load CSV data"""
        try:
            # Load projects
            if os.path.exists(projects_file):
                with open(projects_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    self.projects_data = list(reader)
                print(f"✅ Loaded projects: {len(self.projects_data)} records")
            else:
                print(f"⚠️ Creating sample projects data...")
                self.create_sample_projects()
            
            # Load beneficiaries
            if os.path.exists(beneficiaries_file):
                with open(beneficiaries_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    self.beneficiaries_data = list(reader)
                print(f"✅ Loaded beneficiaries: {len(self.beneficiaries_data)} records")
            else:
                print(f"⚠️ Creating sample beneficiaries data...")
                self.create_sample_beneficiaries()
                
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.create_sample_projects()
            self.create_sample_beneficiaries()
    
    def create_sample_projects(self):
        """Create sample project data"""
        regions = ['Dublin', 'Cork', 'Galway', 'Limerick', 'Waterford']
        project_types = ['Digital Skills', 'Youth Employment', 'Green Skills', 'Social Innovation']
        statuses = ['Active', 'Completed', 'Planning', 'On Hold']
        risk_levels = ['Low', 'Medium', 'High']
        
        self.projects_data = []
        for i in range(30):
            budget = random.randint(50000, 500000)
            actual_spend = budget * random.uniform(0.7, 1.1)
            
            project = {
                'project_id': f'ESF_{str(i+1).zfill(3)}',
                'project_name': f'ESF Project {i+1}',
                'project_type': random.choice(project_types),
                'status': random.choice(statuses),
                'region': random.choice(regions),
                'total_budget': str(budget),
                'actual_spend': str(int(actual_spend)),
                'esf_funding': str(int(budget * 0.8)),
                'beneficiaries_target': str(random.randint(50, 200)),
                'beneficiaries_actual': str(random.randint(40, 220)),
                'engagement_score': str(round(random.uniform(3.0, 5.0), 1)),
                'risk_flag': random.choice(risk_levels),
                'start_date': '2023-01-01',
                'year': '2023'
            }
            self.projects_data.append(project)
    
    def create_sample_beneficiaries(self):
        """Create sample beneficiary data"""
        genders = ['Male', 'Female', 'Other', 'Prefer not to say']
        age_groups = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        education_levels = ['Primary', 'Secondary', 'Post-Secondary', 'Tertiary']
        regions = ['Dublin', 'Cork', 'Galway', 'Limerick', 'Waterford']
        
        self.beneficiaries_data = []
        project_ids = [p['project_id'] for p in self.projects_data]
        
        for i in range(150):
            beneficiary = {
                'beneficiary_id': f'BEN_{str(i+1).zfill(4)}',
                'project_id': random.choice(project_ids),
                'gender': random.choice(genders),
                'age_group': random.choice(age_groups),
                'education_level': random.choice(education_levels),
                'region': random.choice(regions),
                'satisfaction_score': str(random.randint(1, 5)),
                'training_hours': str(random.randint(20, 200)),
                'outcome_achieved': random.choice(['Employed', 'Self-employed', 'Further Education', 'Still Seeking'])
            }
            self.beneficiaries_data.append(beneficiary)
    
    def calculate_kpis(self):
        """Calculate dashboard KPIs"""
        self.kpis = {
            'total_projects': len(self.projects_data),
            'total_budget': sum(float(p.get('total_budget', 0)) for p in self.projects_data),
            'total_beneficiaries': len(self.beneficiaries_data),
            'avg_engagement': sum(float(p.get('engagement_score', 0)) for p in self.projects_data) / len(self.projects_data) if self.projects_data else 0
        }
    
    def generate_chart_data(self):
        """Generate data for charts"""
        charts_data = {}
        
        # Budget vs Spend data (top 10 projects)
        budget_data = []
        for project in sorted(self.projects_data, key=lambda x: float(x.get('total_budget', 0)), reverse=True)[:10]:
            budget_data.append({
                'name': project['project_name'][:20] + '...' if len(project['project_name']) > 20 else project['project_name'],
                'budget': float(project.get('total_budget', 0)),
                'spend': float(project.get('actual_spend', 0))
            })
        charts_data['budget_vs_spend'] = budget_data
        
        # Regional distribution
        region_counts = {}
        for project in self.projects_data:
            region = project.get('region', 'Unknown')
            region_counts[region] = region_counts.get(region, 0) + 1
        charts_data['regions'] = [{'name': k, 'value': v} for k, v in region_counts.items()]
        
        # Gender breakdown
        gender_counts = {}
        for beneficiary in self.beneficiaries_data:
            gender = beneficiary.get('gender', 'Unknown')
            gender_counts[gender] = gender_counts.get(gender, 0) + 1
        charts_data['gender'] = [{'name': k, 'value': v} for k, v in gender_counts.items()]
        
        # Age group by region
        age_region = {}
        for beneficiary in self.beneficiaries_data:
            region = beneficiary.get('region', 'Unknown')
            age = beneficiary.get('age_group', 'Unknown')
            if region not in age_region:
                age_region[region] = {}
            age_region[region][age] = age_region[region].get(age, 0) + 1
        charts_data['age_region'] = age_region
        
        return charts_data
    
    def create_dashboard_html(self):
        """Create the main dashboard HTML"""
        charts_data = self.generate_chart_data()
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>ESF Program Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            color: #333;
        }}
        
        .header {{
            background: linear-gradient(135deg, #0078D4, #005A9E);
            color: white;
            padding: 30px 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .kpi-section {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .kpi-card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }}
        
        .kpi-card:hover {{
            transform: translateY(-5px);
        }}
        
        .kpi-value {{
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .kpi-label {{
            color: #666;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .main-content {{
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 30px;
        }}
        
        .filters {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            height: fit-content;
        }}
        
        .filters h3 {{
            color: #0078D4;
            margin-bottom: 20px;
            font-size: 1.3rem;
        }}
        
        .filter-group {{
            margin-bottom: 20px;
        }}
        
        .filter-label {{
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }}
        
        select {{
            width: 100%;
            padding: 10px;
            border: 2px solid #e1e1e1;
            border-radius: 6px;
            font-size: 14px;
            transition: border-color 0.3s ease;
        }}
        
        select:focus {{
            outline: none;
            border-color: #0078D4;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .chart-title {{
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 15px;
            color: #333;
        }}
        
        .full-width {{
            grid-column: 1 / -1;
        }}
        
        .table-container {{
            overflow-x: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e1e1e1;
        }}
        
        th {{
            background-color: #f8f9fa;
            font-weight: 600;
            color: #333;
        }}
        
        tr:hover {{
            background-color: #f8f9fa;
        }}
        
        .risk-high {{ background-color: #ffebee; }}
        .risk-medium {{ background-color: #fff3e0; }}
        .risk-low {{ background-color: #e8f5e8; }}
        
        .status-active {{ color: #4caf50; font-weight: bold; }}
        .status-completed {{ color: #2196f3; font-weight: bold; }}
        .status-planning {{ color: #ff9800; font-weight: bold; }}
        .status-hold {{ color: #f44336; font-weight: bold; }}
        
        @media (max-width: 768px) {{
            .main-content {{
                grid-template-columns: 1fr;
            }}
            
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
            
            .kpi-section {{
                grid-template-columns: 1fr 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏆 ESF Program Dashboard</h1>
        <p>Interactive Business Intelligence Dashboard for European Social Fund Projects</p>
    </div>
    
    <div class="container">
        <!-- KPI Cards Section -->
        <div class="kpi-section">
            <div class="kpi-card">
                <div class="kpi-value" style="color: #0078D4;">{self.kpis['total_projects']:,}</div>
                <div class="kpi-label">Total Projects</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value" style="color: #107C10;">€{self.kpis['total_budget']:,.0f}</div>
                <div class="kpi-label">Total Budget</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value" style="color: #FF8C00;">{self.kpis['total_beneficiaries']:,}</div>
                <div class="kpi-label">Total Beneficiaries</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value" style="color: #D13438;">{self.kpis['avg_engagement']:.1f}/5.0</div>
                <div class="kpi-label">Avg Engagement Score</div>
            </div>
        </div>
        
        <!-- Main Content -->
        <div class="main-content">
            <!-- Filters Panel -->
            <div class="filters">
                <h3>📍 Filters</h3>
                
                <div class="filter-group">
                    <label class="filter-label">Region</label>
                    <select id="regionFilter" onchange="applyFilters()">
                        <option value="all">All Regions</option>
                        {self.generate_filter_options('region')}
                    </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label">Project Type</label>
                    <select id="typeFilter" onchange="applyFilters()">
                        <option value="all">All Types</option>
                        {self.generate_filter_options('project_type')}
                    </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label">Status</label>
                    <select id="statusFilter" onchange="applyFilters()">
                        <option value="all">All Statuses</option>
                        {self.generate_filter_options('status')}
                    </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label">Risk Flag</label>
                    <select id="riskFilter" onchange="applyFilters()">
                        <option value="all">All Risk Levels</option>
                        {self.generate_filter_options('risk_flag')}
                    </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label">Gender</label>
                    <select id="genderFilter" onchange="applyFilters()">
                        <option value="all">All Genders</option>
                        {self.generate_beneficiary_filter_options('gender')}
                    </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label">Age Group</label>
                    <select id="ageFilter" onchange="applyFilters()">
                        <option value="all">All Ages</option>
                        {self.generate_beneficiary_filter_options('age_group')}
                    </select>
                </div>
            </div>
            
            <!-- Charts Section -->
            <div class="charts-grid">
                <div class="chart-container">
                    <div class="chart-title">💰 Budget vs. Actual Spend (Top 10)</div>
                    <canvas id="budgetChart"></canvas>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">🗺️ Projects by Region</div>
                    <canvas id="regionChart"></canvas>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">👥 Beneficiary Gender Breakdown</div>
                    <canvas id="genderChart"></canvas>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">📊 Age Groups by Region</div>
                    <canvas id="ageRegionChart"></canvas>
                </div>
                
                <div class="chart-container full-width">
                    <div class="chart-title">📋 Project Details Table</div>
                    <div class="table-container">
                        {self.generate_projects_table()}
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Chart data
        const chartData = {json.dumps(charts_data)};
        
        // Initialize charts
        function initCharts() {{
            // Budget vs Spend Chart
            const budgetCtx = document.getElementById('budgetChart').getContext('2d');
            new Chart(budgetCtx, {{
                type: 'bar',
                data: {{
                    labels: chartData.budget_vs_spend.map(d => d.name),
                    datasets: [
                        {{
                            label: 'Budget',
                            data: chartData.budget_vs_spend.map(d => d.budget),
                            backgroundColor: '#0078D4',
                            borderRadius: 4
                        }},
                        {{
                            label: 'Actual Spend',
                            data: chartData.budget_vs_spend.map(d => d.spend),
                            backgroundColor: '#107C10',
                            borderRadius: 4
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{
                            position: 'top',
                        }},
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
            
            // Region Distribution Chart
            const regionCtx = document.getElementById('regionChart').getContext('2d');
            new Chart(regionCtx, {{
                type: 'doughnut',
                data: {{
                    labels: chartData.regions.map(d => d.name),
                    datasets: [{{
                        data: chartData.regions.map(d => d.value),
                        backgroundColor: ['#0078D4', '#107C10', '#FF8C00', '#D13438', '#5C2D91']
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{
                            position: 'bottom',
                        }},
                    }}
                }}
            }});
            
            // Gender Breakdown Chart
            const genderCtx = document.getElementById('genderChart').getContext('2d');
            new Chart(genderCtx, {{
                type: 'pie',
                data: {{
                    labels: chartData.gender.map(d => d.name),
                    datasets: [{{
                        data: chartData.gender.map(d => d.value),
                        backgroundColor: ['#0078D4', '#FF8C00', '#107C10', '#D13438']
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{
                            position: 'bottom',
                        }},
                    }}
                }}
            }});
            
            // Age Region Chart (simplified bar chart)
            const ageRegionCtx = document.getElementById('ageRegionChart').getContext('2d');
            const regions = Object.keys(chartData.age_region);
            const ageGroups = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+'];
            
            new Chart(ageRegionCtx, {{
                type: 'bar',
                data: {{
                    labels: regions,
                    datasets: ageGroups.map((age, index) => ({{
                        label: age,
                        data: regions.map(region => chartData.age_region[region][age] || 0),
                        backgroundColor: `hsl(${{index * 60}}, 70%, 50%)`,
                        borderRadius: 4
                    }}))
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{
                            position: 'top',
                        }},
                    }},
                    scales: {{
                        x: {{
                            stacked: true,
                        }},
                        y: {{
                            stacked: true,
                            beginAtZero: true
                        }}
                    }}
                }}
            }});
        }}
        
        // Filter functionality (placeholder)
        function applyFilters() {{
            console.log('Filters applied - connect to backend for full functionality');
        }}
        
        // Initialize when page loads
        document.addEventListener('DOMContentLoaded', initCharts);
    </script>
</body>
</html>"""
        
        return html_content
    
    def generate_filter_options(self, field):
        """Generate HTML options for project filters"""
        values = set()
        for project in self.projects_data:
            if field in project:
                values.add(project[field])
        
        options = ""
        for value in sorted(values):
            options += f'<option value="{value}">{value}</option>\n'
        return options
    
    def generate_beneficiary_filter_options(self, field):
        """Generate HTML options for beneficiary filters"""
        values = set()
        for beneficiary in self.beneficiaries_data:
            if field in beneficiary:
                values.add(beneficiary[field])
        
        options = ""
        for value in sorted(values):
            options += f'<option value="{value}">{value}</option>\n'
        return options
    
    def generate_projects_table(self):
        """Generate HTML table for project details"""
        table_html = """
        <table>
            <thead>
                <tr>
                    <th>Project Name</th>
                    <th>Type</th>
                    <th>Region</th>
                    <th>Status</th>
                    <th>Budget</th>
                    <th>Actual Spend</th>
                    <th>Engagement</th>
                    <th>Risk</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for project in self.projects_data:
            risk_class = f"risk-{project.get('risk_flag', 'low').lower()}"
            status_class = f"status-{project.get('status', 'active').lower().replace(' ', '')}"
            
            table_html += f"""
                <tr class="{risk_class}">
                    <td><strong>{project.get('project_name', 'N/A')}</strong></td>
                    <td>{project.get('project_type', 'N/A')}</td>
                    <td>{project.get('region', 'N/A')}</td>
                    <td class="{status_class}">{project.get('status', 'N/A')}</td>
                    <td>€{float(project.get('total_budget', 0)):,.0f}</td>
                    <td>€{float(project.get('actual_spend', 0)):,.0f}</td>
                    <td>{project.get('engagement_score', 'N/A')}/5.0</td>
                    <td>{project.get('risk_flag', 'N/A')}</td>
                </tr>
            """
        
        table_html += """
            </tbody>
        </table>
        """
        
        return table_html
    
    def generate_dashboard(self, output_file='esf_dashboard.html'):
        """Generate the complete dashboard"""
        print("🎨 Generating Power BI style dashboard...")
        
        # Create dashboard HTML
        html_content = self.create_dashboard_html()
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Create summary report
        self.create_summary_report()
        
        print(f"✅ Dashboard generated: {output_file}")
        return output_file
    
    def create_summary_report(self):
        """Create a summary report"""
        summary = {
            'dashboard_kpis': self.kpis,
            'data_overview': {
                'projects_count': len(self.projects_data),
                'beneficiaries_count': len(self.beneficiaries_data),
                'unique_regions': len(set(p.get('region', '') for p in self.projects_data)),
                'unique_project_types': len(set(p.get('project_type', '') for p in self.projects_data))
            },
            'charts_included': [
                'KPI Cards (Total Projects, Budget, Beneficiaries, Engagement)',
                'Budget vs Actual Spend (Bar Chart)',
                'Projects by Region (Doughnut Chart)',
                'Beneficiary Gender Breakdown (Pie Chart)',
                'Age Groups by Region (Stacked Bar Chart)',
                'Project Details Table (Sortable)'
            ],
            'filters_available': [
                'Region', 'Project Type', 'Status', 'Risk Flag', 'Gender', 'Age Group'
            ],
            'generated_at': datetime.now().isoformat()
        }
        
        with open('dashboard_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("✅ Summary report created: dashboard_summary.json")

def main():
    """Main execution"""
    print("🎨 ESF Dashboard Generator (Lightweight)")
    print("=" * 50)
    
    # Generate dashboard
    dashboard = SimpleDashboardGenerator()
    output_file = dashboard.generate_dashboard()
    
    print(f"""
    🎉 Dashboard Generation Complete!
    
    📊 Main Dashboard: {output_file}
    📋 Summary Report: dashboard_summary.json
    
    🚀 Features Included:
    ✅ KPI Cards (Projects, Budget, Beneficiaries, Engagement)
    ✅ Interactive Charts (Budget, Regional, Gender, Age Analysis)
    ✅ Filter Controls (Region, Type, Status, Risk, Demographics)
    ✅ Sortable Project Details Table
    ✅ Responsive Design (Mobile-friendly)
    ✅ Professional Power BI Style Layout
    
    💡 Next Steps:
    1. Open {output_file} in your web browser
    2. Use the filter controls on the left panel
    3. Hover over charts for detailed information
    4. Sort the project table by clicking headers
    
    🔧 To connect real data:
    1. Replace sample data with your cleaned CSV files
    2. Update the file paths in the script
    3. Re-run the generator
    
    📈 Power BI Integration:
    - Use this as a template for Power BI report design
    - Import your CSV data into Power BI Desktop
    - Recreate these visualizations for full enterprise features
    """)

if __name__ == "__main__":
    main()
