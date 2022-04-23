import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(layout="wide")


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{'
                            '}?api_key=027c6c66285e937cd48dc4bd438e9425&language=en-US'.format(movie_id))
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']  # complete poster path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)  # to print movies title / movies names
        # fetching movies posters using API from themoviedb.org
        recommended_movies_posters.append(fetch_poster(movie_id))  # appending movies posters to fetch_poster function
    return recommended_movies, recommended_movies_posters


similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

selected_movies_name = st.selectbox('Which Movie would you like to watch', movies['title'].values)

if st.button('Recommend'):
    recommended_movies_names, recommended_movies_posters = recommend(selected_movies_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies_names[0])
        st.image(recommended_movies_posters[0], width=150)
    with col2:
        st.text(recommended_movies_names[1])
        st.image(recommended_movies_posters[1], width=150)
    with col3:
        st.text(recommended_movies_names[2])
        st.image(recommended_movies_posters[2], width=150)
    with col4:
        st.text(recommended_movies_names[3])
        st.image(recommended_movies_posters[3], width=150)
    with col5:
        st.text(recommended_movies_names[4])
        st.image(recommended_movies_posters[4], width=150)
