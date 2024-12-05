import numpy as np
import pandas as pd
from numpy.linalg import norm
import argparse

# MAKING ALL VARIABLES NUMERIC
def convert_duration(duration):
    hours, minutes = 0, 0
    if 'h' in duration:
        hours = int(duration.split('h')[0])
        duration = duration.split('h')[1]
    if 'm' in duration:
        minutes = int(duration.split('m')[0])
    return hours * 60 + minutes

# converting number of ratings to numeric
def convert_ratings(ratings):
    if pd.isna(ratings) or ratings.lower() == 'nan':
        return 0
    if 'K' in ratings:
        return int(float(ratings.replace('K', '')) * 1000)
    if 'M' in ratings:
        return int(float(ratings.replace('M', '')) * 1000000)
    return int(ratings)

def cosine_sim(movie1, movie2):
    """takes in two movies in the form of numpy array and returns the cosine similarity score"""
    movie1 = movie1.flatten()
    movie2 = movie2.flatten()
    cosine = np.dot(movie1,movie2)/(norm(movie1)*norm(movie2))
    print("Cosine Similarity:", cosine)
    
def cosine_max(movie_index):
    movie = movies.iloc[movie_index:movie_index+1].drop(columns=['Title']).to_numpy().flatten()
    similarities = []
        
    for i in range(len(movies)):
        if i != movie_index:
            other_movie = movies.iloc[i:i+1].drop(columns=['Title']).to_numpy().flatten()
            cosine = np.dot(movie, other_movie) / (norm(movie) * norm(other_movie))
            similarities.append((i, cosine))
        
    similarities.sort(key=lambda x: x[1], reverse=True)
    titles = convert_to_title(similarities[:5])
    print(titles)
    return similarities[:5]

def convert_to_title(sims):
    titles = []
    for index, _ in sims:
        titles.append(movies.iloc[index]['Title'])
    return titles
    
# Reading in CSV
movies = pd.read_csv("output_file.csv")
# Converting duration to numeric
movies['Duration'] = movies['Duration'].astype(str)
movies['Duration'] = movies['Duration'].apply(convert_duration)

# converting MPAA rating to numeric
rating_mapping = {
    'nan': 0,
    'G': 1,
    'PG': 2,
    'PG-13': 3,
    'R': 4,
    'NC-17': 5,
    'Unrated': 6
}
movies['Rated'] = movies['Rated'].map(rating_mapping)
    
movies['Number of Ratings'] = movies['Number of Ratings'].astype(str).fillna('0')
movies['Number of Ratings'] = movies['Number of Ratings'].apply(convert_ratings)

# dropping variables:
columns_to_drop = ['Description', 'Descrption', 'Genre', 'Runtime', 'Director', 'Writer', 'Actors', 'Rating', 'Awards', 'Description']
movies = movies.drop(columns=columns_to_drop)

# filling the missing with zeros
movies = movies.fillna(0)

# normalizing all the variables to 0-1
movie_titles = movies['Title']
movies = movies.drop(columns=['Title']).apply(lambda x: (x - x.min()) / (x.max() - x.min()))
movies['Title'] = movie_titles
    
# Getting movie title from user
parser = argparse.ArgumentParser(description="Movie Title Input")
parser.add_argument("-t", required=True, help="Title of Movie")
args = parser.parse_args()

# finding the index of the title
index = movies[movies['Title'].str.contains(args.t, case=False, na=False)].index[0]
print(movies.iloc[index])
movie_index = index # Define the movie index you want to compare
print(cosine_max(movie_index))