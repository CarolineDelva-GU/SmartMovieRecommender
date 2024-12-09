import pandas as pd
import os
import json
import logging 
from smartmovierecommender.calculation.cosine_sim import convert_duration, convert_ratings
from sklearn.metrics.pairwise import cosine_similarity

def movie_combiner(output_path, output_file):

    #output_path = "../../../output_data/"
    output_path = output_path
    all_files = [f for f in os.listdir(output_path) if f.endswith('.csv')]
    genre_df = pd.concat([pd.read_csv(os.path.join(output_path, file)) for file in all_files], ignore_index=True)
        
    movie_list = []
    for filename in os.listdir('data'):
        if not filename.endswith('.json'):
            logging.info(f"Skipping non-JSON file: {filename}")
            continue
        input_file = os.path.join('Data', filename)
            
        with open(input_file, 'r', encoding='Windows-1252') as file:
            movie_data = json.load(file)
            movie_list.append(pd.DataFrame(movie_data))
    movie_df = pd.concat(movie_list, ignore_index=True)

    # logging.info the unique
    logging.info(len(genre_df))
    logging.info(genre_df['movie'].nunique())
    logging.info(len(movie_df))
    logging.info(movie_df['Title'].nunique())

    # changing the movie variable name
    genre_df.rename(columns={'movie': 'Title'}, inplace=True)

    # merging
    merged_df = pd.merge(movie_df, genre_df, on='Title', how='inner')
    logging.info(merged_df.head(10))
    logging.info(len(merged_df))

    # keeping only unique titles
    merged_df = merged_df.drop_duplicates(subset=['Title'], keep='first')
    logging.info(merged_df.head(10))
    logging.info(len(merged_df))
    merged_df.to_csv(output_file, index=False)
    
    

    #merged_df.to_csv('output_file.csv', index=False)

#this cleans the columns to normalize it to do the cosine similaritiy 
def preprocess_movies(filepath):
        movies = pd.read_csv(filepath)
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
        print("Data preprocessing completed.")
        return movies



def get_movie_rec(movies,movie_title,top_n=5):
     
        target_movie = movies[movies['Title'] == movie_title]

        features = movies.drop(columns=['Title'])
        target_features = target_movie.drop(columns=['Title'])

            # Compute cosine similarities
        similarities = cosine_similarity(target_features, features)[0]

        # Get the top 5 similar movies
        # Get top N recommendations
        movies['Similarity'] = similarities
        recommendations = movies[movies['Title'] != movie_title].sort_values(
                by='Similarity', ascending=False).head(5)
        return recommendations[['Title', 'Similarity']]

