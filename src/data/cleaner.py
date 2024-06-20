import pandas as pd
from src.utils.preprocess import preprocess_ingredients
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)


# Read the Recipe file
df = pd.read_csv("../../data/raw/recipes.csv")
df_original = df.copy(deep=True)

df['ingredients'] = df['ingredients'].apply(preprocess_ingredients)

# Save preprocessed data
df.to_csv("../../data/processed/recipes.csv", index=False)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['ingredients'])

# Convert the TF-IDF matrix to a DataFrame for better visualization
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

with open('../../data/processed/tfidf_matrix.pkl', 'wb') as file:
    pickle.dump(tfidf_matrix, file)

with open('../../data/processed/vectorizer.pkl', 'wb') as file:
    pickle.dump(vectorizer, file)

with open('../../data/processed/recipes.pkl', 'wb') as file:
    pickle.dump(df_original, file)
print("TF-IDF matrix and vectorizer saved to 'tfidf_matrix.pkl' and 'tfidf_vectorizer.pkl'.")

