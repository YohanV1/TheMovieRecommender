import streamlit as st
import main
import requests

st.set_page_config(layout="wide")

if 'movie_tracker' not in st.session_state:
    st.session_state['movie_tracker'] = 0

if st.session_state['movie_tracker'] == 0:
    st.title('The Movie Recommender.')

    option = st.selectbox('Select a movie.', (i for i in main.titles), index=46)

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

    col1, ecol1, col2, ecol2, col3 = st.columns([1.5, 0.5, 1.5, 0.5, 1.5])

    with col1:
        b1 = st.button(images[0][0], key=1)
        st.session_state['movie_tracker'] += 1
        try:
            st.image(images[0][1]['Poster'], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[0]}')

    with col2:
        b2 = st.button(images[1][0], key=2)

        try:
            st.image(images[1][1]['Poster'], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[1]}')

    with col3:
        b3 = st.button(images[2][0], key=3)

        try:
            st.image(images[2][1]['Poster'], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[2]}')

    col4, ecol3, col5, ecol4, col6 = st.columns([1.5, 0.5, 1.5, 0.5, 1.5])

    with col4:
        b4 = st.button(images[3][0], key=4)

        try:
            st.image(images[3][1]['Poster'], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[3]}')

    with col5:
        b5 = st.button(images[4][0], key=5)

        try:
            st.image(images[4][1]['Poster'], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[4]}')

    with col6:
        b6 = st.button(images[5][0], key=6)

        try:
            st.image(images[5][1]['Poster'], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[5]}')

    col7, ecol5, col8, ecol6, col9 = st.columns([1.5, 0.5, 1.5, 0.5, 1.5])

    with col7:
        b7 = st.button(images[6][0], key=7)

        try:
            st.image(images[6][1]['Poster'], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[6]}')

    with col8:
        b8 = st.button(images[7][0], key=8)

        try:
            st.image(images[7][1]['Poster'], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[7]}')

    with col9:
        b9 = st.button(images[8][0], key=9)

        try:
            st.image(images[8][1]['Poster'], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[8]}')

else:
    st.write("hi")
    print("hi")

