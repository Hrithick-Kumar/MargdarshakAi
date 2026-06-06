import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier

os.makedirs("models", exist_ok=True)

# TEXT MODEL

stream_data = pd.read_csv("Stream1.csv")

vectorizer = CountVectorizer()

X_text = vectorizer.fit_transform(
    stream_data["word"]
)

text_model = MultinomialNB()

text_model.fit(
    X_text,
    stream_data["stream"]
)

joblib.dump(
    vectorizer,
    "models/vectorizer.pkl"
)

joblib.dump(
    text_model,
    "models/text_model.pkl"
)

# PREFERENCE MODEL

pref_data = pd.read_csv(
    "Preference.csv"
)

pref_X = pref_data[
[
"Maths_Interest",
"Science_Interest",
"Business_Interest",
"Creativity",
"Stress_Handling_Level"
]
]

pref_y = pref_data["Stream"]

pref_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

pref_model.fit(
    pref_X,
    pref_y
)

joblib.dump(
    pref_model,
    "models/pref_model.pkl"
)

# MARKS MODEL

marks_data = pd.read_csv(
    "StudentMark.csv"
)

marks_X = marks_data[
[
"Maths",
"Science",
"Social Science",
"English"
]
]

marks_y = marks_data["Stream"]

marks_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

marks_model.fit(
    marks_X,
    marks_y
)

joblib.dump(
    marks_model,
    "models/marks_model.pkl"
)

print("Models Saved")
