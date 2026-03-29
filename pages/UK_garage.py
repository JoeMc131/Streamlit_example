import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import re


headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

url = 'https://en.wikipedia.org/wiki/List_of_UK_garage_songs'
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')

table_boxes = soup.find_all('table', class_="wikitable plainrowheaders")

songs_dict = {
    'song':[],
    'artist':[],
    'year':[],
    'UK chart position':[],
    'UK Dance Singles':[]
}

column_names = [n.text.strip() for n in table_boxes[0].find_all('tr')[0].find_all('th')]

for table in table_boxes:
    songs = table.find_all('tr')
    for song in songs[1:]:

        name = song.find('th', scope = 'row').text.strip()
        
        data = song.find_all('td', recursive=False)
        songs_dict['song'].append(name)
        songs_dict['artist'].append(data[0].text.strip())
        songs_dict['year'].append(data[1].text.strip())
        songs_dict['UK chart position'].append(re.sub(r'\[.*?\]', '', data[2].text.strip()))
        songs_dict['UK Dance Singles'].append(re.sub(r'\[.*?\]', '', data[3].text.strip()))
        # songs_dict['song'].append(song[0].text)
        # songs_dict['artist'].append(song[1].text)
        # songs_dict['year'].append(song[2].text)
        # songs_dict['UK chart position'].append(song[3]).text
        # songs_dict['UK Dance Singles'].append(song[4]).text

# print(songs_dict)

df = pd.DataFrame(songs_dict)

df = df.apply(lambda x: x.str.replace(r'\[.*\]', '', regex=True) if x.dtype == 'object' else x)
df['year'] = df['year'].str.replace(r'\/.*', '', regex=True)
df['year'] = df['year'].astype(int)

df['UK chart position'] = df['UK chart position'].str.replace(r'\/.*', '', regex=True)

df['UK chart position'] = df['UK chart position'].replace({'—':'0',
                                                           '':'0',
                                                           '-':'0'})
df['UK Dance Singles'] = df['UK Dance Singles'].replace({'—':'0', '':'0'})

df['UK chart position'] = df['UK chart position'].astype(int)
df['UK Dance Singles'] = df['UK Dance Singles'].astype(int)

# create site
st.title('UK garage songs that charted')

st.markdown(
    """
    This page scrapes data from [Wikipedia](https://en.wikipedia.org/wiki/List_of_UK_garage_songs)
    and feeds it into a dataframe. The data can then be analysed here using user-defined options
    """
)

columns = st.columns(2)

year_begin = columns[0].number_input(label='Min. Year', value=df.year.min())
min_uk_chart = columns[0].number_input(label='Min. chart position', value=1)
min_Dance = columns[0].number_input(label='Min. Dance Singles', value=1)

year_end = columns[1].number_input(label='Max. Year', value=df.year.max())
max_uk_chart = columns[1].number_input(label='Min. chart position', value=df['UK chart position'].max())
max_Dance = columns[1].number_input(label='Min. Dance Singles', value=df['UK Dance Singles'].max())


if st.button('Show'):
    df = df[df['year'] >= year_begin]
    df = df[df['year'] <= year_end]

    df = df[df['UK chart position'] >= min_uk_chart] 
    df = df[df['UK chart position'] <= max_uk_chart]

    df = df[df['UK Dance Singles'] >= min_Dance]
    df = df[df['UK Dance Singles'] <= max_Dance]

    st.write(df)

