import streamlit as st
import pandas as pd
import numpy as np
import requests
import pickle
import time
from send_email import send_email
from datetime import datetime

st.set_page_config(layout="wide", page_title='The Movie Recommender')

if 'movie_index' not in st.session_state:
    st.session_state['movie_index'] = 101

st.sidebar.title("The Movie Recommender.")
with st.sidebar.expander("About"):
    st.write(f"The Movie Recommender uses cosine similarity to suggest "
             f"movies based on user input. The system "
             f"is built using TMDB's 5000 movie dataset. Additional "
             f"information is "
             f"retrieved from TMDB's API."
             f" This project was initiated for a course at my university"
             f" and is still a work in progress. If you would like to give"
             f" feedback or contribute, the source code and documentation "
             f"for the project can be found "
             f"[here](https://github.com/YohanV1/TheMovieRecommender)."
             f" If you have any suggestions or questions, "
             f"please don't hesitate to reach out.")


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


def fetch_reviews(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?" \
          f"api_key=433ff6eeee0036e8693c029787f184c5&language=en-US&page=1"
    data = requests.get(url)
    data = data.json()
    text = data['results']
    review_details = []
    for reviews in text:
        d = {'author': reviews['author'],
             'author_path': reviews['author_details']['avatar_path'],
             'rating': reviews['author_details']['rating'],
             'content': reviews['content'],
             'review_date': reviews['created_at']}
        review_details.append(d)
    return review_details


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
        recommended_movies_summaries.append(' '
                                            .join(movies.iloc[i[0]].overview))
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies_ids, recommended_movies, \
        recommended_movie_posters, \
        recommended_movies_summaries


@st.cache_resource
def load_data():
    movies = pd.read_pickle('models/movies.pkl')
    movies_data = pd.read_pickle('models/movies_data.pkl')
    similarity = pd.read_pickle('models/similarity.pkl')
    return movies, movies_data, similarity


movies, movies_data, similarity = load_data()
titles = list(movies['title'])

st.title('The Movie Recommender.')

option = st.selectbox('Select a movie.'
                      '', titles, index=st.session_state['movie_index'])

if titles.index(option) != st.session_state['movie_index']:
    st.session_state['movie_index'] = titles.index(option)
    st.experimental_rerun()

movie_id = movies.iloc[st.session_state['movie_index']].id
movie_details = movies_data[movies_data['id'] == movie_id]

release_date = \
    movie_details['release_date'].values[
        0].replace('-', '/')
production_area = movie_details[
    'production_countries'].values[
    0]
genres = movie_details['genres'].values[
    0]
runtime = int(
    movie_details['runtime'].values[0])

crew = movie_details['crew'].values[0]
crew = crew[0:4]
l_crew = len(crew)

col1, col2, ecol1 = st.columns([0.9, 1.3, 0.3])

with col1:
    st.image(fetch_poster(movie_id), width=325)
with col2:
    st.header(option)
    text = f"{release_date} ({production_area[17:19]}) • " \
           f"{', '.join(genres)} • {runtime // 60}h {runtime % 60}m"
    st.write(text)

    st.success(
        f"Rating: {(movie_details['vote_average'].values[0] + 0.6).round(1)}"
        f" ({movie_details['vote_count'].values[0]} votes)")

    if not pd.isna(
            movie_details['tagline'].values[
                0]):
        st.markdown(
            f"_{movie_details['tagline'].values[0]}_")

    st.subheader("Overview")
    text = movies[movies['id'] == movie_id]['overview'].values[0]
    if len(text) > 0:
        text = ' '.join(text)
        st.write(text)
    else:
        st.write("Overview unavailable.")

    col1a, col1b, col1c, col1d = st.columns(4)

    if l_crew >= 1:
        with col1a:
            st.markdown(
                f"**{list(crew[0].values())[0]}**  "
                f"\n{list(crew[0].keys())[0]}")

    if l_crew >= 2:
        with col1b:
            st.markdown(
                f"**{list(crew[1].values())[0]}**  "
                f"\n{list(crew[1].keys())[0]}")

    if l_crew >= 3:
        with col1c:
            st.markdown(
                f"**{list(crew[2].values())[0]}**  "
                f"\n{list(crew[2].keys())[0]}")

    if l_crew >= 4:
        with col1d:
            st.markdown(
                f"**{list(crew[3].values())[0]}**  "
                f"\n{list(crew[3].keys())[0]}")

with st.spinner(text='Loading actors...'):
    actors = movie_details['cast'].values[0]
    actors = actors[0:8]
    l_actors = len(actors)
    actor_details = []
    for i in range(l_actors):
        d = {'character': actors[i]['character'],
             'image': fetch_actor_image(actors[i]['id']),
             'name': actors[i]['name']}
        actor_details.append(d)
    time.sleep(1)

st.markdown('##')
st.subheader("Top billed cast.")
st.markdown('######')

if l_actors > 0:
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
else:
    st.write("Actor details unavailable.")

with st.spinner(text='Loading recommendations...'):
    ids, names, posters, summaries = recommend(option)
    time.sleep(0.01)

st.markdown('##')
st.subheader('Movies you might like.')
st.markdown('######')

col1, ecol1, col2, ecol2, col3 = st.columns([1.5, 0.5, 1.5, 0.5, 1.5])

with col1:
    if st.button(names[0], key=1):
        st.session_state['movie_index'] = titles.index(names[0])
        st.experimental_rerun()
    st.image(posters[0], width=250)
    st.write(
        f"Rating: {(movies_data[movies_data['id'] == ids[0]]['vote_average'].values[0] + 0.6).round(1)}")
    st.caption(f'{summaries[0][:200]}...')

with col2:
    if st.button(names[1], key=2):
        st.session_state['movie_index'] = titles.index(names[1])
        st.experimental_rerun()
    st.image(posters[1], width=250)
    st.write(
        f"Rating: {(movies_data[movies_data['id'] == ids[1]]['vote_average'].values[0] + 0.6).round(1)}")
    st.caption(f'{summaries[1][:200]}...')

with col3:
    if st.button(names[2], key=3):
        st.session_state['movie_index'] = titles.index(names[2])
        st.experimental_rerun()
    st.image(posters[2], width=250)
    st.write(
        f"Rating: {(movies_data[movies_data['id'] == ids[2]]['vote_average'].values[0] + 0.6).round(1)}")
    st.caption(f'{summaries[2][:200]}...')

col4, ecol3, col5, ecol4, col6 = st.columns([1.5, 0.5, 1.5, 0.5, 1.5])

with col4:
    if st.button(names[3], key=4):
        st.session_state['movie_index'] = titles.index(names[3])
        st.experimental_rerun()
    st.image(posters[3], width=250)
    st.write(
        f"Rating: {(movies_data[movies_data['id'] == ids[3]]['vote_average'].values[0] + 0.6).round(1)}")
    st.caption(f'{summaries[3][:200]}...')

with col5:
    if st.button(names[4], key=5):
        st.session_state['movie_index'] = titles.index(names[4])
        st.experimental_rerun()
    st.image(posters[4], width=250)
    st.write(
        f"Rating: {(movies_data[movies_data['id'] == ids[4]]['vote_average'].values[0] + 0.6).round(1)}")
    st.caption(f'{summaries[4][:200]}...')

with col6:
    if st.button(names[5], key=6):
        st.session_state['movie_index'] = titles.index(names[5])
        st.experimental_rerun()
    st.image(posters[5], width=250)
    st.write(
        f"Rating: {(movies_data[movies_data['id'] == ids[5]]['vote_average'].values[0] + 0.6).round(1)}")
    st.caption(f'{summaries[5][:200]}...')

col7, ecol5, col8, ecol6, col9 = st.columns([1.5, 0.5, 1.5, 0.5, 1.5])

with col7:
    if st.button(names[6], key=7):
        st.session_state['movie_index'] = titles.index(names[6])
        st.experimental_rerun()
    st.image(posters[6], width=250)
    st.write(
        f"Rating: {(movies_data[movies_data['id'] == ids[6]]['vote_average'].values[0] + 0.6).round(1)}")
    st.caption(f'{summaries[6][:200]}...')

with col8:
    if st.button(names[7], key=8):
        st.session_state['movie_index'] = titles.index(names[7])
        st.experimental_rerun()
    st.image(posters[7], width=250)
    st.write(
        f"Rating: {(movies_data[movies_data['id'] == ids[7]]['vote_average'].values[0] + 0.6).round(1)}")
    st.caption(f'{summaries[7][:200]}...')

with col9:
    if st.button(names[8], key=9):
        st.session_state['movie_index'] = titles.index(names[8])
        st.experimental_rerun()
    st.image(posters[8], width=250)
    st.write(
        f"Rating: {(movies_data[movies_data['id'] == ids[8]]['vote_average'].values[0] + 0.6).round(1)}")
    st.caption(f'{summaries[8][:200]}...')

with st.spinner("Loading reviews..."):
    reviews = fetch_reviews(movie_id)
    time.sleep(0.01)

st.markdown('##')
st.subheader("Reviews.")
st.markdown('######')

if len(reviews) != 0:
    reviews = reviews[:10]

    date_str = reviews[0]['review_date'][0:10]
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')

    new_date_str = date_obj.strftime('%B %d, %Y')

    with st.container():
        col, cole = st.columns([10, 1])
        with col:
            st.write(f"#### **A review by {reviews[0]['author']}** "
                     f"{'- ' + str(reviews[0]['rating']) + '/10' if reviews[0]['rating'] is not None else ''}  \n"
                     f"###### Written by {reviews[0]['author']} on {new_date_str}",
                     unsafe_allow_html=True)
            st.caption(f"{reviews[0]['content']}")

    button_placeholder = st.empty()
    if button_placeholder.button("Load more reviews."):
        button_placeholder.empty()
        for review in reviews[1:]:
            date_str = review['review_date'][0:10]
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            new_date_str = date_obj.strftime('%B %d, %Y')
            with st.container():
                col1, col1e = st.columns([10, 1])
                with col1:
                    st.write(
                        f"#### **A review by {review['author']}** "
                        f"{'- ' + str(review['rating']) + '/10' if review['rating'] is not None else ''}  \n"
                        f"###### Written by {review['author']} on {new_date_str}",
                        unsafe_allow_html=True)
                    st.caption(f"{review['content']}")
        button_placeholder2 = st.empty()
        if button_placeholder2.button("Show less."):
            button_placeholder2.empty()
            st.experimental_rerun()
else:
    st.write("Reviews for this movie are currently unavailable.")

st.markdown('##')
st.subheader("Watched this movie? Leave a rating and a review.")
st.markdown('######')

with st.form(key="review_form", clear_on_submit=True):
    user_name = st.text_input("Your name")
    user_email = st.text_input("Your email address")
    rating = st.slider('Rating', 0.0, 10.0, 5.0, 0.5)
    message = st.text_area("Your review")
    subject = f"New Review from {user_name}"
    text = f"From: {user_email}\nUsername - {user_name}\nMovie - " \
           f"{option}\nRating - {rating}\nReview - {message}"

    button = st.form_submit_button("Submit")
    if button:
        send_email(text, subject)
        st.info("Your review was submitted successfully.")

st.markdown("#")

icol1, iecol, icol2, iecol1, icol3 = st.columns([1.5, 0.5, 1.5, 0.5, 1.5])

with icol1:
    st.info(icon="💡", body="LinkedIn: [yohanvinu](https://www.linkedin.com/"
            "in/yohanvinu/)")

with icol2:
    st.info(icon="💻" , body="GitHub: [YohanV1](https://github.com/YohanV1)")

with icol3:
    st.info(icon="🧠", body="Data: [TMDB](https://www.kaggle.com/datasets/tmdb/"
            "tmdb-movie-metadata)")
