import streamlit as st
import pandas as pd
import main
from PIL import Image
import requests

st.set_page_config(layout="wide")
st.title('The Movie Recommender.')

options = list(main.titles)
options.insert(0, '')
option = st.selectbox('Select a movie.', options)
if option != '':
    option_img_response = requests.get(f'http://www.omdbapi.com/?t={option}&'
                                       f'apikey=2b84cbca')
    option_img = option_img_response.json()

    st.image(option_img['Poster'], width=250, caption=option)

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

    col1, col2, col3 = st.columns(3, gap='medium')

    with col1:
        st.write(images[0][0])
        try:
            st.image(images[0][1]['Poster'], width=250,
                     caption=f'{summaries[0]}')
        except KeyError:
            st.text('Details unavailable.')

    with col2:
        st.write(images[1][0])
        try:
            st.image(images[1][1]['Poster'], width=250,
                     caption=f'{summaries[1]}')
        except KeyError:
            st.text('Details unavailable.')

    with col3:
        st.write(images[2][0])
        try:
            st.image(images[2][1]['Poster'], width=250,
                     caption=f'{summaries[2]}')
        except KeyError:
            st.text('Details unavailable.')

    col4, col5, col6 = st.columns(3, gap='medium')

    with col4:
        st.write(images[3][0])
        try:
            st.image(images[3][1]['Poster'], width=250,
                     caption=f'{summaries[3]}')
        except KeyError:
            st.text('Details unavailable.')

    with col5:
        st.write(images[4][0])
        try:
            st.image(images[4][1]['Poster'], width=250,
                     caption=f'{summaries[4]}')
        except KeyError:
            st.text('Details unavailable.')

    with col6:
        st.write(images[5][0])
        try:
            st.image(images[5][1]['Poster'], width=250,
                     caption=f'{summaries[5]}')
        except KeyError:
            st.text('Details unavailable.')

    col7, col8, col9 = st.columns(3, gap='medium')

    with col7:
        st.write(images[6][0])
        try:
            st.image(images[6][1]['Poster'], width=250,
                     caption=f'{summaries[6]}')
        except KeyError:
            st.text('Details unavailable.')

    with col8:
        st.write(images[7][0])
        try:
            st.image(images[7][1]['Poster'], width=250,
                     caption=f'{summaries[7]}')
        except KeyError:
            st.text('Details unavailable.')

    with col9:
        st.write(images[8][0])
        try:
            st.image(images[8][1]['Poster'], width=250,
                     caption=f'{summaries[8]}')
        except KeyError:
            st.text('Details unavailable.')
