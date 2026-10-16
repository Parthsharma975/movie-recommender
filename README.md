# 🎬 Movie Recommender System

A content-based movie recommendation web app. Type or select a movie and get **5 similar movies** with their posters.

**🔗 Live Demo:** [https://movie-recommender-gudg.onrender.com](https://movie-recommender-gudg.onrender.com)

> Hosted on Render's free plan, so the first load after inactivity can take about a minute while the server wakes up.

---

## ✨ Features

- Search with autocomplete across ~4,800 movies
- Top 5 similar movie recommendations in one click
- Movie posters fetched live from the TMDB API
- Responsive dark UI built with Bootstrap 5
- Graceful fallback ("Poster Not Found") if a poster can't be loaded

## 🧠 How It Works

1. **Tags creation:** each movie is represented by a single `tags` text field (overview, genres, keywords, cast, crew combined).
2. **Vectorization:** `CountVectorizer` (max 5000 features, English stop words removed) converts the tags into numeric vectors.
3. **Similarity:** cosine similarity is computed between the selected movie and all other movies.
4. **Ranking:** the 5 most similar movies (excluding the movie itself) are returned.
5. **Posters:** poster images are fetched from the TMDB API using each movie's `movie_id`.

The similarity is computed per request, so the app does not need a large precomputed similarity matrix file and stays light enough for free hosting.

## 🛠️ Tech Stack

| Area | Tools |
|------|-------|
| Backend | Python, Flask, Gunicorn |
| ML / Data | Pandas, NumPy, scikit-learn |
| Frontend | HTML, Jinja2, Bootstrap 5 |
| API | TMDB (The Movie Database) |
| Deployment | Render |

## 📁 Project Structure

```
movie-recommender/
├── app.py              # Flask app and recommendation logic
├── movies_dict.pkl     # Movie data (id, title, tags)
├── templates/
│   └── index.html      # Frontend page
├── requirements.txt    # Python dependencies
├── Procfile            # Start command for deployment
└── .python-version     # Python version for Render
```

## 🚀 Run Locally

1. **Clone the repo**
   ```bash
   git clone https://github.com/Parthsharma975/movie-recommender.git
   cd movie-recommender
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get a free TMDB API key** from [themoviedb.org](https://www.themoviedb.org/settings/api) and set it as an environment variable:

   Windows (CMD):
   ```bash
   set TMDB_API_KEY=your_api_key_here
   ```
   Mac / Linux:
   ```bash
   export TMDB_API_KEY=your_api_key_here
   ```

4. **Run the app**
   ```bash
   python app.py
   ```
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## ☁️ Deployment (Render)

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app`
- **Environment variable:** `TMDB_API_KEY`

## 🔮 Future Improvements

- Add filters by genre and release year
- Show movie overview, rating and cast on a details page
- Hybrid recommendations combining content and user ratings
- Cache poster requests to speed up responses

## 👤 Author

**Parth Sharma**
GitHub: [@Parthsharma975](https://github.com/Parthsharma975)

---

*This product uses the TMDB API but is not endorsed or certified by TMDB.*
