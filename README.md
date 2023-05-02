# The Movie Recommender - Using Streamlit & Cosine Similarity

![Python version](https://img.shields.io/badge/Python-3.11.0-lightgrey) ![Framework](https://img.shields.io/badge/Framework-Streamlit-blue) ![API](https://img.shields.io/badge/API-TMDB-red) ![License](https://img.shields.io/badge/License-MIT-orange)
![Status](https://img.shields.io/badge/Status-Active-brightgreen) ![Contributions](https://img.shields.io/badge/Contributions-Welcome-green)

This application implements the Streamlit framework for the UI and frontend. The recommendation system works on the concept of cosine similarity, which is a way to measure how similar two movies are to each other based on the features they share, such as genre, cast, and plot. The project utilizes the '[TDMB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv)' from Kaggle, and additional data is fetched from [TMDB's API](https://developers.themoviedb.org/3/getting-started/introduction) to supplement missing or limited information. This project was initiated for a course at my university and is still a work in progress. 

### Features
* An option to search for any movie in the dataset.
* The movie's poster and additional details (release date, genres, rating, overview etc.) are displayed.
* Cast images are displayed along with their names and the characters they play in the movie.
* The posters of 9 recommended movies are displayed along with their ratings and brief overviews. Each movie's recommendations and information can be accessed by clicking on a movie's title.
* Reviews from TMDB's API can be viewed.
* A review form that allows a user to give their view on the movie is available. For now, this data is not stored anywhere and is only sent via a mailer.
* A contact us page is available if a user wants to give their feedback. This data is also sent via a mailer.

### How it Works
Cosine similarity is a technique used to calculate the similarity between two vectors or sets of data. In the case of a movie recommender system, we use cosine similarity to calculate the similarity between two movies based on their features. In order to use cosine similarity, we first need to represent each movie as a vector of features. For example, we might represent each movie using a vector of genre tags, where each element of the vector represents a different genre and has a value of 1 if the movie belongs to that genre, and 0 otherwise.

![Cosine similarity between two vectors](https://storage.googleapis.com/lds-media/images/cosine-similarity-vectors.original.jpg)

Once we have represented each movie as a vector, we can calculate the cosine similarity between two movies by taking the [dot product](https://www.geeksforgeeks.org/cosine-similarity/) of their vectors and dividing it by the product of their magnitudes. 

The resulting cosine similarity value will range between -1 and 1, where -1 indicates that the two movies are completely dissimilar, 0 indicates that they have no similarity, and 1 indicates that they are identical.

To recommend movies based on user input, we can calculate the cosine similarity between the input movie and all other movies in the dataset, and then recommend the top 9 most similar movies based on cosine similarity. This approach assumes that movies with similar features are likely to be enjoyed by the same users, and can provide a personalized recommendation to the user based on their input.

## Getting Started

### Prerequisites
* Python 3.6+
* Python modules from ```requirements.txt```

### Usage
1. Clone the repository via ```https://github.com/YohanV1/TheMovieRecommender.git``` or download the repository. 

   > Note: The repository might take a little longer to clone as the datasets are relatively large, and the 'similarity.pkl' file has to be fetched from git LFS (Large File Storage).
2. Install the dependencies with ```pip install -r requirements.txt```.
3. An API key is included with this project. If you'd like your own API key, you can get one from [TMDB's API](https://developers.themoviedb.org/3/getting-started/introduction). Replace everything from ```api_key=``` till ```&language``` with your own key on lines 33, 43, and 53 of 'Recommend_Movies..py'.
4. Run the application with ```streamlit run Recommend_Movies..py```. The application should launch locally on your web browser.

### Developer Usage
1. The `model_testing.ipynb` file is where data cleaning, preprocessing, and feature engineering is carried out. The similarity scores and dataframes are pickled into '.pkl' files for use in the application. If you'd like to tweak this file, you might have to install scikit-learn with `pip install scikit-learn`. Scikit-learn usually comes with Anaconda, if that's what you'll be using.
2. The `Recommend_Movies..py` file is the UI and frontend of the application. The previously pickled data is simply loaded, and additional information is fetched via the API. 
3. The `send_email.py` is the mailer used in the application to recieve feedback and user reviews. 

## Contributions
If you found an issue or would like to submit an improvement to the project, please submit an issue in the issues tab above. If you would like to submit a PR, please reference the issue you created.

Contributions to this project are welcome. If you would like to contribute, please fork the repository and submit a pull request.

## Known Issues
* TMDB's API should work for most people but some ISPs have blocked the domain. In such a case, you can use a VPN or another network.
* Actor data is scattered across it's container if there is not enough actor information for the particular movie.

## License
This project is licensed under the MIT License. See the [LICENSE file](https://github.com/YohanV1/TheMovieRecommender/blob/main/LICENSE) for more information.

⭐ this repository if you find it useful!
