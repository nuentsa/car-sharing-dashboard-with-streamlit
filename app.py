import pandas as pd
import streamlit as st
import plotly.express as px


# Load the data
@st.cache_data
def load_data_set(csv_file_path):
    """
    Load the Data from the CSV File
    and keep it in the application cache 
    """
    df = pd.read_csv(csv_file_path, parse_dates=["pickup_time", "dropoff_time"])
    return df

# Function to apply filters and return a filtered dataframe
def get_filtered_data(df, city_filter, brand_filter, date_range):
    return df[
        (df["car_city"].isin(city_filter)) & 
        (df["car_brand"].isin(brand_filter)) & 
        (df["pickup_time"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
    ]

# Read the Car Sharing Data Set
df = load_data_set("datasets/car_sharing_trips.csv")

# Create a Side bar with some filters
st.sidebar.header("Dashboard Filters")
city_filter = st.sidebar.multiselect("Select City", df["car_city"].unique(), default=df["car_city"].unique())
brand_filter = st.sidebar.multiselect("Select Car Brand", df["car_brand"].unique(), default=df["car_brand"].unique())
date_range = st.sidebar.date_input("Select Date Range", [df["pickup_time"].min(), df["pickup_time"].max()])
group_by_option = st.sidebar.selectbox(
    "Group trips by:", 
    ["car_city", "car_brand", "customer_name"]
)

# Apply the Filters on the dataframe
filtered_df = get_filtered_data(df, city_filter, brand_filter, date_range)

# Display some Summary Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Trips", filtered_df.shape[0])
col2.metric("Total Revenue ($)", f"${filtered_df['revenue'].sum():,.2f}")
col3.metric("Avg Trip Distance (miles)", f"{filtered_df['distance'].mean():.2f}")

grouped_data = filtered_df.groupby(group_by_option).size().reset_index(name="Total Trips")
# Display Title
st.write("Trip Metrics by " + group_by_option.replace("_", " ").title())
# Display Bar Chart
fig = px.bar(
    grouped_data, 
    x=group_by_option, 
    y="Total Trips", 
    title=f"Total Trips by {group_by_option.replace('_', ' ').title()}",
    text="Total Trips",
    color=group_by_option
)
st.plotly_chart(fig, use_container_width=True)
# Display the whole dataframe
st.subheader("Trip Data")
st.dataframe(filtered_df)
