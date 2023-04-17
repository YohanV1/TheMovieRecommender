import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer


def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L


def convert_actors(obj):
    L = []
    c=0
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


# def stem(text):
#     y = []
#     for i in text.split():
#         y.append(ps.stem(i))
#     return " ".join(y)


def recommend(movie):
    movie_index = data[data['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True,
                         key=lambda x: x[1])

    res = []
    for i in movies_list[1:7]:
        res.append(data.iloc[i[0]].title)
    return res


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

# ps = PorterStemmer()
# data['tags'] = data['tags'].apply(stem)
similarity = cosine_similarity(vectors)

titles = list(data['title'])


