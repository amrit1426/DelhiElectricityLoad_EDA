import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page config
st.set_page_config(
    page_title="Delhi Electricity Load",
    page_icon="⚡",
    layout="wide",
)

# Header
st.title("⚡ Delhi Electricity Load vs Weather")
st.markdown("Time series analysis of electricity demand and temperature.")

# Load and preprocess data
@st.cache_data
def load_data():
    # Load archive load data
    load = pd.read_csv("archive_data.csv")
    load.columns = ["Load", "timestamp"]
    load["timestamp"] = pd.to_datetime(load["timestamp"])
    load = load.sort_values("timestamp").reset_index(drop=True)
    
    # Resample to hourly by averaging 15-min intervals
    load = load.set_index("timestamp").resample("h").mean().reset_index()
    
    # Load weather data
    weather = pd.read_csv("delhi_weather_data.csv")
    weather.columns = ["timestamp", "temp", "rhum", "wspd"]
    weather["timestamp"] = pd.to_datetime(weather["timestamp"])
    weather = weather.sort_values("timestamp").reset_index(drop=True)
    
    # Merge on timestamp
    df = pd.merge(load, weather, on="timestamp", how="inner")
    
    # Replace 0 load with NaN and forward fill
    df["Load"] = df["Load"].replace(0, np.nan).ffill()
    
    # Extract time features
    df["hour"] = df["timestamp"].dt.hour
    df["week"] = df["timestamp"].dt.dayofweek
    df["month"] = df["timestamp"].dt.month
    df["year"] = df["timestamp"].dt.year
    
    # Season mapping
    summer = [6, 7, 8]
    autumn = [9, 10, 11]
    winter = [12, 1, 2]
    spring = [3, 4, 5]
    df.loc[df["month"].isin(summer), "season"] = "Summer"
    df.loc[df["month"].isin(autumn), "season"] = "Autumn"
    df.loc[df["month"].isin(winter), "season"] = "Winter"
    df.loc[df["month"].isin(spring), "season"] = "Spring"
    
    # Daily averages for trend plots
    daily = df.resample("D", on="timestamp").mean(numeric_only=True).reset_index()
    daily["month"] = daily["timestamp"].dt.month
    daily.loc[daily["month"].isin(summer), "season"] = "Summer"
    daily.loc[daily["month"].isin(autumn), "season"] = "Autumn"
    daily.loc[daily["month"].isin(winter), "season"] = "Winter"
    daily.loc[daily["month"].isin(spring), "season"] = "Spring"
    
    return df, daily

df, daily_data = load_data()

# Chart styling helper
def style_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#f8fafc",
        xaxis_gridcolor="#1e293b",
        yaxis_gridcolor="#1e293b",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    seasons = st.multiselect(
        "Season",
        options=sorted(df["season"].dropna().unique()),
        default=sorted(df["season"].dropna().unique()),
    )
    years = st.multiselect(
        "Year",
        options=sorted(df["year"].dropna().unique()),
        default=sorted(df["year"].dropna().unique()),
    )

filtered = df[df["season"].isin(seasons) & df["year"].isin(years)]
filtered_daily = daily_data[daily_data["season"].isin(seasons) & daily_data["timestamp"].dt.year.isin(years)]

# Tabs
tab_overview, tab_analysis, tab_details = st.tabs(["Overview", "Analysis", "Details"])

with tab_overview:
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", len(filtered))
    col2.metric(
        "Avg Load (MW)",
        f"{filtered['Load'].mean():.0f}" if len(filtered) else "N/A",
    )
    col3.metric(
        "Peak Load (MW)",
        f"{filtered['Load'].max():.0f}" if len(filtered) else "N/A",
    )
    col4.metric(
        "Avg Temp (°C)",
        f"{filtered['temp'].mean():.1f}" if len(filtered) else "N/A",
    )

    st.subheader("Monthly Load Trend by Year")
    if len(filtered_daily):
        monthly_trend = (
            filtered_daily.assign(
                year=filtered_daily["timestamp"].dt.year,
                month=filtered_daily["timestamp"].dt.month,
            )
            .groupby(["year", "month"], as_index=False)["Load"]
            .mean()
        )
        fig = px.line(
            monthly_trend,
            x="month",
            y="Load",
            color="year",
            title="Monthly Electricity Load Demand by Year",
            markers=True,
            category_orders={"month": list(range(1, 13))},
        )
        fig.update_layout(xaxis_tickmode="linear", xaxis_tick0=1, xaxis_dtick=1)
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Daily Temperature Trend")
    if len(filtered_daily):
        fig = px.line(
            filtered_daily,
            x="timestamp",
            y="temp",
            title="Daily Temperature Trend",
        )
        fig.update_traces(line_color="#fbbf24")
        st.plotly_chart(style_chart(fig), width="stretch")

with tab_analysis:
    st.subheader("Average Hourly Load Pattern")
    if len(filtered):
        hourly = filtered.groupby("hour")["Load"].mean().reset_index()
        fig = px.line(
            hourly,
            x="hour",
            y="Load",
            title="Average Hourly Electricity Load",
            markers=True,
        )
        fig.update_traces(line_color="#f59e0b")
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Average Weekly Load Pattern")
    if len(filtered):
        weekly = filtered.groupby("week")["Load"].mean().reset_index()
        fig = px.line(
            weekly,
            x="week",
            y="Load",
            title="Average Load Across Days of Week",
            markers=True,
        )
        fig.update_traces(line_color="#f59e0b")
        fig.update_layout(xaxis_tickmode="linear", xaxis_tick0=0, xaxis_dtick=1)
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Average Monthly Load Pattern")
    if len(filtered):
        monthly = filtered.groupby("month")["Load"].mean().reset_index()
        fig = px.line(
            monthly,
            x="month",
            y="Load",
            title="Average Load Across Months",
            markers=True,
        )
        fig.update_traces(line_color="#f59e0b")
        fig.update_layout(xaxis_tickmode="linear", xaxis_tick0=1, xaxis_dtick=1)
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Hourly Load by Season")
    if len(filtered):
        season_hour = filtered.groupby(["season", "hour"])["Load"].mean().reset_index()
        fig = px.line(
            season_hour,
            x="hour",
            y="Load",
            color="season",
            title="Hourly Load Profile Across Seasons",
            markers=True,
            color_discrete_sequence=["#f59e0b", "#fbbf24", "#34d399", "#6ee7b7"],
        )
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Temperature vs Daily Load")
    if len(filtered_daily):
        fig = px.scatter(
            filtered_daily,
            x="temp",
            y="Load",
            title="Temperature vs Avg Daily Load",
            trendline="ols",
        )
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Temperature vs Load by Season")
    if len(filtered_daily):
        fig = px.scatter(
            filtered_daily,
            x="temp",
            y="Load",
            color="season",
            title="Temperature vs Load by Season",
            color_discrete_sequence=["#f59e0b", "#fbbf24", "#34d399", "#6ee7b7"],
        )
        st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("Correlation: Temp vs Load")
    if len(filtered_daily):
        corr = filtered_daily[["temp", "Load", "rhum", "wspd"]].corr()
        fig = px.imshow(
            corr,
            text_auto=".2f",
            aspect="auto",
            title="Correlation Matrix",
            color_continuous_scale="RdBu_r",
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#f8fafc",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig, width="stretch")

with tab_details:
    st.subheader("Data Preview")
    st.dataframe(filtered.head(100), width="stretch")

# Footer
st.divider()
st.caption("Built with Streamlit | Data sources: archive_data.csv, delhi_weather_data.csv")
