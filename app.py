import streamlit as st
import pickle
import difflib

st.markdown(
    """
    <style>
    .sidebar .dropdown-container .dropdown-menu {
        pointer-events: none;
    }
    .sidebar .dropdown-container .dropdown-trigger {
        pointer-events: all;
    }
    .sidebar .dropdown-container:hover .dropdown-menu {
        display: block;
        pointer-events: all;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def movie_recommend(movie_name,category):
    val=df[df.title==movie_name[0]]["index"].values[0]
    movie=df.loc[[int (val)],["title"]].values[0][0]
    genres=df.loc[[int (val)], ["genres"]].values[0][0]
    cast=df.loc[[int (val)], ["cast"]].values[0][0]
    release_date=df.loc[[int (val)], ["release_date"]].values[0][0]
    st.write("Movie Name:",movie)
    st.write("Genre:",genres)
    st.write("Cast:",cast)
    st.write("Release Date:",release_date)
    st.header('Recommendations based on '+category+' :')

    if category=="Genre":
        function=similarity_genres
    elif category=="Favourite Characters":
        function=similarity_cast
    elif category=="Time Zone":
        function=similarity_rel_pop
    else:
        function=similarity_factors

    factors_score=list(enumerate(function[val]))
    count=0
    recommended_movies=[]
    sorted_recomendations=sorted(factors_score,key=lambda x:x[1],reverse=True)
    #print(sorted_recomendations)
    for i in sorted_recomendations:
        index=i[0]
        recommended_movies.append(df[df. index==index] ['title'].values[0])
        count+=1
        if(count>(10)):
            break
    #print(recommended_movies)
    return recommended_movies

df=pickle.load(open("movie_recm.pkl","rb"))
similarity_factors=pickle.load(open("similarity_factors.pkl","rb"))
similarity_genres=pickle.load(open("similarity_genres.pkl","rb"))
similarity_cast=pickle.load(open("similarity_cast.pkl","rb"))
similarity_rel_pop=pickle.load(open("similarity_rel_pop.pkl","rb"))

st.header("Movie Recommendation Engine")
movie=st.text_input("Enter movie name:")
movie_name=difflib.get_close_matches(movie,df["title"])

options = [
    "Recommend Movies by Genre",
    "Recommend Movies by Favorite Characters",
    "Recommend Movies by Time Zone",
    "Recommend Movies by Overall Interest"
]

# Create a dropdown select box
selected_option = st.sidebar.selectbox("Select Recommendation Type", options)
category="Genre"

if selected_option == "Recommend Movies by Genre":
    catergory="Genre"
elif selected_option == "Recommend Movies by Favorite Characters":
    category="Favourite Characters"
elif selected_option == "Recommend Movies by Time Zone":
    category="Time Zone"
elif selected_option == "Recommend Movies by Overall Interest":
    category="Interest"

movie_list=movie_recommend(movie_name,category)
for movie in movie_list:
    st.write("- " + movie)

