# Delhi Electricity Load Forecasting — Case Study

## Project Overview

This case study explores the relationship between **electricity load** and **weather conditions** in Delhi. Understanding how weather influences electricity consumption is essential for efficient energy management, planning, and forecasting.

Delhi experiences a wide range of weather conditions throughout the year, making it an ideal case study for analyzing the impact of temperature on electricity load. The dataset includes detailed information on hourly electricity load, temperature, and other weather parameters provided by the Delhi Electricity Board.

## Objectives

- Analyze seasonal patterns of electricity consumption at multiple timescales (daily, weekly, monthly, yearly)
- Identify peak and off-peak hours across different seasons
- Discover consistent patterns across days of the week and months
- Correlate temperature variations with electricity load
- Assess holiday effects on load demand
- Provide actionable insights for energy management and infrastructure planning

## Dataset

- **Electricity Load:** Hourly load data for Delhi
- **Weather Data:** Temperature and related weather parameters
- **Archive Data:** Historical records for trend analysis
- **Source:** Delhi Electricity Board

## Tools Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Repository Structure

```
C:\Users\AB\hermes-work\data_projects\20251122_DelhiElectricityLoad_CaseStudy + GitHub
┣ 📓 20251122_DelhiElectricityLoad_CaseStudy.ipynb   ← Main analysis notebook
┣ 📊 archive_data.csv                                 ← Historical load data
┣ 📊 delhi_weather_data.csv                           ← Weather data
┣ 📦 daily_load_data.zip                              ← Daily load archive
┣ 📦 #extras.zip                                      ← Additional resources
┗ 📄 README.md                                        ← Project documentation
```

## Key Questions Addressed

1. How do electricity load patterns vary within a day, week, month, and across years?
2. What are the peak and off-peak hours for different seasons?
3. Are there consistent patterns across days of the week and months?
4. How does temperature variation affect electricity load?
5. How do holidays affect load demand?

## How to Run

1. Clone the repository
2. Install dependencies: `pip install pandas numpy matplotlib seaborn`
3. Open `20251122_DelhiElectricityLoad_CaseStudy.ipynb` in Jupyter

## Live App

- **Delhi Electricity Load Dashboard:** https://delhi-electricity-load-dash.streamlit.app/

## About

This case study was completed as part of a data analytics learning path, focusing on time series analysis and energy demand forecasting.
