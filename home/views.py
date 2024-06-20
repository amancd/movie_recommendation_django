from django.shortcuts import render

import joblib

new_df = joblib.load('static/new_df.pkl')
count_vectorizer = joblib.load('static/count_vectorizer.pkl')
similarity = joblib.load('static/similarity.pkl')

def recommend(movie):
    try:
        movie_index = new_df[new_df['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        for i in movies_list:
            recommended_movies.append(new_df.iloc[i[0]].title)

        return recommended_movies
    except IndexError:
        return ["Movie not found in database"]

def index(request):
    recommendations = []
    if request.method == "POST":
        movie_name = str(request.POST.get("movie_name"))
        recommendations = recommend(movie_name)
    
    return render(request, "index.html", {"recommendations": recommendations})