import streamlit as st
import pickle
import pandas as pd
import requests
import time



TMDB_API_KEY = "dc5fbf7476a888c63f13713fe9f6a17c"
OMDB_API_KEY = "fd2adf10"

def fetch_poster(imdb_id):
    # 1️⃣ First try TMDB
    try:
        tmdb_url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id"
        response = requests.get(tmdb_url)
        data = response.json()

        if data.get("movie_results"):
            poster_path = data["movie_results"][0].get("poster_path")
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception as e:
        print("TMDB fetch error:", e)

    # 2️⃣ If TMDB fails → try OMDb
    try:
        omdb_url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
        response = requests.get(omdb_url)
        data = response.json()

        poster_url = data.get("Poster")
        if poster_url and poster_url != "N/A":
            return poster_url
    except Exception as e:
        print("OMDb fetch error:", e)

    # 3️⃣ Final fallback → placeholder image
    return "https://via.placeholder.com/300x450.png?text=No+Poster+Available"





def recommend(movie):
    movie_index = movies[movies['original_title'] == movie].index[0]
    proper_index=movie_index.item()
    distance = similarity[proper_index]

    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters= []

    for i in movies_list:


        recommend_movies.append(movies.iloc[i[0]].original_title)
        id1= movies.iloc[i[0]].imdb_id

        # fetch poster
        recommend_movies_posters.append(fetch_poster(id1))
    return recommend_movies,recommend_movies_posters


movies_dict = pickle.load(open('movies_dict_final.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity= pickle.load(open('similarity_final.pkl','rb'))

st.title('Movie Recommender System')

movie_selected = st.selectbox(
'Which recent movie you Watched recently, want any recommendations........',
movies['original_title'].values
)


if st.button("Recommend"):
    names, posters = recommend(movie_selected)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])
