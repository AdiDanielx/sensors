import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from PIL import Image

# User information
user_name = "Alex Green"

# Dashboard Title and Welcome Message
st.markdown(f"<h1 style='text-align: center;'>Smart Steps Dashboard for <br> {user_name}</h1>", unsafe_allow_html=True)

# Sidebar Time Frame Selection
time_frame = st.sidebar.selectbox(
    "Select Time Frame for Dashboard Display",
    ("Today", "Last Week", "Select Month")
)

col1, col2 = st.columns(2, gap="large")

# Today's Dashboard
if time_frame == "Today":
    st.markdown("<h2 style='text-align: center;'>Daily Progress Overview</h2>", unsafe_allow_html=True)

    st.write(f"""
    Welcome to the daily progress dashboard for **{user_name}**. This dashboard offers a snapshot of today's rehabilitation metrics, providing real-time insights into goal completion, weight application during walking, and weight consistency throughout the day.

    By reviewing these metrics, you can monitor the patient's adherence to their daily rehabilitation targets and make necessary adjustments to maximize recovery outcomes.
    """)

    st.subheader("1. Daily Goal Completion")
    completion = 75
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=completion,
        number={"suffix": "%"},
        title={"text": "150 meters left"},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#16a085"}}
    ))
    st.plotly_chart(fig)

    st.subheader("2. Weight Applied During Walking")
    pie_data = pd.DataFrame({
        "Category": ["Insufficient Weight", "Sufficient Weight"],
        "Values": [30, 70]
    })
    fig_pie = px.pie(pie_data, names="Category", values="Values",
                     color_discrete_sequence=["#abebc6", "#16a085"])
    st.plotly_chart(fig_pie)

    st.subheader("3. Weight Applied Over Time")
    time_data = pd.date_range(start="08:00", end="20:00", freq="H")
    weight_data = np.random.randint(20, 100, len(time_data))
    line_chart_data = pd.DataFrame({"Time": time_data, "Weight Applied (kg)": weight_data})
    fig_line = px.line(line_chart_data, x="Time", y="Weight Applied (kg)")
    fig_line.update_traces(line=dict(color="#16a085"))
    st.plotly_chart(fig_line)

# Last Week's Dashboard
if time_frame == "Last Week":
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    weight_data = np.random.randint(20, 100, size=7)
    time_in_ranges = [np.random.randint(30, 60) for _ in range(7)]
    distance_data = np.cumsum(np.random.randint(50, 150, size=7))
    step_data = np.random.randint(500, 1500, size=7)
    goal_completion = np.random.randint(60, 100, size=7)

    df = pd.DataFrame({
        "Day": days_of_week,
        "Average Weight Applied (kg)": weight_data,
        "Time in Sufficient Weight (min)": time_in_ranges,
        "Cumulative Distance (m)": distance_data,
        "Steps": step_data,
        "Goal Completion (%)": goal_completion
    })
    st.markdown("<h2 style='text-align: center;'>Weekly Progress Overview</h2>", unsafe_allow_html=True)

    st.write(f"""
    Welcome to the weekly progress dashboard for **{user_name}**. This dashboard provides a comprehensive view of rehabilitation metrics for the past week, including daily weight application averages, time spent in sufficient weight-bearing ranges, cumulative distance covered, and goal completion rates.

    Use these insights to track trends and monitor progress, helping to assess adherence to weekly rehabilitation goals and identify any areas where adjustments may be needed to enhance recovery outcomes.
    """)

    st.subheader("1. Average Weight Applied Throughout the Week")
    fig1 = px.line(df, x="Day", y="Average Weight Applied (kg)")
    fig1.update_traces(line=dict(color="#16a085"))
    st.plotly_chart(fig1)

    st.subheader("2. Time Spent in Sufficient vs. Insufficient Weight Ranges")
    total_time_per_day = np.random.randint(30, 90, size=7)
    insufficient_weight_time = total_time_per_day - df["Time in Sufficient Weight (min)"]
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=days_of_week, y=df["Time in Sufficient Weight (min)"], name="Sufficient Weight", marker_color="#16a085"))
    fig2.add_trace(go.Bar(x=days_of_week, y=insufficient_weight_time, name="Insufficient Weight", marker_color="#abebc6"))
    fig2.update_layout(barmode='stack', xaxis_title="Day", yaxis_title="Time (minutes)")
    st.plotly_chart(fig2)

    st.subheader("3. Cumulative Distance Covered Over the Week")
    fig3 = px.area(df, x="Day", y="Cumulative Distance (m)")
    fig3.update_traces(line=dict(color="#16a085"), fillcolor="#16a085")
    st.plotly_chart(fig3)

    st.subheader("4. Goal Completion Throughout the Week")
    fig8 = px.line(df, x="Day", y="Goal Completion (%)")
    fig8.update_traces(line=dict(color="#16a085"))
    st.plotly_chart(fig8)

# Monthly Dashboard
if time_frame == 'Select Month':
    date_range = pd.date_range(start="2023-08-01", end="2023-10-31", freq="D")
    data = {
        "Date": date_range,
        "Weight Applied (kg)": np.random.randint(20, 100, len(date_range)),
        "Time in Sufficient Weight (min)": np.random.randint(30, 60, len(date_range)),
        "Distance (m)": np.random.randint(100, 1000, len(date_range)),
        "Steps": np.random.randint(500, 2000, len(date_range)),
        "Goal Completion (%)": np.random.randint(50, 100, len(date_range))
    }
    df = pd.DataFrame(data)

    st.sidebar.header("Select Month and Year")
    year = st.sidebar.selectbox("Year", sorted(df["Date"].dt.year.unique(), reverse=True))
    month = st.sidebar.selectbox("Month", sorted(df["Date"].dt.month.unique(), reverse=True))

    filtered_df = df[(df["Date"].dt.year == year) & (df["Date"].dt.month == month)].copy()
    filtered_df["Day"] = filtered_df["Date"].dt.day
    filtered_df["Day of Week"] = filtered_df["Date"].dt.strftime('%A')
    filtered_df["Week"] = (filtered_df["Date"].dt.day - 1) // 7 + 1
    filtered_df = filtered_df[filtered_df["Week"] <= 4]
    st.markdown(f"<h2 style='text-align: center;'>Monthly Progress Overview for {datetime(year, month, 1).strftime('%B %Y')}</h2>", unsafe_allow_html=True)

    st.write(f"""
    This dashboard provides a detailed look at the rehabilitation progress for **{datetime(year, month, 1).strftime('%B %Y')}**. 
    Here, you’ll find insights into daily weight application, time spent in sufficient weight-bearing ranges, cumulative distance covered, step counts, and goal completion percentages.

    Use these metrics to monitor progress and identify areas that may need adjustment in the rehabilitation plan.
    """)

    st.subheader(f"1. Weekly Weight Application Trends for {datetime(year, month, 1).strftime('%B %Y')}")
    color_map = {1: "#a569bd", 2: "#48c9b0", 3: "#f4d03f", 4: "#5499c7"}
    fig = px.line(filtered_df, x="Day of Week", y="Weight Applied (kg)", color="Week")
    for i, week in enumerate(filtered_df["Week"].unique()):
        if week in color_map:
            fig.data[i].line.color = color_map[week]
    st.plotly_chart(fig)

    st.subheader("2. Time in Sufficient vs. Insufficient Weight Ranges")

    # Generate random total time per day and calculate insufficient weight time
    total_time_per_day = np.random.randint(30, 90, size=len(filtered_df))
    insufficient_weight_time = np.maximum(0, total_time_per_day - filtered_df["Time in Sufficient Weight (min)"])  # Ensure no negative values

    # Create the stacked bar chart
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=filtered_df["Day"], y=filtered_df["Time in Sufficient Weight (min)"], name="Sufficient Weight", marker_color="#16a085"))
    fig2.add_trace(go.Bar(x=filtered_df["Day"], y=insufficient_weight_time, name="Insufficient Weight", marker_color="#abebc6"))
    fig2.update_layout(barmode='stack', title="Time Spent in Sufficient vs. Insufficient Weight Ranges", xaxis_title="Day", yaxis_title="Time (minutes)")

    # Display the chart
    st.plotly_chart(fig2)

    st.subheader("3. Cumulative Distance Covered Throughout the Month")
    filtered_df["Cumulative Distance"] = filtered_df["Distance (m)"].cumsum()
    fig3 = px.area(filtered_df, x="Day", y="Cumulative Distance")
    fig3.update_traces(line=dict(color="#16a085"), fillcolor="#16a085")
    st.plotly_chart(fig3)

    st.subheader("4. Daily Goal Completion Percentage")
    fig4 = px.line(filtered_df, x="Day", y="Goal Completion (%)")
    fig4.update_traces(line=dict(color="#16a085"))
    st.plotly_chart(fig4)
