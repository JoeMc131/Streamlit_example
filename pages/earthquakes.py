 
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# The various urls needed to retrieve data from
urls = {
    'hour':'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson',
    'day':'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson',
    'week':'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson',
    'month':'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson',
}

def make_dataframe(time_period):
    # Data is messy so need to gather things in list and then convert to dataframe
    web_data = requests.get(urls[time_period])
    data_json = web_data.json()

    mag = []
    lat = []
    long = []
    depth = []
    tsunami = []
    place = []

    for i, event in enumerate(data_json['features']):
        mag.append(event['properties']['mag'])
        lat.append(event['geometry']['coordinates'][1])
        long.append(event['geometry']['coordinates'][0])
        depth.append(event['geometry']['coordinates'][2])
        tsunami.append(event['properties']['tsunami'])
        place.append(event['properties']['place'])



    df = pd.DataFrame({
        'LAT':lat,
        'LON':long,
        'Mag':mag,
        'Depth':depth,
        'Tsunami Warning':tsunami,
        'Location':place
    })

    return df


# start streamlit 
st.title('Earthquake data analysis')

st.markdown('This page uses data provided by [USGS](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)' \
' to display earthquakes from a selected time period, display these earthquakes on a map and ' \
'show some statistics associated with the requested dataset')

earthquake_period = st.radio('Select earthquakes from past:',
                             options=['hour', 'day', 'week', 'month'])

# make dataframe and convert boolean values for tsunami to words
df = make_dataframe(earthquake_period)
df['Tsunami Warning'] = df['Tsunami Warning'].map({1:'Yes', 0:'No'})


mag_threshold = st.number_input(label='With magnitude greater than:', value=0)

if st.button('Show'):
    
    # filter by magnitude
    df = df[df['Mag']>mag_threshold]

    # display table
    st.write(df[['Location', 'Mag', 'Depth', 'Tsunami Warning']])

    # display map
    st.title('Map of events')
    m = st.map(df, size = 50)

    # display statistics and graph
    st.title('Key statistics')

    tsunami_percentage = (len(df[df['Tsunami Warning'] == 'Yes'])/len(df)) * 100

    columns = st.columns(3)
    columns[0].metric(label='Number of earthquakes', value = len(df))
    columns[1].metric(label='Mean Magnitude', value = f'{df['Mag'].mean():.2f}')
    columns[2].metric(label='Percentage with Tsunami Warnings', value=f'{tsunami_percentage:.2f} %')
    
    fig, ax = plt.subplots()
    ax.hist(df['Mag'], color = 'black')
    ax.set_xlabel('Mag')
    ax.set_ylabel('Count')
    st.pyplot(fig)




# data = pd.read_json(request.json)

# data.head()