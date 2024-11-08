import pandas as pd
from datetime import timedelta
import streamlit as st
import re  # Import regex

# Streamlit app title
st.set_page_config(page_title="Service Feedback Reports", page_icon="logo.jpg")
st.title("Netcreators Automation")
st.title("Customer Service Feedback Reports")
st.markdown(
    """
        Upload the .txt file, select the date and time, and generate a summary report of customer service feedback.
        Follow the instructions as given below to use the app.
    """
)

# File uploader
uploaded_file = st.file_uploader("Upload your log file", type=["txt"])

if uploaded_file is not None:
    # Load the data from the uploaded text file
    log_data = uploaded_file.readlines()

    # Extract relevant entries from the log data
    events = []
    for line in log_data:
        line = line.decode("utf-8")  # Decode bytes to string

        # Regex to extract timestamp and event type (feedback type)
        if "Customer felt" in line or "Service Experienced" in line:
            parts = line.split("\t")
            timestamp = parts[0].strip()
            feedback = parts[1].strip()

            # Append to the events list
            events.append((timestamp, feedback))

    # Create a DataFrame from the events
    df = pd.DataFrame(events, columns=["Timestamp", "Feedback Type"])

    # Convert Timestamp to datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%Y-%m-%d %p %I:%M")

    # Date filter inputs in Streamlit
    st.sidebar.header("Filter Options")

    # Select a date range
    start_date = st.sidebar.date_input(
        "Start date", value=pd.to_datetime(df["Timestamp"].min()).date()
    )
    end_date = st.sidebar.date_input(
        "End date", value=pd.to_datetime(df["Timestamp"].max()).date()
    )

    # Optionally select time range
    filter_time = st.sidebar.checkbox("Filter by time range")
    if filter_time:
        start_time = st.sidebar.time_input("Start time", value=pd.Timestamp("00:00:00").time())
        end_time = st.sidebar.time_input("End time", value=pd.Timestamp("23:59:59").time())
    else:
        start_time = pd.Timestamp("00:00:00").time()
        end_time = pd.Timestamp("23:59:59").time()

    # Combine selected date and time into datetime
    start_datetime = pd.Timestamp.combine(start_date, start_time)
    end_datetime = pd.Timestamp.combine(end_date, end_time)

    # Filter the data based on selected date and time range
    df_filtered = df[(df["Timestamp"] >= start_datetime) & (df["Timestamp"] <= end_datetime)]

    # ** Add Feedback Type Filter **
    feedback_options = df_filtered["Feedback Type"].unique()
    selected_feedback = st.sidebar.multiselect("Select Feedback Types", feedback_options, feedback_options)

    # Filter the data based on selected feedback types
    df_filtered = df_filtered[df_filtered["Feedback Type"].isin(selected_feedback)]

    # Display the filtered summary DataFrame in Streamlit
    st.write("Filtered Customer Feedback Summary")
    st.dataframe(df_filtered)

    # Generate dynamic file name based on date range
    file_name = f"service_feedback_summary_{start_date}_to_{end_date}.xlsx".replace(":", "-")

    # Option to download the cleaned data
    if st.button("Download cleaned data as Excel"):
        output_file_path = file_name
        df_filtered.to_excel(output_file_path, index=False)

        with open(output_file_path, "rb") as file:
            btn = st.download_button(
                label="Download Excel",
                data=file,
                file_name=output_file_path,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
