import streamlit as st
import pandas as pd
import main
from PIL import Image
import requests

st.set_page_config(layout="wide")
nav = st.sidebar.radio(label='', options=['Home', 'Contribute'])
st.title('The Movie Recommender.')

if nav == 'Home':
    st.header("Home")
    option = st.selectbox('Choose your movie', (i for i in main.titles))
    st.subheader('You selected:')
    option_img_response = requests.get(f'http://www.omdbapi.com/?t={option}&'
                                       f'apikey=2b84cbca')
    option_img = option_img_response.json()

    st.image(option_img['Poster'], width=200, caption=option)

    rec = main.recommend(option)
    images = []
    summaries = []
    for i in rec:
        images.append((i, (requests.get(
            f'http://www.omdbapi.com/?t={i}&apikey=2b84cbca')).json()))
        summaries.append((' '.join(str(v) for v in (
            ((main.movies.loc[main.movies['title'] == i])['overview']).
            to_list())[0])))

    st.subheader('Check out these recommendations:')

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(images[0][1]['Poster'], width=200,
                 caption=f'{images[0][0]}: {summaries[0]}')
    with col2:
        st.image(images[1][1]['Poster'], width=200,
                 caption=f'{images[1][0]}: {summaries[1]}')
    with col3:
        st.image(images[2][1]['Poster'], width=200,
                 caption=f'{images[2][0]}: {summaries[2]}')

    col4, col5, col6 = st.columns(3)
    with col4:
        st.image(images[3][1]['Poster'], width=200,
                 caption=f'{images[3][0]}: {summaries[3]}')
    with col5:
        st.image(images[4][1]['Poster'], width=200,
                 caption=f'{images[4][0]}: {summaries[4]}')
    with col6:
        st.image(images[5][1]['Poster'], width=200,
                 caption=f'{images[5][0]}: {summaries[5]}')