import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Delhi Electricity Load", layout="wide")
st.title("⚡ Delhi Electricity Load vs Weather")
st.markdown("Time series analysis of electricity demand and temperature.")

df = pd.read_csv("delhi_weather_data.csv")
load = pd.read_csv("archive_data.csv")

with st.sidebar:
    st.header("Filters")
    seasons = st.multiselect("Season", options=["Winter", "Summer", "Monsoon"], default=["Winter", "Summer", "Monsoon"])

filtered = df[df["Season"].isin(seasons)] if "Season" in df.columns else df

col1, col2, col3 = st.columns(3)
col1.metric("Records", len(filtered))
col2.metric("Avg Temp (°C)", f"{filtered['Temperature'].mean():.1f}" if "Temperature" in filtered.columns else "N/A")
col3.metric("Avg Load (MW)", f"{load['Load'].mean():.0f}" if "Load" in load.columns else "N/A")

st.subheader("Temperature Trend")
if "Temperature" in filtered.columns and "Date" in filtered.columns:
    fig = px.line(filtered, x="Date", y="Temperature")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Load Distribution")
if "Load" in load.columns:
    fig = px.histogram(load, x="Load", nbins=50)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Temperature vs Load")
if "Temperature" in filtered.columns and "Load" in load.columns:
    merged = pd.concat([filtered.reset_index(drop=True), load.reset_index(drop=True)], axis=1)
    fig = px.scatter(merged, x="Temperature", y="Load")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Data Preview")
st.dataframe(filtered.head(100))
