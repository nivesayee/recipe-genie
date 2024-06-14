from flask import Flask, render_template, request
import pickle
from utils.preprocess import preprocess_user_ingredients
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os


app = Flask(__name__)

# Get the directory of the current Python script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one directory to access the data directory
data_dir = os.path.join(current_dir, "..", "data")

# Load all the pickle files using relative paths
recipes_path = os.path.join(data_dir, "processed", "recipes.pkl")
tfidf_matrix_path = os.path.join(data_dir, "processed", "tfidf_matrix.pkl")
vectorizer_path = os.path.join(data_dir, "processed", "vectorizer.pkl")


with open(recipes_path, 'rb') as file:
   recipe_df = pickle.load(file)

with open(tfidf_matrix_path, 'rb') as file:
    tfidf_matrix = pickle.load(file)

with open(vectorizer_path, 'rb') as file:
   vectorizer = pickle.load(file)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_ingredients = request.form['ingredients']
        preprocessed_user_ingredients = preprocess_user_ingredients(user_ingredients)
        print(preprocessed_user_ingredients)
        user_ingredients_vector = vectorizer.transform([preprocessed_user_ingredients])
        similarity_scores = cosine_similarity(user_ingredients_vector, tfidf_matrix)
        top_indices = similarity_scores.argsort()[0][-5:][::-1]
        recommended_recipes = recipe_df.iloc[top_indices]
        return render_template('results.html', recipes=recommended_recipes)
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
