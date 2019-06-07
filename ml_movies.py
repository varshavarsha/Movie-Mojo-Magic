import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler 
from sklearn.linear_model import LogisticRegression
import pickle


movie_data_final = pd.read_csv("dbs/Movie_Data_Final.csv")

mlone = movie_data_final[["Good", "Runtime in Min", "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", 
            "Documentary", "Drama", "Family", "Fantasy", "Film Noir", "History", "Horror",
            "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Short", "Sport", "Superhero", 
            "Thriller", "War", "Western","Title Compound Sentiment"]].dropna()

mlone = mlone.reset_index(drop=True)

X = mlone[["Runtime in Min", "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", 
            "Documentary", "Drama", "Family", "Fantasy", "Film Noir", "History", "Horror",
            "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Short", "Sport", "Superhero", 
            "Thriller", "War", "Western", "Title Compound Sentiment"]]
y = mlone[["Good"]].values.reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

X_scaler = StandardScaler().fit(X_train)
y_scaler = StandardScaler().fit(y_train)

X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)
y_train_scaled = y_scaler.transform(y_train)
y_test_scaled = y_scaler.transform(y_test)

classifier = LogisticRegression(penalty='l1').fit(X_train, y_train)

print(f"Training Data Score: {classifier.score(X_train, y_train)}")
print(f"Testing Data Score: {classifier.score(X_test, y_test)}")

pickle.dump(classifier, open("finalized_model.pkl", "wb"))


loaded_model = pickle.load(open("finalized_model.pkl", "rb"))
result = loaded_model.score(X_test, y_test)
print(result)


mltwo = movie_data_final[["Good", "Runtime in Min", "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", 
            "Documentary", "Drama", "Family", "Fantasy", "Film Noir", "History", "Horror",
            "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Short", "Sport", "Superhero", 
            "Thriller", "War", "Western", "Actors Avg Total Gross", "Actors Avg Number of Movies", 
            "Actors Avg Best Picture Gross", "Director Total Gross", "Director Number of Movies", 
            "Director Best Picture Gross","Title Compound Sentiment"]].dropna()

mltwo = mltwo.reset_index(drop=True)

X = mltwo[["Runtime in Min", "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", 
            "Documentary", "Drama", "Family", "Fantasy", "Film Noir", "History", "Horror",
            "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Short", "Sport", "Superhero", 
            "Thriller", "War", "Western", "Actors Avg Total Gross", "Actors Avg Number of Movies", 
            "Actors Avg Best Picture Gross", "Director Total Gross", "Director Number of Movies", 
            "Director Best Picture Gross","Title Compound Sentiment"]]
            
y = mltwo[["Good"]].values.reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

X_scaler = StandardScaler().fit(X_train)
y_scaler = StandardScaler().fit(y_train)

X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)
y_train_scaled = y_scaler.transform(y_train)
y_test_scaled = y_scaler.transform(y_test)

classifier = LogisticRegression(penalty='l1').fit(X_train, y_train)

print(f"Training Data Score: {classifier.score(X_train, y_train)}")
print(f"Testing Data Score: {classifier.score(X_test, y_test)}")

pickle.dump(classifier, open("finalized_model2.pkl", "wb"))


loaded_model = pickle.load(open("finalized_model2.pkl", "rb"))
result = loaded_model.score(X_test, y_test)
print(result)