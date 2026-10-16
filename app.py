import os
import pickle

import pandas as pd
import requests
from flask import Flask, request, render_template
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. TMDB API key (set as an environment variable, never hard-code it) ---
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")


def fetch_poster(movie_id):
    """Fetch poster URL for a TMDB movie id. Returns '' if anything fails."""
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}",
            params={"api_key": TMDB_API_KEY},
            timeout=5,
        )
        response.raise_for_status()
        poster_path = response.json().get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
    except requests.RequestException:
        pass
    return ""


# --- 2. Load data once at startup ---
# similarity.pkl (185 MB) is no longer needed: vectors are rebuilt from the
# 'tags' column in a second, and similarity is computed per query.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
movies = pd.DataFrame(pickle.load(open(os.path.join(BASE_DIR, "movies_dict.pkl"), "rb")))
vectors = CountVectorizer(max_features=5000, stop_words="english").fit_transform(movies["tags"])


# --- 3. Recommendation logic ---
def recommend(movie_title):
    """Return top 5 similar movies as [(title, poster_url), ...]."""
    matches = movies[movies["title"] == movie_title].index
    if len(matches) == 0:
        return [("Movie not found.", "")] * 5

    idx = matches[0]
    distances = cosine_similarity(vectors[idx], vectors).flatten()
    top = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]

    return [
        (movies.iloc[i].title, fetch_poster(movies.iloc[i].movie_id))
        for i, _ in top
    ]


# --- 4. Flask Application Setup ---
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Get the list of all movie titles for the dropdown menu
    movie_titles = movies['title'].values.tolist()
    
    recommendation_data = None
    selected_movie = None
    
    if request.method == 'POST':
        # --- Handle Form Submission ---
        # Get the selected movie name from the form input named 'movie_name'
        selected_movie = request.form.get('movie_name')
        
        if selected_movie:
            # Get recommendations as a list of tuples: [(name1, poster1), (name2, poster2), ...]
            recommendation_data = recommend(selected_movie)

    # Render the index.html template, passing the data it needs
    return render_template(
        'index.html', 
        movie_titles=movie_titles, 
        recommendation_data=recommendation_data,
        selected_movie=selected_movie
    )

if __name__ == "__main__":
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')