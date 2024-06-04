import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import ast

nltk.download('stopwords')
nltk.download('wordnet')
stopwords = set(stopwords.words('english'))
pd.set_option('display.max_colwidth', None)

# Read the Recipe file
df = pd.read_csv("../../data/raw/recipes - Copy.csv")


# Preprocessing functions
def preprocess_ingredients(ingredients_str):
    ingredients_list = ast.literal_eval(ingredients_str)
    preprocessed = []
    measurements = ['tbsp', 'tablespoon', 'tsp', 'teaspoon', 'oz', 'ounce', 'fl oz',
                    'fluid ounce', 'c', 'cup', 'qt', 'quart', 'pt', 'pint',
                    'gal', 'gallon', 'lb', 'pound', 'ml', 'millilitre', 'g', 'gram',
                    'kg', 'kilogram', 'l', 'liter'
                    ]
    unwanted_words = ['chopped', 'piece', 'cubed', 'like', 'grated', 'sliced', 'mild', 'delallo', 'castelvetrano', 'drizzle', 'thinly', 'splash', 'shake', 'taste']
    lemmatizer = WordNetLemmatizer()
    for ingredient in ingredients_list:
        ingredient = re.sub(r'\(.*\)', '', ingredient).strip()
        ingredient = ingredient.split(',')[0].lower()
        ingredient = re.sub(r'[^a-z\s]+', '', ingredient).strip()
        ingredient_tokens = word_tokenize(ingredient)
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in ingredient_tokens]
        filtered_tokens = [token for token in lemmatized_tokens if token not in stopwords and token not in measurements and token not in unwanted_words]
        cleansed_ingredient = ' '.join(filtered_tokens)

        preprocessed.append(cleansed_ingredient)
    return preprocessed




df['ingredients'] = df['ingredients'].apply(preprocess_ingredients)
print(df['ingredients'])






