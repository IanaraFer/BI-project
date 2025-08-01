# DAX MEASURES REFERENCE FOR ESF BUSINESS INTELLIGENCE
# =====================================================
# 
# This file contains comprehensive DAX measures for analyzing ESF (European Social Fund)
# projects and beneficiaries data in Power BI. Copy and paste these measures into your
# Power BI report to enable advanced analytics and KPI calculations.
#
# Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Compatible with: Power BI Desktop, Power BI Service
# Data Model: ESF Projects & Beneficiaries

## TABLE OF CONTENTS
# 1. PROJECT MEASURES
# 2. BUDGET & FINANCIAL MEASURES  
# 3. PERFORMANCE MEASURES
# 4. BENEFICIARY MEASURES
# 5. TIME INTELLIGENCE MEASURES
# 6. COMPARATIVE MEASURES
# 7. ADVANCED ANALYTICS MEASURES

# =============================================================================
# 1. PROJECT MEASURES
# =============================================================================

## Total Projects
Total Projects = COUNTROWS(Projects)

## Active Projects
Active Projects = 
CALCULATE(
    COUNTROWS(Projects),
    Projects[Status] = "Active"
)

## Completed Projects
Completed Projects = 
CALCULATE(
    COUNTROWS(Projects),
    Projects[Status] = "Completed"
)

## Project Success Rate
Project Success Rate = 
DIVIDE(
    CALCULATE(
        COUNTROWS(Projects),
        Projects[Target Achievement Rate] >= 100
    ),
    COUNTROWS(Projects),
    0
)

## Average Project Duration (Days)
Avg Project Duration = 
AVERAGEX(
    Projects,
    DATEDIFF(Projects[Start Date], Projects[End Date], DAY)
)

## Projects Over Budget
Projects Over Budget = 
CALCULATE(
    COUNTROWS(Projects),
    Projects[Actual Cost] > Projects[Total Budget]
)

# =============================================================================
# 2. BUDGET & FINANCIAL MEASURES
# =============================================================================

## Total Budget
Total Budget = SUM(Projects[Total Budget])

## Total ESF Funding
Total ESF Funding = SUM(Projects[ESF Funding])

## ESF Funding Rate
ESF Funding Rate = 
DIVIDE(
    [Total ESF Funding],
    [Total Budget],
    0
) * 100

## Average Project Budget
Avg Project Budget = 
AVERAGE(Projects[Total Budget])

## Budget Utilization Rate
Budget Utilization Rate = 
DIVIDE(
    SUM(Projects[Actual Cost]),
    SUM(Projects[Total Budget]),
    0
) * 100

## Cost Per Beneficiary
Cost Per Beneficiary = 
DIVIDE(
    [Total Budget],
    [Total Beneficiaries],
    0
)

## ROI (Return on Investment)
ROI = 
DIVIDE(
    SUM(Projects[Economic Impact]) - SUM(Projects[Total Budget]),
    SUM(Projects[Total Budget]),
    0
) * 100

# =============================================================================
# 3. PERFORMANCE MEASURES
# =============================================================================

## Average Target Achievement Rate
Avg Target Achievement = 
AVERAGE(Projects[Target Achievement Rate])

## Performance Rating
Performance Rating = 
SWITCH(
    TRUE(),
    [Avg Target Achievement] >= 120, "Excellent",
    [Avg Target Achievement] >= 100, "Good", 
    [Avg Target Achievement] >= 80, "Fair",
    "Poor"
)

## Projects Meeting Targets
Projects Meeting Targets = 
CALCULATE(
    COUNTROWS(Projects),
    Projects[Target Achievement Rate] >= 100
)

## High Performing Projects (>120% target)
High Performing Projects = 
CALCULATE(
    COUNTROWS(Projects),
    Projects[Target Achievement Rate] > 120
)

## Efficiency Score (Achievement per Euro)
Efficiency Score = 
DIVIDE(
    [Avg Target Achievement],
    [Avg Project Budget] / 1000000,
    0
)

## Quality Index
Quality Index = 
(
    [Project Success Rate] * 0.4 +
    ([Avg Target Achievement] / 100) * 0.3 +
    ([Budget Utilization Rate] / 100) * 0.3
) * 100

# =============================================================================
# 4. BENEFICIARY MEASURES
# =============================================================================

## Total Beneficiaries
Total Beneficiaries = COUNTROWS(Beneficiaries)

## Employment Success Rate
Employment Success Rate = 
DIVIDE(
    CALCULATE(
        COUNTROWS(Beneficiaries),
        Beneficiaries[Outcome Achieved] IN {"Employed", "Self-employed"}
    ),
    COUNTROWS(Beneficiaries),
    0
) * 100

## Average Training Hours
Avg Training Hours = 
AVERAGE(Beneficiaries[Training Hours])

## Total Training Hours Delivered
Total Training Hours = 
SUM(Beneficiaries[Training Hours])

## Average Satisfaction Score
Avg Satisfaction Score = 
AVERAGE(Beneficiaries[Satisfaction Score])

## High Satisfaction Rate (Score >= 8)
High Satisfaction Rate = 
DIVIDE(
    CALCULATE(
        COUNTROWS(Beneficiaries),
        Beneficiaries[Satisfaction Score] >= 8
    ),
    COUNTROWS(Beneficiaries),
    0
) * 100

## Gender Diversity Index
Gender Diversity Index = 
VAR FemaleCount = 
    CALCULATE(
        COUNTROWS(Beneficiaries),
        Beneficiaries[Gender] = "Female"
    )
VAR MaleCount = 
    CALCULATE(
        COUNTROWS(Beneficiaries),
        Beneficiaries[Gender] = "Male"
    )
VAR TotalCount = [Total Beneficiaries]
RETURN
    1 - ABS(FemaleCount - MaleCount) / TotalCount

## Training Efficiency
Training Efficiency = 
DIVIDE(
    [Employment Success Rate],
    [Avg Training Hours] / 100,
    0
)

# =============================================================================
# 5. TIME INTELLIGENCE MEASURES
# =============================================================================

## Projects Started This Year
Projects Started This Year = 
CALCULATE(
    COUNTROWS(Projects),
    YEAR(Projects[Start Date]) = YEAR(TODAY())
)

## Projects Completed This Year
Projects Completed This Year = 
CALCULATE(
    COUNTROWS(Projects),
    Projects[Status] = "Completed",
    YEAR(Projects[End Date]) = YEAR(TODAY())
)

## YTD Budget
YTD Budget = 
CALCULATE(
    [Total Budget],
    DATESYTD('Calendar'[Date])
)

## Previous Year Budget
PY Budget = 
CALCULATE(
    [Total Budget],
    SAMEPERIODLASTYEAR('Calendar'[Date])
)

## Budget Growth
Budget Growth = 
DIVIDE(
    [YTD Budget] - [PY Budget],
    [PY Budget],
    0
) * 100

## Monthly Project Starts
Monthly Project Starts = 
CALCULATE(
    COUNTROWS(Projects),
    MONTH(Projects[Start Date]) = MONTH(TODAY()),
    YEAR(Projects[Start Date]) = YEAR(TODAY())
)

## Quarterly Performance Trend
Quarterly Performance = 
CALCULATE(
    [Avg Target Achievement],
    DATESQTD('Calendar'[Date])
)

# =============================================================================
# 6. COMPARATIVE MEASURES
# =============================================================================

## Regional Performance Rank
Regional Performance Rank = 
RANKX(
    ALLSELECTED(Projects[Region]),
    [Avg Target Achievement],
    ,
    DESC
)

## Best Performing Region
Best Performing Region = 
CALCULATE(
    SELECTEDVALUE(Projects[Region]),
    TOPN(1, ALLSELECTED(Projects[Region]), [Avg Target Achievement])
)

## Budget vs Target Variance
Budget Variance = 
([Total Budget] - [YTD Budget]) / [Total Budget] * 100

## Performance vs Industry Benchmark
Performance vs Benchmark = 
[Avg Target Achievement] - 95  // Assuming 95% is industry benchmark

## Regional Budget Share
Regional Budget Share = 
DIVIDE(
    [Total Budget],
    CALCULATE([Total Budget], ALLSELECTED(Projects[Region])),
    0
) * 100

## Project Type Performance Comparison
Project Type Performance = 
RANKX(
    ALLSELECTED(Projects[Project Type]),
    [Project Success Rate],
    ,
    DESC
)

# =============================================================================
# 7. ADVANCED ANALYTICS MEASURES
# =============================================================================

## Predictive Success Score
Predictive Success Score = 
VAR BudgetScore = 
    SWITCH(
        TRUE(),
        [Avg Project Budget] > 5000000, 0.2,
        [Avg Project Budget] > 2000000, 0.6,
        [Avg Project Budget] > 1000000, 0.8,
        1.0
    )
VAR RegionScore = 
    SWITCH(
        SELECTEDVALUE(Projects[Region]),
        "North", 0.9,
        "South", 0.8,
        "East", 0.7,
        "West", 0.85,
        "Central", 0.75,
        0.5
    )
VAR TypeScore = 
    SWITCH(
        SELECTEDVALUE(Projects[Project Type]),
        "Skills Development", 0.9,
        "Employment Support", 0.8,
        "Innovation", 0.7,
        "Social Inclusion", 0.75,
        0.6
    )
RETURN (BudgetScore * 0.3 + RegionScore * 0.4 + TypeScore * 0.3) * 100

## Risk Assessment Score
Risk Score = 
VAR BudgetRisk = IF([Budget Utilization Rate] > 95, 30, 0)
VAR TimeRisk = IF([Avg Project Duration] > 730, 25, 0)  // 2 years
VAR PerformanceRisk = IF([Avg Target Achievement] < 80, 45, 0)
RETURN BudgetRisk + TimeRisk + PerformanceRisk

## Anomaly Detection Score
Anomaly Score = 
VAR CurrentPerformance = [Avg Target Achievement]
VAR HistoricalAvg = 
    CALCULATE(
        [Avg Target Achievement],
        DATESBETWEEN(
            'Calendar'[Date],
            DATE(YEAR(TODAY())-2, 1, 1),
            DATE(YEAR(TODAY())-1, 12, 31)
        )
    )
VAR Deviation = ABS(CurrentPerformance - HistoricalAvg)
RETURN 
    SWITCH(
        TRUE(),
        Deviation > 30, "High",
        Deviation > 15, "Medium", 
        "Low"
    )

## Clustering Score (Project Similarity)
Clustering Score = 
VAR CurrentBudget = SELECTEDVALUE(Projects[Total Budget])
VAR CurrentDuration = SELECTEDVALUE(Projects[Project Duration])
VAR SimilarProjects = 
    CALCULATE(
        COUNTROWS(Projects),
        Projects[Total Budget] >= CurrentBudget * 0.8,
        Projects[Total Budget] <= CurrentBudget * 1.2,
        Projects[Project Duration] >= CurrentDuration * 0.8,
        Projects[Project Duration] <= CurrentDuration * 1.2
    )
RETURN SimilarProjects

## Optimization Potential
Optimization Potential = 
VAR CurrentEfficiency = [Efficiency Score]
VAR MaxEfficiency = 
    CALCULATE(
        MAX(Projects[Target Achievement Rate]) / (MAX(Projects[Total Budget]) / 1000000),
        ALLSELECTED(Projects[Project Type])
    )
RETURN (MaxEfficiency - CurrentEfficiency) / MaxEfficiency * 100

# =============================================================================
# CONDITIONAL FORMATTING MEASURES
# =============================================================================

## Traffic Light - Performance
Performance Traffic Light = 
SWITCH(
    TRUE(),
    [Avg Target Achievement] >= 100, "Green",
    [Avg Target Achievement] >= 80, "Yellow",
    "Red"
)

## Traffic Light - Budget
Budget Traffic Light = 
SWITCH(
    TRUE(),
    [Budget Utilization Rate] <= 100, "Green",
    [Budget Utilization Rate] <= 110, "Yellow",
    "Red"
)

## Arrow Direction - Trend
Performance Trend = 
VAR CurrentQuarter = [Avg Target Achievement]
VAR PreviousQuarter = 
    CALCULATE(
        [Avg Target Achievement],
        DATEADD('Calendar'[Date], -3, MONTH)
    )
RETURN 
    SWITCH(
        TRUE(),
        CurrentQuarter > PreviousQuarter * 1.05, "↗",
        CurrentQuarter < PreviousQuarter * 0.95, "↘",
        "→"
    )

# =============================================================================
# USAGE INSTRUCTIONS
# =============================================================================

/*
HOW TO USE THESE MEASURES:

1. IMPORTING TO POWER BI:
   - Copy each measure individually
   - In Power BI Desktop, go to "Modeling" tab
   - Click "New Measure"
   - Paste the DAX code
   - Press Enter to create the measure

2. MEASURE DEPENDENCIES:
   - Ensure your data model has tables named "Projects" and "Beneficiaries"
   - Column names should match those referenced in the measures
   - Create a Calendar table for time intelligence measures

3. RECOMMENDED VISUALIZATIONS:
   - KPI Cards: Total Projects, Total Budget, Success Rate
   - Gauge Charts: Performance vs targets
   - Bar Charts: Regional comparisons
   - Line Charts: Trend analysis over time
   - Scatter Plots: Budget vs Performance analysis

4. CUSTOMIZATION:
   - Adjust benchmarks and thresholds as needed
   - Modify color coding in traffic light measures
   - Add additional business rules specific to your organization

5. PERFORMANCE OPTIMIZATION:
   - Use SELECTEDVALUE() instead of VALUES() where possible
   - Consider using variables for complex calculations
   - Test measure performance with large datasets

For support and additional measures, refer to the ESF BI project documentation.
*/
