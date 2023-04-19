import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests


def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L


def convert_actors(obj):
    L = []
    c = 0
    for i in ast.literal_eval(obj):
        if c != 5:
            L.append(i['name'])
            c+=1
        else:
            break
    return L


def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L


def fetch_poster(movie_id):
    with open('apikey.txt', 'r') as f:
        your_api_key = f.read().strip()
    url = f"https://api.themoviedb.org/3/movie/{{}}?api_key={your_api_key}&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True,
                         key=lambda x: x[1])[1:10]

    recommended_movies = []
    recommended_movie_posters = []
    recommended_movies_summaries = []

    for i in movies_list:
        # fetch the movie poster
        print(i)
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_summaries.append(' '.join(movies.iloc[i[0]].overview))
        recommended_movie_posters.append(fetch_poster(movie_id))

    print(recommended_movies, recommended_movie_posters)
    return recommended_movies, recommended_movie_posters, \
        recommended_movies_summaries


credits = pd.read_csv('datasets/tmdb_5000_credits.csv')
movies = pd.read_csv('datasets/tmdb_5000_movies.csv')

movies = movies.merge(credits,on='title')

movies = movies[['id', 'title', 'overview', 'genres', 'keywords', 'cast',
                 'crew']]

movies.dropna(inplace=True)

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert_actors)
movies['crew'] = movies['crew'].apply(fetch_director)

movies['overview'] = movies['overview'].apply(lambda x: x.split())

movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "")
                                                     for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "")
                                                         for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "")
                                                 for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "")
                                                 for i in x])

movies['tags'] = movies['overview'] + movies['genres'] + movies['cast'] + \
                 movies['crew']

data = movies[['id', 'title', 'tags']]

data['tags'] = data['tags'].apply(lambda x: " ".join(x))
data['tags'] = data['tags'].apply(lambda x:x.lower())

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(data['tags']).toarray()

similarity = cosine_similarity(vectors)

titles = list(data['title'])


