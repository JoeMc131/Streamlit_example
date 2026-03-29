
import streamlit as st

# establish pages
main_pg = st.Page('./pages/main.py', title='Home')
tornado_pg = st.Page('./pages/earthquakes.py', title='Earthquakes')
pokemon_pg = st.Page('./pages/Pokemon.py', title='Shiny Pokemon')
uk_garage_pg = st.Page('./pages/UK_garage', title='UK garage')

pg = st.navigation([main_pg, tornado_pg, pokemon_pg, uk_garage_pg])

pg.run()