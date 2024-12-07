import pandas as pd
import os
import json
import logging 

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