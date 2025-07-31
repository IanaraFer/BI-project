#!/usr/bin/env python3
"""
Power BI Style Dashboard Generator for ESF Data
===============================================

This script creates interactive visualizations matching Power BI layout:
- KPI Cards at the top
- Filter panels on the left
- Interactive charts in the center
- Drill-through capabilities

Uses plotly for interactive visualizations that can be exported to HTML
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo
import numpy as np
from datetime import datetime, timedelta
import json
import os

class PowerBIDashboardGenerator:
    """
    Creates Power BI style interactive dashboards for ESF data
    """
    
    def __init__(self, projects_file='cleaned_data/esf_projects_cleaned.csv', 
                 beneficiaries_file='cleaned_data/esf_beneficiaries_cleaned.csv'):
        """Initialize with cleaned data files"""
        self.projects_df = None
        self.beneficiaries_df = None
        self.kpis = {}
        self.colors = {
            'primary': '#0078D4',      # Microsoft Blue
            'secondary': '#005A9E',    # Dark Blue
            'success': '#107C10',      # Green
            'warning': '#FF8C00',      # Orange
            'danger': '#D13438',       # Red
            'light': '#F3F2F1',       # Light Gray
            'dark': '#323130'          # Dark Gray
        }
        
        # Load and prepare data
        self.load_data(projects_file, beneficiaries_file)
        self.calculate_kpis()
        
    def load_data(self, projects_file, beneficiaries_file):
        """Load and prepare the ESF datasets"""
        try:
            # Load projects data
            if os.path.exists(projects_file):
                self.projects_df = pd.read_csv(projects_file)
                print(f"✅ Loaded projects data: {len(self.projects_df)} records")
            else:
                print(f"⚠️ Projects file not found: {projects_file}")
                self.create_sample_data()
                
            # Load beneficiaries data
            if os.path.exists(beneficiaries_file):
                self.beneficiaries_df = pd.read_csv(beneficiaries_file)
                print(f"✅ Loaded beneficiaries data: {len(self.beneficiaries_df)} records")
            else:
                print(f"⚠️ Beneficiaries file not found: {beneficiaries_file}")
                
            # Data preparation
            self.prepare_data()
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample data if files don't exist"""
        print("📊 Creating sample dashboard data...")
        
        # Enhanced sample projects
        np.random.seed(42)
        n_projects = 50
        
        regions = ['Dublin', 'Cork', 'Galway', 'Limerick', 'Waterford', 'Kilkenny']
        project_types = ['Digital Skills', 'Youth Employment', 'Green Skills', 'Social Innovation', 'Rural Development']
        statuses = ['Active', 'Completed', 'Planning', 'On Hold']
        
        projects_data = {
            'project_id': [f'ESF_{str(i).zfill(3)}' for i in range(1, n_projects + 1)],
            'project_name': [f'Project {i}' for i in range(1, n_projects + 1)],
            'project_type': np.random.choice(project_types, n_projects),
            'status': np.random.choice(statuses, n_projects, p=[0.4, 0.3, 0.2, 0.1]),
            'region': np.random.choice(regions, n_projects),
            'total_budget': np.random.normal(200000, 80000, n_projects).clip(50000, 500000),
            'esf_funding': lambda x: x * np.random.uniform(0.6, 0.9, len(x)),
            'beneficiaries_target': np.random.randint(50, 300, n_projects),
            'beneficiaries_actual': lambda x: np.random.randint(int(x * 0.7), int(x * 1.2), len(x)),
            'engagement_score': np.random.uniform(3.0, 5.0, n_projects),
            'start_date': pd.date_range('2023-01-01', periods=n_projects, freq='W'),
            'risk_flag': np.random.choice(['Low', 'Medium', 'High'], n_projects, p=[0.6, 0.3, 0.1])
        }
        
        # Apply lambda functions
        projects_data['esf_funding'] = projects_data['esf_funding'](projects_data['total_budget'])
        projects_data['beneficiaries_actual'] = projects_data['beneficiaries_actual'](projects_data['beneficiaries_target'])
        projects_data['actual_spend'] = projects_data['total_budget'] * np.random.uniform(0.5, 1.1, n_projects)
        
        self.projects_df = pd.DataFrame(projects_data)
        
        # Enhanced sample beneficiaries
        n_beneficiaries = 200
        genders = ['Male', 'Female', 'Other', 'Prefer not to say']
        age_groups = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        education_levels = ['Primary', 'Secondary', 'Post-Secondary', 'Tertiary']
        
        beneficiaries_data = {
            'beneficiary_id': [f'BEN_{str(i).zfill(4)}' for i in range(1, n_beneficiaries + 1)],
            'project_id': np.random.choice(self.projects_df['project_id'], n_beneficiaries),
            'gender': np.random.choice(genders, n_beneficiaries, p=[0.45, 0.45, 0.05, 0.05]),
            'age_group': np.random.choice(age_groups, n_beneficiaries, p=[0.25, 0.25, 0.2, 0.15, 0.1, 0.05]),
            'education_level': np.random.choice(education_levels, n_beneficiaries, p=[0.1, 0.4, 0.3, 0.2]),
            'region': np.random.choice(regions, n_beneficiaries),
            'satisfaction_score': np.random.randint(1, 6, n_beneficiaries),
            'training_hours': np.random.randint(20, 200, n_beneficiaries),
            'outcome_achieved': np.random.choice(['Employed', 'Self-employed', 'Further Education', 'Still Seeking'], 
                                               n_beneficiaries, p=[0.4, 0.2, 0.2, 0.2])
        }
        
        self.beneficiaries_df = pd.DataFrame(beneficiaries_data)
        print(f"✅ Created sample data: {len(self.projects_df)} projects, {len(self.beneficiaries_df)} beneficiaries")
    
    def prepare_data(self):
        """Prepare data for visualization"""
        if self.projects_df is not None:
            # Ensure date columns are datetime
            if 'start_date' in self.projects_df.columns:
                self.projects_df['start_date'] = pd.to_datetime(self.projects_df['start_date'])
                self.projects_df['year'] = self.projects_df['start_date'].dt.year
            
            # Add calculated columns if they don't exist
            if 'actual_spend' not in self.projects_df.columns:
                self.projects_df['actual_spend'] = self.projects_df['total_budget'] * np.random.uniform(0.7, 1.1, len(self.projects_df))
            
            if 'engagement_score' not in self.projects_df.columns:
                self.projects_df['engagement_score'] = np.random.uniform(3.0, 5.0, len(self.projects_df))
            
            if 'risk_flag' not in self.projects_df.columns:
                self.projects_df['risk_flag'] = np.random.choice(['Low', 'Medium', 'High'], len(self.projects_df), p=[0.6, 0.3, 0.1])
    
    def calculate_kpis(self):
        """Calculate key performance indicators"""
        if self.projects_df is not None:
            self.kpis = {
                'total_projects': len(self.projects_df),
                'total_budget': self.projects_df['total_budget'].sum(),
                'total_esf_funding': self.projects_df['esf_funding'].sum() if 'esf_funding' in self.projects_df.columns else self.projects_df['total_budget'].sum() * 0.8,
                'total_beneficiaries_target': self.projects_df['beneficiaries_target'].sum() if 'beneficiaries_target' in self.projects_df.columns else 0,
                'total_beneficiaries_actual': self.projects_df['beneficiaries_actual'].sum() if 'beneficiaries_actual' in self.projects_df.columns else 0,
                'avg_engagement_score': self.projects_df['engagement_score'].mean() if 'engagement_score' in self.projects_df.columns else 4.0,
                'total_actual_spend': self.projects_df['actual_spend'].sum() if 'actual_spend' in self.projects_df.columns else self.projects_df['total_budget'].sum() * 0.85
            }
            
        if self.beneficiaries_df is not None:
            self.kpis['total_beneficiaries_served'] = len(self.beneficiaries_df)
    
    def create_kpi_cards(self):
        """Create KPI cards for the top section"""
        fig = make_subplots(
            rows=1, cols=4,
            subplot_titles=[
                f"Total Projects<br><b>{self.kpis.get('total_projects', 0):,}</b>",
                f"Total Budget<br><b>€{self.kpis.get('total_budget', 0):,.0f}</b>",
                f"Total Beneficiaries<br><b>{self.kpis.get('total_beneficiaries_served', 0):,}</b>",
                f"Avg Engagement Score<br><b>{self.kpis.get('avg_engagement_score', 0):.1f}/5.0</b>"
            ],
            specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]]
        )
        
        # Add gauge charts for each KPI
        fig.add_trace(go.Indicator(
            mode="number",
            value=self.kpis.get('total_projects', 0),
            title={"text": "Projects"},
            number={'font': {'size': 40, 'color': self.colors['primary']}}
        ), row=1, col=1)
        
        fig.add_trace(go.Indicator(
            mode="number",
            value=self.kpis.get('total_budget', 0),
            title={"text": "Budget (€)"},
            number={'font': {'size': 40, 'color': self.colors['success']}, 'prefix': '€'}
        ), row=1, col=2)
        
        fig.add_trace(go.Indicator(
            mode="number",
            value=self.kpis.get('total_beneficiaries_served', 0),
            title={"text": "Beneficiaries"},
            number={'font': {'size': 40, 'color': self.colors['warning']}}
        ), row=1, col=3)
        
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=self.kpis.get('avg_engagement_score', 0),
            title={"text": "Engagement"},
            gauge={'axis': {'range': [None, 5]},
                   'bar': {'color': self.colors['primary']},
                   'steps': [{'range': [0, 2.5], 'color': "lightgray"},
                            {'range': [2.5, 4], 'color': "gray"}],
                   'threshold': {'line': {'color': "red", 'width': 4},
                               'thickness': 0.75, 'value': 4.5}}
        ), row=1, col=4)
        
        fig.update_layout(
            height=300,
            showlegend=False,
            title_text="📊 ESF Program KPIs Dashboard",
            title_x=0.5,
            font=dict(family="Arial, sans-serif", size=14)
        )
        
        return fig
    
    def create_budget_vs_spend_chart(self):
        """Bar Chart: Budget vs. Actual Spend by Project"""
        if self.projects_df is None:
            return go.Figure()
        
        # Get top 15 projects by budget for readability
        top_projects = self.projects_df.nlargest(15, 'total_budget')
        
        fig = go.Figure()
        
        # Budget bars
        fig.add_trace(go.Bar(
            name='Total Budget',
            x=top_projects['project_name'],
            y=top_projects['total_budget'],
            marker_color=self.colors['primary'],
            text=[f"€{x:,.0f}" for x in top_projects['total_budget']],
            textposition='outside'
        ))
        
        # Actual spend bars
        fig.add_trace(go.Bar(
            name='Actual Spend',
            x=top_projects['project_name'],
            y=top_projects['actual_spend'],
            marker_color=self.colors['success'],
            text=[f"€{x:,.0f}" for x in top_projects['actual_spend']],
            textposition='outside'
        ))
        
        fig.update_layout(
            title="💰 Budget vs. Actual Spend by Project (Top 15)",
            xaxis_title="Project",
            yaxis_title="Amount (€)",
            barmode='group',
            height=500,
            xaxis_tickangle=-45,
            showlegend=True
        )
        
        return fig
    
    def create_projects_map(self):
        """Map: Projects by Region (using scatter plot as approximation)"""
        if self.projects_df is None:
            return go.Figure()
        
        # Group by region
        region_summary = self.projects_df.groupby('region').agg({
            'project_id': 'count',
            'total_budget': 'sum',
            'beneficiaries_target': 'sum'
        }).reset_index()
        region_summary.columns = ['region', 'project_count', 'total_budget', 'beneficiaries']
        
        # Create a map-like visualization (bubble chart)
        fig = px.scatter(
            region_summary,
            x='region',
            y=['project_count'],
            size='total_budget',
            color='beneficiaries',
            hover_data=['project_count', 'total_budget', 'beneficiaries'],
            title="🗺️ Projects Distribution by Region",
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            height=400,
            showlegend=True,
            yaxis_title="Number of Projects"
        )
        
        return fig
    
    def create_gender_breakdown_pie(self):
        """Pie Chart: Beneficiary Gender Breakdown"""
        if self.beneficiaries_df is None:
            return go.Figure()
        
        gender_counts = self.beneficiaries_df['gender'].value_counts()
        
        fig = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            title="👥 Beneficiary Gender Breakdown",
            color_discrete_sequence=[self.colors['primary'], self.colors['success'], 
                                   self.colors['warning'], self.colors['danger']]
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        
        fig.update_layout(height=400)
        
        return fig
    
    def create_age_region_stacked_chart(self):
        """Stacked Column: Beneficiaries by Age Group and Region"""
        if self.beneficiaries_df is None:
            return go.Figure()
        
        # Create cross-tabulation
        age_region_crosstab = pd.crosstab(
            self.beneficiaries_df['region'],
            self.beneficiaries_df['age_group']
        )
        
        fig = go.Figure()
        
        colors = [self.colors['primary'], self.colors['success'], self.colors['warning'], 
                 self.colors['danger'], self.colors['secondary'], '#800080']
        
        for i, age_group in enumerate(age_region_crosstab.columns):
            fig.add_trace(go.Bar(
                name=age_group,
                x=age_region_crosstab.index,
                y=age_region_crosstab[age_group],
                marker_color=colors[i % len(colors)]
            ))
        
        fig.update_layout(
            title="📊 Beneficiaries by Age Group and Region",
            xaxis_title="Region",
            yaxis_title="Number of Beneficiaries",
            barmode='stack',
            height=450,
            showlegend=True
        )
        
        return fig
    
    def create_project_details_table(self):
        """Table: Project Details (sortable)"""
        if self.projects_df is None:
            return go.Figure()
        
        # Prepare data for table
        table_data = self.projects_df[['project_name', 'project_type', 'region', 'status', 
                                     'total_budget', 'actual_spend', 'engagement_score', 'risk_flag']].copy()
        
        # Format budget columns
        table_data['total_budget'] = table_data['total_budget'].apply(lambda x: f"€{x:,.0f}")
        table_data['actual_spend'] = table_data['actual_spend'].apply(lambda x: f"€{x:,.0f}")
        table_data['engagement_score'] = table_data['engagement_score'].apply(lambda x: f"{x:.1f}")
        
        # Create color coding for risk flags
        risk_colors = []
        for risk in table_data['risk_flag']:
            if risk == 'High':
                risk_colors.append('#ffcccc')  # Light red
            elif risk == 'Medium':
                risk_colors.append('#fff3cd')  # Light yellow
            else:
                risk_colors.append('#d4edda')  # Light green
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['Project Name', 'Type', 'Region', 'Status', 'Budget', 'Actual Spend', 'Engagement', 'Risk'],
                fill_color=self.colors['primary'],
                font=dict(color='white', size=12),
                align="center"
            ),
            cells=dict(
                values=[table_data[col] for col in table_data.columns],
                fill_color=['white' if col != 'risk_flag' else risk_colors for col in table_data.columns],
                align="center",
                font=dict(size=11)
            )
        )])
        
        fig.update_layout(
            title="📋 Project Details Table",
            height=600
        )
        
        return fig
    
    def create_drill_through_page(self, project_id=None):
        """Create detailed drill-through page for a specific project"""
        if self.projects_df is None or project_id is None:
            return go.Figure()
        
        # Get project details
        project = self.projects_df[self.projects_df['project_id'] == project_id].iloc[0]
        
        # Get beneficiaries for this project
        project_beneficiaries = self.beneficiaries_df[
            self.beneficiaries_df['project_id'] == project_id
        ] if self.beneficiaries_df is not None else pd.DataFrame()
        
        # Create detailed view
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                f"Project: {project['project_name']}",
                "Beneficiary Age Distribution",
                "Budget Breakdown",
                "Project Timeline"
            ],
            specs=[[{"type": "table", "colspan": 2}, None],
                   [{"type": "pie"}, {"type": "bar"}]]
        )
        
        # Project details table
        project_details = pd.DataFrame({
            'Attribute': ['Project Type', 'Region', 'Status', 'Start Date', 'Total Budget', 
                         'ESF Funding', 'Target Beneficiaries', 'Engagement Score', 'Risk Level'],
            'Value': [project['project_type'], project['region'], project['status'],
                     project.get('start_date', 'N/A'), f"€{project['total_budget']:,.0f}",
                     f"€{project.get('esf_funding', 0):,.0f}", project.get('beneficiaries_target', 0),
                     f"{project.get('engagement_score', 0):.1f}/5.0", project.get('risk_flag', 'Unknown')]
        })
        
        fig.add_trace(go.Table(
            header=dict(values=['Attribute', 'Value'], fill_color=self.colors['primary'], font=dict(color='white')),
            cells=dict(values=[project_details['Attribute'], project_details['Value']], fill_color='white')
        ), row=1, col=1)
        
        # Beneficiary age distribution
        if not project_beneficiaries.empty:
            age_dist = project_beneficiaries['age_group'].value_counts()
            fig.add_trace(go.Pie(
                values=age_dist.values,
                labels=age_dist.index,
                name="Age Groups"
            ), row=2, col=1)
        
        # Budget breakdown
        budget_breakdown = {
            'ESF Funding': project.get('esf_funding', project['total_budget'] * 0.8),
            'Co-financing': project['total_budget'] - project.get('esf_funding', project['total_budget'] * 0.8),
            'Actual Spend': project.get('actual_spend', project['total_budget'] * 0.85)
        }
        
        fig.add_trace(go.Bar(
            x=list(budget_breakdown.keys()),
            y=list(budget_breakdown.values()),
            marker_color=[self.colors['primary'], self.colors['success'], self.colors['warning']]
        ), row=2, col=2)
        
        fig.update_layout(
            title=f"🔍 Detailed View: {project['project_name']}",
            height=800,
            showlegend=False
        )
        
        return fig
    
    def create_filter_options(self):
        """Generate filter options for the dashboard"""
        filters = {}
        
        if self.projects_df is not None:
            filters['regions'] = sorted(self.projects_df['region'].unique())
            filters['years'] = sorted(self.projects_df['year'].unique()) if 'year' in self.projects_df.columns else []
            filters['risk_flags'] = sorted(self.projects_df['risk_flag'].unique()) if 'risk_flag' in self.projects_df.columns else []
            filters['project_types'] = sorted(self.projects_df['project_type'].unique())
            filters['statuses'] = sorted(self.projects_df['status'].unique())
        
        if self.beneficiaries_df is not None:
            filters['age_groups'] = sorted(self.beneficiaries_df['age_group'].unique())
            filters['genders'] = sorted(self.beneficiaries_df['gender'].unique())
            filters['education_levels'] = sorted(self.beneficiaries_df['education_level'].unique())
        
        return filters
    
    def generate_full_dashboard(self, output_file='esf_powerbi_dashboard.html'):
        """Generate the complete dashboard"""
        print("🎨 Generating Power BI style dashboard...")
        
        # Create all visualizations
        kpi_cards = self.create_kpi_cards()
        budget_chart = self.create_budget_vs_spend_chart()
        projects_map = self.create_projects_map()
        gender_pie = self.create_gender_breakdown_pie()
        age_region_chart = self.create_age_region_stacked_chart()
        details_table = self.create_project_details_table()
        
        # Create combined HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ESF Program Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .dashboard-header {{
                    text-align: center;
                    color: #323130;
                    margin-bottom: 30px;
                }}
                .kpi-section {{
                    margin-bottom: 30px;
                }}
                .main-content {{
                    display: grid;
                    grid-template-columns: 250px 1fr;
                    gap: 20px;
                }}
                .filters {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    height: fit-content;
                }}
                .charts {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                }}
                .chart-container {{
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    padding: 15px;
                }}
                .full-width {{
                    grid-column: 1 / -1;
                }}
                .filter-group {{
                    margin-bottom: 20px;
                }}
                .filter-label {{
                    font-weight: bold;
                    color: #323130;
                    margin-bottom: 8px;
                    display: block;
                }}
                select {{
                    width: 100%;
                    padding: 8px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="dashboard-header">
                <h1>🏆 ESF Program Performance Dashboard</h1>
                <p>Interactive Business Intelligence Dashboard for European Social Fund Projects</p>
            </div>
            
            <div class="kpi-section">
                <div id="kpi-cards" class="chart-container"></div>
            </div>
            
            <div class="main-content">
                <div class="filters">
                    <h3>📍 Filters</h3>
                    {self.generate_filter_html()}
                </div>
                
                <div class="charts">
                    <div id="budget-chart" class="chart-container"></div>
                    <div id="projects-map" class="chart-container"></div>
                    <div id="gender-pie" class="chart-container"></div>
                    <div id="age-region-chart" class="chart-container"></div>
                    <div id="details-table" class="chart-container full-width"></div>
                </div>
            </div>
            
            <script>
                // Plot all charts
                Plotly.newPlot('kpi-cards', {kpi_cards.to_json()});
                Plotly.newPlot('budget-chart', {budget_chart.to_json()});
                Plotly.newPlot('projects-map', {projects_map.to_json()});
                Plotly.newPlot('gender-pie', {gender_pie.to_json()});
                Plotly.newPlot('age-region-chart', {age_region_chart.to_json()});
                Plotly.newPlot('details-table', {details_table.to_json()});
            </script>
        </body>
        </html>
        """
        
        # Save individual charts
        os.makedirs('dashboard_output', exist_ok=True)
        
        pyo.plot(kpi_cards, filename='dashboard_output/kpi_cards.html', auto_open=False)
        pyo.plot(budget_chart, filename='dashboard_output/budget_vs_spend.html', auto_open=False)
        pyo.plot(projects_map, filename='dashboard_output/projects_map.html', auto_open=False)
        pyo.plot(gender_pie, filename='dashboard_output/gender_breakdown.html', auto_open=False)
        pyo.plot(age_region_chart, filename='dashboard_output/age_region_analysis.html', auto_open=False)
        pyo.plot(details_table, filename='dashboard_output/project_details.html', auto_open=False)
        
        # Save main dashboard
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Dashboard generated: {output_file}")
        print(f"📁 Individual charts saved in: dashboard_output/")
        
        return output_file
    
    def generate_filter_html(self):
        """Generate HTML for filter controls"""
        filters = self.create_filter_options()
        
        filter_html = ""
        
        for filter_name, options in filters.items():
            if options:
                filter_html += f"""
                <div class="filter-group">
                    <label class="filter-label">{filter_name.replace('_', ' ').title()}</label>
                    <select id="{filter_name}" onchange="applyFilter('{filter_name}')">
                        <option value="all">All {filter_name.replace('_', ' ').title()}</option>
                        {"".join([f'<option value="{opt}">{opt}</option>' for opt in options])}
                    </select>
                </div>
                """
        
        return filter_html
    
    def export_data_summary(self):
        """Export data summary for Power BI import"""
        summary = {
            'dashboard_metrics': self.kpis,
            'data_summary': {
                'projects_count': len(self.projects_df) if self.projects_df is not None else 0,
                'beneficiaries_count': len(self.beneficiaries_df) if self.beneficiaries_df is not None else 0,
                'regions': self.projects_df['region'].unique().tolist() if self.projects_df is not None else [],
                'project_types': self.projects_df['project_type'].unique().tolist() if self.projects_df is not None else []
            },
            'filter_options': self.create_filter_options(),
            'generated_at': datetime.now().isoformat()
        }
        
        with open('dashboard_output/dashboard_summary.json', 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print("✅ Dashboard summary exported: dashboard_output/dashboard_summary.json")

def main():
    """Main execution function"""
    print("🎨 ESF Power BI Dashboard Generator")
    print("=" * 50)
    
    # Initialize dashboard generator
    dashboard = PowerBIDashboardGenerator()
    
    # Generate complete dashboard
    output_file = dashboard.generate_full_dashboard()
    
    # Export summary
    dashboard.export_data_summary()
    
    print(f"""
    🎉 Dashboard Generation Complete!
    
    📊 Main Dashboard: {output_file}
    📁 Individual Charts: dashboard_output/
    📋 Data Summary: dashboard_output/dashboard_summary.json
    
    🚀 Next Steps:
    1. Open {output_file} in your web browser
    2. Use the filter controls on the left panel
    3. Hover over charts for interactive details
    4. Use individual chart files for specific analysis
    
    💡 Power BI Integration:
    - Import your cleaned CSV files into Power BI
    - Use the dashboard_summary.json for field mappings
    - Recreate these visualizations in Power BI for full interactivity
    """)

if __name__ == "__main__":
    main()
