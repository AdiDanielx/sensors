
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pytz

st.markdown("<h1 style='text-align: center;'>Smart Steps: Crutch Pressure Monitoring Dashboard</h1>", unsafe_allow_html=True)
st.markdown("### Overview of Smart Steps")
st.markdown("Smart Steps is designed to provide insights into the pressure applied on crutches during rehabilitation.")

# סרגל ניווט
page = st.sidebar.selectbox("Select Page", ["Walking Statistics", "Time Walked", "Alerts Count"])

if page == "Walking Statistics":
    # דף ראשון
    dates = pd.date_range(start='2023-01-01', end='2023-01-02', freq='H')
    total_hours = len(dates)
    active_percentage = 0.5  
    inactive_percentage = 1 - active_percentage  
    num_active_hours = int(total_hours * active_percentage)
    num_inactive_hours = total_hours - num_active_hours
    weights = np.zeros(total_hours)
    active_hours_indices = np.random.choice(total_hours, num_active_hours, replace=False)
    weights[active_hours_indices] = np.random.uniform(11, 50, num_active_hours)  # משקל מעל 10
    inactive_indices = [i for i in range(total_hours) if i not in active_hours_indices]
    weights[inactive_indices] = np.random.uniform(0, 10, num_inactive_hours)  # משקל מתחת ל-10
    data = pd.DataFrame({'DateTime': dates, 'WeightOnCrutches': weights})
    israel_timezone = pytz.timezone('Asia/Jerusalem')
    current_hour = datetime.now(israel_timezone).hour
    data = data[data['DateTime'].dt.hour <= current_hour]
    active_hours = data[data['WeightOnCrutches'] > 10]['DateTime'].dt.hour.value_counts().sort_index()
    active_time = active_hours.sum()
    inactive_time = len(data) - active_time 
    fig_today = go.Figure(data=[go.Pie(
        labels=['Active', 'Inactive'],
        values=[active_time, inactive_time],
        hole=0.3,
        textinfo='label+percent',
        hoverinfo='label+value+text',
        hovertext=['Hours: {}'.format(active_time), 'Hours: {}'.format(inactive_time)]
    )])
    fig_today.update_layout(title_text=f"Percentage of Time Spent<br> Walking Until Now <br> (at {current_hour})", title_font=dict(size=16))
    st.plotly_chart(fig_today)

elif page == "Time Walked":
    # דף שני
    dates = pd.date_range(start='2023-10-23', end='2023-10-29', freq='D')  
    time_walked = np.random.randint(30, 120, size=len(dates))  
    alerts_count = np.random.randint(1, 5, size=len(dates))  
    weight_factor = np.random.randint(30, 80, size=len(dates))
    data_2 = pd.DataFrame({
        'Date': dates,
        'TotalTimeWalked': time_walked,
        'AlertsCount': alerts_count,
        'WeightApplied': weight_factor
    })

    fig = px.bar(data_2, x=data_2['Date'].dt.strftime('%A'), y='TotalTimeWalked',
                 labels={'TotalTimeWalked': 'Total Time Walked (minutes)', 'x': 'Day'},
                 title="Total Time Walked Each <br> Day of the Week")
    fig.update_traces(marker_line_width=1.5, marker_line_color="black")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

elif page == "Alerts Count":
    # דף שלישי
    dates = pd.date_range(start='2023-10-23', end='2023-10-29', freq='D')  
    time_walked = np.random.randint(30, 120, size=len(dates))  
    alerts_count = np.random.randint(1, 5, size=len(dates))  
    weight_factor = np.random.randint(30, 80, size=len(dates))
    data_2 = pd.DataFrame({
        'Date': dates,
        'TotalTimeWalked': time_walked,
        'AlertsCount': alerts_count,
        'WeightApplied': weight_factor
    })

    fig_alerts = px.bar(data_2, x=data_2['Date'].dt.strftime('%A'), y='AlertsCount',
                        labels={'AlertsCount': 'Alerts Count', 'x': 'Day'},
                        title="Alerts Count Per <br> Day of the Week")
    fig_alerts.update_traces(marker_line_width=1.5, marker_line_color="black")
    fig_alerts.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_alerts)
