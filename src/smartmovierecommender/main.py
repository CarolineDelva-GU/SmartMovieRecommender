

import pandas as pd 
import logging 
import argparse
from sklearn.metrics.pairwise import cosine_similarity
#from smartmovierecommender.transformer.gemini_query import process_movies
#from smartmovierecommender.collector.datascraper import scraper 
from smartmovierecommender.utils.combining_data import movie_combiner
from smartmovierecommender.calculation.cosine_sim import convert_duration, convert_ratings, cosine_sim, cosine_max, convert_to_title



# logging.basicConfig(
#     level=logging.INFO,
#     filename='../../../../logs.txt',
#     filemode='w', 
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

#def main(#to_imdb,link_for_scraping, to_scrape, to_gemini, to_cosine_score, movie): 
def main(to_cosine_score, movie_title): 
    # if to_imdb:



    # if to_scrape:
    #     scraper(link_for_scraping)
    
    # movie_combiner("../../output_data/", "../../processed-data/output_file.csv")
    
    # if to_gemini:
    #     process_movies()
        
    if to_cosine_score:   
            # Reading in CSV
        movies = pd.read_csv("processed-data/output_file.csv")
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
            
            # Find the movie in the dataset
        target_movie = movies[movies['Title'] == movie_title]
        if target_movie.empty:
                print(f"Movie '{movie_title}' not found in the dataset.")
                return

        features = movies.drop(columns=['Title'])
        target_features = target_movie.drop(columns=['Title'])

            # Compute cosine similarities
        similarities = cosine_similarity(target_features, features)[0]

            # Get the top 5 similar movies
        movies['Similarity'] = similarities
        recommendations = movies[movies['Title'] != movie_title].sort_values(
                by='Similarity', ascending=False).head(5)

            # Print recommendations
        print("\nTop 5 Recommendations:")
        for i, row in recommendations.iterrows():
                print(f"{row['Title']}")

        # Getting movie title from user
   
            
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Movie_recommender_script")
    #parser.add_argument("-l", "--link", required=True, help="link to scrape")
    #parser.add_argument("-s", "--to_scrape", action="store_true", help="Flag to scrape or not")
    #parser.add_argument("-g", "--to_gemini", action="store_true", help="Flag to gemini score")
    parser.add_argument("-cs", "--to_cosine_score", action="store_true", help="Flag to gemini score")
    parser.add_argument("-t", required=True, help="Title of Movie")
    
    args = parser.parse_args()
    main(
        #link_for_scraping=args.link,
        #to_scrape=args.to_scrape,
        #to_gemini=args.to_gemini,
        to_cosine_score=args.to_cosine_score,
        movie_title=args.t
    )
    
    #main(args.file, args.result, args.scorer, args.evaluate)
    logging.info('Scoring is completed')  
    logging.shutdown()  
    
    # parser = argparse.ArgumentParser(description="Movie Title Input")
    # parser.add_argument("-t", required=True, help="Title of Movie")
    # args = parser.parse_args()

    # # finding the index of the title
    # index = movies[movies['Title'].str.contains(args.t, case=False, na=False)].index[0]
    # logging.info(movies.iloc[index])
    # movie_index = index # Define the movie index you want to compare
    # logging.info(cosine_max(movie_index))
    

