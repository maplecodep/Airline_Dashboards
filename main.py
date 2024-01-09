# Import required libraries
import pandas as pd
import streamlit as st
import plotly.express as px

# Read the airline data into pandas dataframe
airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding="ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# List of years 
year_list = [i for i in range(2005, 2021, 1)]

# Page title
st.title('US Domestic Airline Flights Performance')

# Sidebar with input widgets
report_type = st.sidebar.selectbox('Report Type:', ['Yearly Airline Performance Report', 'Yearly Airline Delay Report'])
selected_year = st.sidebar.selectbox('Choose Year:', year_list)

# Filter data based on selected year
df = airline_data[airline_data['Year'] == int(selected_year)]

# Compute data based on report type
if report_type == 'Yearly Airline Performance Report':
    # Cancellation Category Count
    bar_data = df.groupby(['Month', 'CancellationCode'])['Flights'].sum().reset_index()
    # Average flight time by reporting airline
    line_data = df.groupby(['Month', 'Reporting_Airline'])['AirTime'].mean().reset_index()
    # Diverted Airport Landings
    div_data = df[df['DivAirportLandings'] != 0.0]
    # Source state count
    map_data = df.groupby(['OriginState'])['Flights'].sum().reset_index()
    # Destination state count
    tree_data = df.groupby(['DestState', 'Reporting_Airline'])['Flights'].sum().reset_index()

    # Plot graphs
    st.plotly_chart(px.bar(bar_data, x='Month', y='Flights', color='CancellationCode', title='Monthly Flight Cancellation'))
    st.plotly_chart(px.line(line_data, x='Month', y='AirTime', color='Reporting_Airline', title='Average monthly flight time (minutes) by airline'))
    st.plotly_chart(px.pie(div_data, values='Flights', names='Reporting_Airline', title='% of flights by reporting airline'))
    st.plotly_chart(px.choropleth(map_data, locations='OriginState', color='Flights', hover_data=['OriginState', 'Flights'], locationmode='USA-states', color_continuous_scale='GnBu', range_color=[0, map_data['Flights'].max()]).update_layout(title_text='Number of flights from origin state', geo_scope='usa'))
    st.plotly_chart(px.treemap(tree_data, path=['DestState', 'Reporting_Airline'], values='Flights', color='Flights', color_continuous_scale='RdBu', title='Flight count by airline to destination state'))

else:
    # Compute delay averages
    avg_car = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()

    # Plot graphs
    st.plotly_chart(px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline', title='Average carrrier delay time (minutes) by airline'))
    st.plotly_chart(px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline', title='Average weather delay time (minutes) by airline'))
    st.plotly_chart(px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline', title='Average NAS delay time (minutes) by airline'))
    st.plotly_chart(px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline', title='Average security delay time (minutes) by airline'))
    st.plotly_chart(px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline', title='Average late aircraft delay time (minutes) by airline'))
