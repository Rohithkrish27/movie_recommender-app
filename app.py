import streamlit as st
import pickle
import requests
import pandas as pd

def render_movie_column(col, name, poster, query):
    with col:
        st.text(name)
        st.image(poster)
        url = f'https://www.google.com/search?q={query}'
        button_html = f'''
                <a href="{url}" target="_blank">
                    <button style="background-color: transparent; border: 2px solid red; color: red; 
                                   padding: 10px 24px; text-align: center; text-decoration: none; 
                                   display: inline-block; font-size: 14px; margin: 4px 2px; 
                                   cursor: pointer; border-radius: 4px;">
                        Learn more
                    </button>
                </a>
            '''
        st.markdown(button_html, unsafe_allow_html=True)
def poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=5717a777d513706fe4f1b89f31d08544&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index=movies[movies['title'] == movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(poster(movie_id))
    return recommended_movies,recommended_movies_poster

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies = pd.DataFrame(movies_dict)
st.title("Movie Recommender")
selected_movie_name = st.selectbox('Choose a movie:',movies['title'].values)
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    url = 'https://www.google.com/search?q=avatar'
    col1, col2, col3, col4, col5 = st.columns(5)
    render_movie_column(col1, names[0], posters[0], names[0] + " movie")
    render_movie_column(col2, names[1], posters[1], names[1] + " movie")
    render_movie_column(col3, names[2], posters[2], names[2] + " movie")
    render_movie_column(col4, names[3], posters[3], names[3] + " movie")
    render_movie_column(col5, names[4], posters[4], names[4] + " movie")


