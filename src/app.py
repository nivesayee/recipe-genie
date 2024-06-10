from flask import Flask, render_template, request
import pickle
from src.utils.preprocess import preprocess_user_ingredients
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

app = Flask(__name__)

# Load all the pickle files
with open("../data/processed/recipes.pkl",'rb') as file:
   recipe_df = pickle.load(file)

with open("../data/processed/tfidf_matrix.pkl",'rb') as file:
    tfidf_matrix = pickle.load(file)

with open("../data/processed/vectorizer.pkl",'rb') as file:
   vectorizer = pickle.load(file)


@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        user_ingredients = request.form['ingredients']
        preprocessed_user_ingredients = preprocess_user_ingredients(user_ingredients)
        user_ingredients_vector = vectorizer.transform([preprocessed_user_ingredients])
        similarity_scores = cosine_similarity(user_ingredients_vector, tfidf_matrix)
        top_indices = similarity_scores.argsort()[0][-5:][::-1]
        recommended_recipes = df.iloc[top_indices]
        return render_template('results.html',recipes=recommended_recipes)
    return render_template('index.html')


if __name__=='__main__':
    app.run(debug=True)