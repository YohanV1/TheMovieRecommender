import streamlit as st
import main

st.set_page_config(layout="wide")

if 'movie_tracker' not in st.session_state:
    st.session_state['movie_tracker'] = -1

if 'movie_index' not in st.session_state:
    st.session_state['movie_index'] = 46


if st.session_state['movie_tracker'] == -1:
    st.title('The Movie Recommender.')

    option = st.selectbox('Select a movie.', (i for i in main.titles),
                          index=st.session_state['movie_index'])

    st.session_state['movie_index'] = main.titles.index(option)

    if st.button(option, key=0):
        st.session_state['movie_tracker'] = 10
        st.experimental_rerun()

    movie_id = main.movies.iloc[st.session_state['movie_index']].id

    st.image(main.fetch_poster(movie_id), width=200)

    names, posters, summaries = main.recommend(option)
    st.subheader('Check out these recommendations:')

    col1, ecol1, col2, ecol2, col3 = st.columns([1.5, 0.5, 1.5, 0.5, 1.5])

    with col1:
        b1 = st.button(names[0], key=1)
        if b1:
            st.session_state['movie_tracker'] = 0
            st.experimental_rerun()
        try:
            st.image(posters[0], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[0][:200]}...')

    with col2:
        b2 = st.button(names[1], key=2)
        if b2:
            st.session_state['movie_tracker'] = 1
            st.experimental_rerun()
        try:
            st.image(posters[1], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[1][:200]}...')

    with col3:
        b3 = st.button(names[2], key=3)
        if b3:
            st.session_state['movie_tracker'] = 2
            st.experimental_rerun()
        try:
            st.image(posters[2], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[2][:200]}...')

    col4, ecol3, col5, ecol4, col6 = st.columns([1.5, 0.5, 1.5, 0.5, 1.5])

    with col4:
        b4 = st.button(names[3], key=4)
        if b4:
            st.session_state['movie_tracker'] = 3
            st.experimental_rerun()
        try:
            st.image(posters[3], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[3][:200]}...')

    with col5:
        b5 = st.button(names[4], key=5)
        if b5:
            st.session_state['movie_tracker'] = 4
            st.experimental_rerun()
        try:
            st.image(posters[4], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[4][:200]}...')

    with col6:
        b6 = st.button(names[5], key=6)
        if b6:
            st.session_state['movie_tracker'] = 5
            st.experimental_rerun()
        try:
            st.image(posters[5], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[5][:200]}...')

    col7, ecol5, col8, ecol6, col9 = st.columns([1.5, 0.5, 1.5, 0.5, 1.5])

    with col7:
        b7 = st.button(names[6], key=7)
        if b7:
            st.session_state['movie_tracker'] = 6
            st.experimental_rerun()
        try:
            st.image(posters[6], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[6][:200]}...')

    with col8:
        b8 = st.button(names[7], key=8)
        if b8:
            st.session_state['movie_tracker'] = 7
            st.experimental_rerun()
        try:
            st.image(posters[7], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[7][:200]}...')

    with col9:
        b9 = st.button(names[8], key=9)
        if b9:
            st.session_state['movie_tracker'] = 8
            st.experimental_rerun()
        try:
            st.image(posters[8], width=250)
        except KeyError:
            st.text('Poster unavailable.')
        st.caption(f'{summaries[8][:200]}...')

else:
    b = st.button("Go back")
    if b:
        st.session_state['movie_tracker'] = -1
        st.experimental_rerun()
