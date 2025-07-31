# 📊 Power BI DAX Measures Reference
## ESF Program Dashboard

### 🏦 Financial Measures

#### Basic Financial KPIs
```dax
Total Budget = SUM(esf_projects[total_budget])

Total Spend = SUM(esf_projects[actual_spend])

Budget Variance = [Total Budget] - [Total Spend]

Budget Utilization % = 
DIVIDE([Total Spend], [Total Budget], 0) * 100

ESF Funding Total = SUM(esf_projects[esf_funding])

ESF Funding Rate % = 
DIVIDE([ESF Funding Total], [Total Budget], 0) * 100
```

#### Cost Efficiency Measures
```dax
Cost Per Beneficiary = 
DIVIDE([Total Budget], [Total Beneficiaries Actual], 0)

ESF Cost Per Beneficiary = 
DIVIDE([ESF Funding Total], [Total Beneficiaries Actual], 0)

Cost Per Training Hour = 
DIVIDE([Total Budget], [Total Training Hours], 0)

Average Project Budget = 
AVERAGE(esf_projects[total_budget])

Budget Per Region = 
CALCULATE([Total Budget], ALLEXCEPT(esf_projects, esf_projects[region]))
```

### 🎯 Performance Measures

#### Target Achievement
```dax
Total Beneficiaries Target = SUM(esf_projects[beneficiaries_target])

Total Beneficiaries Actual = SUM(esf_projects[beneficiaries_actual])

Target Achievement Rate % = 
DIVIDE([Total Beneficiaries Actual], [Total Beneficiaries Target], 0) * 100

Projects Over Target = 
CALCULATE(
    COUNT(esf_projects[project_id]),
    esf_projects[target_achievement_rate] > 100
)

Projects Under Target = 
CALCULATE(
    COUNT(esf_projects[project_id]),
    esf_projects[target_achievement_rate] < 100
)

Over Target Rate % = 
DIVIDE([Projects Over Target], [Total Projects], 0) * 100
```

#### Engagement and Quality
```dax
Average Engagement = AVERAGE(esf_projects[engagement_score])

High Engagement Projects = 
CALCULATE(
    COUNT(esf_projects[project_id]),
    esf_projects[engagement_score] >= 4
)

Low Engagement Projects = 
CALCULATE(
    COUNT(esf_projects[project_id]),
    esf_projects[engagement_score] < 3
)

Engagement Excellence Rate % = 
DIVIDE([High Engagement Projects], [Total Projects], 0) * 100
```

### 👥 Beneficiary Measures

#### Basic Beneficiary KPIs
```dax
Total Beneficiaries = COUNT(esf_beneficiaries[beneficiary_id])

Male Beneficiaries = 
CALCULATE(
    COUNT(esf_beneficiaries[beneficiary_id]),
    esf_beneficiaries[gender] = "Male"
)

Female Beneficiaries = 
CALCULATE(
    COUNT(esf_beneficiaries[beneficiary_id]),
    esf_beneficiaries[gender] = "Female"
)

Gender Diversity % = 
MIN(
    DIVIDE([Male Beneficiaries], [Total Beneficiaries], 0),
    DIVIDE([Female Beneficiaries], [Total Beneficiaries], 0)
) * 100
```

#### Training and Development
```dax
Total Training Hours = SUM(esf_beneficiaries[training_hours])

Average Training Hours = AVERAGE(esf_beneficiaries[training_hours])

Training Hours Per Project = 
DIVIDE([Total Training Hours], [Total Projects], 0)

Intensive Training Beneficiaries = 
CALCULATE(
    COUNT(esf_beneficiaries[beneficiary_id]),
    esf_beneficiaries[training_hours] > 100
)

Training Completion Rate % = 
DIVIDE(
    CALCULATE(
        COUNT(esf_beneficiaries[beneficiary_id]),
        esf_beneficiaries[training_hours] > 0
    ),
    [Total Beneficiaries],
    0
) * 100
```

#### Employment Outcomes
```dax
Employment Success Rate % = 
DIVIDE(
    CALCULATE(
        COUNT(esf_beneficiaries[beneficiary_id]),
        esf_beneficiaries[outcome_achieved] IN {"Employed", "Self-employed"}
    ),
    [Total Beneficiaries],
    0
) * 100

Employed Beneficiaries = 
CALCULATE(
    COUNT(esf_beneficiaries[beneficiary_id]),
    esf_beneficiaries[outcome_achieved] = "Employed"
)

Self-Employed Beneficiaries = 
CALCULATE(
    COUNT(esf_beneficiaries[beneficiary_id]),
    esf_beneficiaries[outcome_achieved] = "Self-employed"
)

Further Education Beneficiaries = 
CALCULATE(
    COUNT(esf_beneficiaries[beneficiary_id]),
    esf_beneficiaries[outcome_achieved] = "Further Education"
)

Employment Conversion Rate % = 
DIVIDE(
    CALCULATE(
        COUNT(esf_beneficiaries[beneficiary_id]),
        esf_beneficiaries[employment_status_before] = "Unemployed" &&
        esf_beneficiaries[outcome_achieved] IN {"Employed", "Self-employed"}
    ),
    CALCULATE(
        COUNT(esf_beneficiaries[beneficiary_id]),
        esf_beneficiaries[employment_status_before] = "Unemployed"
    ),
    0
) * 100
```

#### Satisfaction and Quality
```dax
Average Satisfaction = AVERAGE(esf_beneficiaries[satisfaction_score])

High Satisfaction Rate % = 
DIVIDE(
    CALCULATE(
        COUNT(esf_beneficiaries[beneficiary_id]),
        esf_beneficiaries[satisfaction_score] >= 4
    ),
    [Total Beneficiaries],
    0
) * 100

Low Satisfaction Rate % = 
DIVIDE(
    CALCULATE(
        COUNT(esf_beneficiaries[beneficiary_id]),
        esf_beneficiaries[satisfaction_score] <= 2
    ),
    [Total Beneficiaries],
    0
) * 100

Satisfaction Score Distribution = 
CALCULATE(
    COUNT(esf_beneficiaries[beneficiary_id]),
    esf_beneficiaries[satisfaction_score] = SELECTEDVALUE(esf_beneficiaries[satisfaction_score])
)
```

### 📈 Project Status Measures

#### Project Counting
```dax
Total Projects = COUNT(esf_projects[project_id])

Active Projects = 
CALCULATE(
    COUNT(esf_projects[project_id]),
    esf_projects[status] = "Active"
)

Completed Projects = 
CALCULATE(
    COUNT(esf_projects[project_id]),
    esf_projects[status] = "Completed"
)

Planning Projects = 
CALCULATE(
    COUNT(esf_projects[project_id]),
    esf_projects[status] = "Planning"
)

On Hold Projects = 
CALCULATE(
    COUNT(esf_projects[project_id]),
    esf_projects[status] = "On Hold"
)
```

#### Project Performance Rates
```dax
Completion Rate % = 
DIVIDE([Completed Projects], [Total Projects], 0) * 100

Active Rate % = 
DIVIDE([Active Projects], [Total Projects], 0) * 100

Project Success Rate % = 
DIVIDE(
    [Completed Projects] + [Projects Over Target],
    [Total Projects],
    0
) * 100
```

### ⚠️ Risk Management Measures

#### Risk Assessment
```dax
High Risk Projects = 
CALCULATE(
    COUNT(esf_projects[project_id]),
    esf_projects[risk_flag] = "High"
)

Medium Risk Projects = 
CALCULATE(
    COUNT(esf_projects[project_id]),
    esf_projects[risk_flag] = "Medium"
)

Low Risk Projects = 
CALCULATE(
    COUNT(esf_projects[project_id]),
    esf_projects[risk_flag] = "Low"
)

Projects at Risk = 
CALCULATE(
    COUNT(esf_projects[project_id]),
    esf_projects[risk_flag] IN {"High", "Medium"}
)

Risk Score = 
SWITCH(
    TRUE(),
    [High Risk Projects] > 0, 3,
    [Medium Risk Projects] > 0, 2,
    1
)
```

### 📅 Time Intelligence Measures

#### Year-to-Date Calculations
```dax
Budget YTD = 
TOTALYTD([Total Budget], esf_projects[start_date])

Beneficiaries YTD = 
TOTALYTD([Total Beneficiaries], esf_beneficiaries[participation_start])

Training Hours YTD = 
TOTALYTD([Total Training Hours], esf_beneficiaries[participation_start])
```

#### Previous Period Comparisons
```dax
Previous Year Budget = 
CALCULATE(
    [Total Budget],
    SAMEPERIODLASTYEAR(esf_projects[start_date])
)

Budget Growth % = 
DIVIDE(
    [Total Budget] - [Previous Year Budget],
    [Previous Year Budget],
    0
) * 100

Previous Quarter Beneficiaries = 
CALCULATE(
    [Total Beneficiaries],
    PREVIOUSQUARTER(esf_beneficiaries[participation_start])
)

Beneficiary Growth % = 
DIVIDE(
    [Total Beneficiaries] - [Previous Quarter Beneficiaries],
    [Previous Quarter Beneficiaries],
    0
) * 100
```

### 🌍 Regional Analysis Measures

#### Regional Performance
```dax
Regional Budget Share % = 
DIVIDE(
    CALCULATE([Total Budget], ALLEXCEPT(esf_projects, esf_projects[region])),
    CALCULATE([Total Budget], ALL(esf_projects[region])),
    0
) * 100

Regional Beneficiary Density = 
DIVIDE(
    CALCULATE([Total Beneficiaries], ALLEXCEPT(esf_beneficiaries, esf_beneficiaries[region])),
    CALCULATE([Total Projects], ALLEXCEPT(esf_projects, esf_projects[region])),
    0
)

Top Performing Region = 
TOPN(
    1,
    VALUES(esf_projects[region]),
    [Target Achievement Rate %],
    DESC
)
```

### 📊 Ranking and Top N Measures

#### Performance Rankings
```dax
Project Type Ranking = 
RANKX(
    ALL(esf_projects[project_type]),
    [Target Achievement Rate %],
    ,
    DESC
)

Top 5 Projects by Budget = 
TOPN(
    5,
    VALUES(esf_projects[project_name]),
    [Total Budget],
    DESC
)

Bottom 5 Projects by Engagement = 
TOPN(
    5,
    VALUES(esf_projects[project_name]),
    [Average Engagement],
    ASC
)
```

## 💡 Usage Tips

### 1. Creating Measures in Power BI
1. Go to **Modeling** tab
2. Click **New Measure**
3. Copy and paste the DAX code
4. Rename the measure appropriately

### 2. Using Measures in Visuals
- Drag measures to **Values** field
- Use in KPI cards for key metrics
- Combine with dimensions for analysis

### 3. Error Handling
- Always use `DIVIDE()` instead of `/` to handle division by zero
- Use `ISBLANK()` to check for empty values
- Add `0` as default value in DIVIDE function

### 4. Performance Optimization
- Use `CALCULATE()` for filtered calculations
- Prefer `SUM()` over `SUMX()` when possible
- Create base measures and reference them in complex calculations

This comprehensive set of DAX measures will power your ESF dashboard with professional-grade analytics and insights! 🚀
