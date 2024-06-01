import pandas as pd
import re

# Read the Recipe file
df = pd.read_csv("../../data/raw/recipes.csv")


# Preprocessing functions
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^A-Za-z0-9]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text






