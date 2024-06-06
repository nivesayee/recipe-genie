import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

nltk.download('stopwords')
nltk.download('punkt')
stopwords = set(stopwords.words('english'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
stemmer = PorterStemmer()

# Read the Recipe file
df = pd.read_csv("../../data/raw/recipes.csv")


# Preprocessing functions
def preprocess_ingredients(ingredients_str):
    ingredients_list = ast.literal_eval(ingredients_str)
    preprocessed = set()
    measurements = ['tbsp', 'tablespoon', 'tsp', 'teaspoon', 'oz', 'ounc', 'fl oz',
                    'fluid ounc', 'c', 'cup', 'qt', 'quart', 'pt', 'pint',
                    'gal', 'gallon', 'lb', 'pound', 'ml', 'millilitre', 'g', 'gram',
                    'kg', 'kilogram', 'l', 'liter'
                    ]
    unwanted_words = ['chop', 'piec', 'cube', 'like', 'grate', 'slice', 'thinli', 'drizzl', 'mild', 'delallo', 'castelvetrano', 'splash', 'shake', 'tast',
                      'clove', 'bunch', 'cook', 'inch', 'knob', 'fresh', 'pack', 'one', 'two', 'stalk', 'half', 'san', 'marzano',
                      'dri', 'spici', 'raw', 'jumbo', 'minc', 'larg', 'beaten', 'mediums', 'head', 'low', 'sodium', 'frozen',
                      'shred', 'jar', 'favorit', 'small', 'box', 'uncook', 'contain', 'medium', 'heavi', 'english', 'smoke',
                      'sprig', 'dice', 'petit', 'batch', 'air', 'fryer', 'serv', 'block', 'extra', 'firm', 'fine', 'ish',
                      'refriger', 'ground', 'thi', 'chunk', 'homemad', 'option', 'top', 'packag', 'individu', 'bundl', 'closer',
                      'leav','melt','readytoserv','premad','bag','zest','pinch','halv','abov','absolut','access',
                      'add','addin','addit','also','ancient','asianinspir','barefoot','basic','becaus','best','big','bit','bittersweet',
                      'blend','bold','bought','brand','buy','case','caught','chef','chihuahua','club','coat','cool','corner','could',
                      'crack','creation','cupboard','cut','dare','dark','dinner','either','els','everyth','extrasharp','eyebal','farm'
                      ,'fashion','freshli','friendli','garnish','good','hard','happi','heirloom','hollow','huge','ideal','id','idea',
                      'ingredi','ive','kind','king','koreanstyl','lake','land','layer','le','leftov','life','light','lightli',
                      'littl','loos','lot','love','lump','made','magic','make','market','mash','massag','meal','mediumlarg','mediumrip',
                      'mini','miniatur','minut','mix','mixin','mm','montreal','part','nice','never','note','store','storebought',
                      'random','shortcut','similar','yum','yummi','wan','want','use','thick']
    for ingredient in ingredients_list:
        ingredient = re.sub(r'\(.*\)', '', ingredient).strip()
        ingredient = ingredient.split(',')[0].lower()
        ingredient = re.sub(r'[^a-z\s]+', '', ingredient).strip()
        ingredient_tokens = word_tokenize(ingredient)
        stemmed_tokens = [stemmer.stem(token) for token in ingredient_tokens]
        filtered_tokens = [token for token in stemmed_tokens if token not in stopwords and token not in measurements and token not in unwanted_words]
        cleansed_ingredient = ' '.join(filtered_tokens)
        if 'oil' not in cleansed_ingredient and 'salt' not in cleansed_ingredient and 'water' not in cleansed_ingredient\
                and cleansed_ingredient != '':
            preprocessed.add(cleansed_ingredient)
    return preprocessed




df['ingredients'] = df['ingredients'].apply(preprocess_ingredients).apply(lambda x: ' '.join(x))

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['ingredients'])
#print(vectorizer.get_feature_names_out())

# Convert the TF-IDF matrix to a DataFrame for better visualization
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

with open('../../data/processed/tfidf_matrix.pkl','wb') as file:
    pickle.dump(tfidf_matrix, file)

with open('../../data/processed/vectorizer.pkl','wb') as file:
    pickle.dump(vectorizer, file)

print("TF-IDF matrix and vectorizer saved to 'tfidf_matrix.pkl' and 'tfidf_vectorizer.pkl'.")



