import streamlit as st
import pandas as pd
import numpy as np
import requests
import pickle
import time

st.set_page_config(layout="wide", page_title='The Movie Recommender')

if 'movie_tracker' not in st.session_state:
    st.session_state['movie_tracker'] = -1

if 'movie_index' not in st.session_state:
    st.session_state['movie_index'] = 46

if 'rec_names' not in st.session_state:
    st.session_state['rec_names'] = []

if 'rec_posters' not in st.session_state:
    st.session_state['rec_posters'] = []

if 'rec_summaries' not in st.session_state:
    st.session_state['rec_summaries'] = []

if 'rec_ids' not in st.session_state:
    st.session_state['rec_ids'] = []

if 'flag' not in st.session_state:
    st.session_state['flag'] = 0


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?" \
          "api_key=433ff6eeee0036e8693c029787f184c5&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def fetch_actor_image(actor_id):
    url = f"https://api.themoviedb.org/3/person/{actor_id}?" \
          f"api_key=433ff6eeee0036e8693c029787f184c5&language=en-US"
    data = requests.get(url)
    data = data.json()
    actor_path = data['profile_path']
    full_path = "https://image.tmdb.org/t/p/original/" + str(actor_path)
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True,
                         key=lambda x: x[1])[1:10]

    recommended_movies = []
    recommended_movie_posters = []
    recommended_movies_summaries = []
    recommended_movies_ids = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies_ids.append(movie_id)
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_summaries.append(' '.join(movies.iloc[i[0]].overview))
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies_ids, recommended_movies, \
        recommended_movie_posters, \
        recommended_movies_summaries


@st.cache_resource
def load_data():
    movies = pickle.load(open('models/movies.pkl', 'rb'))
    movies_details = pickle.load(open('models/movies_data.pkl', 'rb'))
    similarity = pickle.load(open('models/similarity.pkl', 'rb'))
    return movies, movies_details, similarity


movies, movies_data, similarity = load_data()
titles = list(movies['title'])

if st.session_state['movie_tracker'] == -1:

    st.title('The Movie Recommender.')

    option = st.selectbox('Select a movie.', titles, index=st.session_state['movie_index'])

    if titles.index(option) != st.session_state['movie_index']:
        st.session_state['movie_index'] = titles.index(option)
        st.experimental_rerun()

    movie_id = movies.iloc[st.session_state['movie_index']].id

    st.image(fetch_poster(movie_id), width=200)

    with st.spinner(text='Loading...'):
        ids, names, posters, summaries = recommend(option)
        time.sleep(0.01)

    st.session_state['rec_ids'] = ids
    st.session_state['rec_names'] = names
    st.session_state['rec_posters'] = posters
    st.session_state['rec_summaries'] = summaries

    st.subheader('Check out these recommendations:')

    col1, ecol1, col2, ecol2, col3 = st.columns([1.5, 0.5, 1.5, 0.5, 1.5])

    with col1:
        if st.button(names[0], key=1):
            st.session_state['movie_tracker'] = 0
            st.experimental_rerun()
        st.image(posters[0], width=250)
        st.write(
            f"Rating: {(movies_data[movies_data['id'] == ids[0]]['vote_average'].values[0] + 0.6).round(1)}")
        st.caption(f'{summaries[0][:200]}...')

    with col2:
        if st.button(names[1], key=2):
            st.session_state['movie_tracker'] = 1
            st.experimental_rerun()
        st.image(posters[1], width=250)
        st.write(f"Rating: {(movies_data[movies_data['id'] == ids[1]]['vote_average'].values[0] + 0.6).round(1)}")
        st.caption(f'{summaries[1][:200]}...')

    with col3:
        if st.button(names[2], key=3):
            st.session_state['movie_tracker'] = 2
            st.experimental_rerun()
        st.image(posters[2], width=250)
        st.write(f"Rating: {(movies_data[movies_data['id'] == ids[2]]['vote_average'].values[0] + 0.6).round(1)}")
        st.caption(f'{summaries[2][:200]}...')

    col4, ecol3, col5, ecol4, col6 = st.columns([1.5, 0.5, 1.5, 0.5, 1.5])

    with col4:
        if st.button(names[3], key=4):
            st.session_state['movie_tracker'] = 3
            st.experimental_rerun()
        st.image(posters[3], width=250)
        st.write(
            f"Rating: {(movies_data[movies_data['id'] == ids[3]]['vote_average'].values[0] + 0.6).round(1)}")
        st.caption(f'{summaries[3][:200]}...')

    with col5:
        if st.button(names[4], key=5):
            st.session_state['movie_tracker'] = 4
            st.experimental_rerun()
        st.image(posters[4], width=250)
        st.write(
            f"Rating: {(movies_data[movies_data['id'] == ids[4]]['vote_average'].values[0] + 0.6).round(1)}")
        st.caption(f'{summaries[4][:200]}...')

    with col6:
        if st.button(names[5], key=6):
            st.session_state['movie_tracker'] = 5
            st.experimental_rerun()
        st.image(posters[5], width=250)
        st.write(
            f"Rating: {(movies_data[movies_data['id'] == ids[5]]['vote_average'].values[0] + 0.6).round(1)}")
        st.caption(f'{summaries[5][:200]}...')

    col7, ecol5, col8, ecol6, col9 = st.columns([1.5, 0.5, 1.5, 0.5, 1.5])

    with col7:
        if st.button(names[6], key=7):
            st.session_state['movie_tracker'] = 6
            st.experimental_rerun()
        st.image(posters[6], width=250)
        st.write(
            f"Rating: {(movies_data[movies_data['id'] == ids[6]]['vote_average'].values[0] + 0.6).round(1)}")
        st.caption(f'{summaries[6][:200]}...')

    with col8:
        if st.button(names[7], key=8):
            st.session_state['movie_tracker'] = 7
            st.experimental_rerun()
        st.image(posters[7], width=250)
        st.write(
            f"Rating: {(movies_data[movies_data['id'] == ids[7]]['vote_average'].values[0] + 0.6).round(1)}")
        st.caption(f'{summaries[7][:200]}...')

    with col9:
        if st.button(names[8], key=9):
            st.session_state['movie_tracker'] = 8
            st.experimental_rerun()
        st.image(posters[8], width=250)
        st.write(f"Rating: {(movies_data[movies_data['id'] == ids[8]]['vote_average'].values[0]+0.6).round(1)}")
        st.caption(f'{summaries[8][:200]}...')

else:

    flag = st.session_state['movie_tracker']
    ids = st.session_state['rec_ids']
    img_path = st.session_state['rec_posters'][flag]
    release_date = movies_data[movies_data['id'] == ids[flag]]['release_date'].values[
        0].replace('-', '/')
    production_area = movies_data[movies_data['id'] == ids[flag]]['production_countries'].values[
        0]
    genres = movies_data[movies_data['id'] == ids[flag]]['genres'].values[0]
    runtime = int(
        movies_data[movies_data['id'] == ids[flag]]['runtime'].values[0])

    actors = movies_data[movies_data['id'] == ids[flag]]['cast'].values[0]
    actors = actors[0:8]
    l_actors = len(actors)
    actor_details = []

    crew = movies_data[movies_data['id'] == ids[flag]]['crew'].values[0]
    crew = crew[0:4]
    l_crew = len(crew)

    for i in range(l_actors):
        d = {'character': actors[i]['character'],
             'image': fetch_actor_image(actors[i]['id']),
             'name': actors[i]['name']}
        actor_details.append(d)

    b = st.button("Go back")
    if b:
        st.session_state['movie_tracker'] = -1
        st.session_state['flag'] = 1
        st.experimental_rerun()

    col1, col2, ecol1 = st.columns([0.9, 1.3, 0.3])

    with col1:
        st.image(img_path, width=325)
    with col2:
        st.header(st.session_state['rec_names'][flag])
        text = f"{release_date} ({production_area[17:19]}) • " \
               f"{', '.join(genres)} • {runtime//60}h {runtime%60}m"
        st.write(text)

        st.success(f"Rating: {(movies_data[movies_data['id'] == ids[flag]]['vote_average'].values[0]+0.6).round(1)}"
                   f" ({movies_data[movies_data['id'] == ids[flag]]['vote_count'].values[0]} votes)")

        if not pd.isna(movies_data[movies_data['id'] == ids[flag]]['tagline'].values[0]):
            st.markdown(f"_{movies_data[movies_data['id'] == ids[flag]]['tagline'].values[0]}_")

        st.subheader("Overview")
        st.write(st.session_state['rec_summaries'][flag])

        col1a, col1b, col1c, col1d = st.columns(4)

        if l_crew >= 1:
            with col1a:
                st.markdown(f"**{list(crew[0].values())[0]}**  \n{list(crew[0].keys())[0]}")

        if l_crew >= 2:
            with col1b:
                st.markdown(f"**{list(crew[1].values())[0]}**  \n{list(crew[1].keys())[0]}")

        if l_crew >= 3:
            with col1c:
                st.markdown(f"**{list(crew[2].values())[0]}**  \n{list(crew[2].keys())[0]}")

        if l_crew >= 4:
            with col1d:
                st.markdown(f"**{list(crew[3].values())[0]}**  \n{list(crew[3].keys())[0]}")

    st.markdown('##')
    st.subheader("Top Billed Cast")

    num_columns = 4
    num_actors_per_column = (l_actors + num_columns - 1) // num_columns

    columns = st.columns(num_columns)

    for col_idx in range(num_columns):
        with columns[col_idx]:
            for i in range(col_idx * num_actors_per_column,
                           min((col_idx + 1) * num_actors_per_column,
                               l_actors)):
                if 'None' not in actor_details[i]['image']:
                    st.image(actor_details[i]['image'], width=170)
                    st.write(actor_details[i]['name'])
                    st.markdown(f"_{actor_details[i]['character']}_")



