import pandas as pd 
import logging 
import argparse
from sklearn.metrics.pairwise import cosine_similarity
#from smartmovierecommender.transformer.gemini_query import process_movies
#from smartmovierecommender.collector.datascraper import scraper 
import os
print(os.getcwd())
from smartmovierecommender.utils.combining_data import movie_combiner, get_movie_rec, preprocess_movies
from smartmovierecommender.calculation.cosine_sim import convert_duration, convert_ratings, cosine_sim, cosine_max, convert_to_title
#from smartmovierecommender.collector.datacollect import fetch_movie_details_imdb

#I don't have permission so it wasn't working 
# logging.basicConfig(
#     level=logging.INFO,
#     filename='../../../../logs.txt',
#     filemode='w', 
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

   

def main(movie_title):
    #opens the function to get the dataset 
    print(os.getcwd())
    #movies = preprocess_movies("../processed-data/output_file.csv")
    movies = preprocess_movies("processed-data/output_file.csv")
    #does the cosine sim and gets the top 5 recs 
    recs = get_movie_rec(movies,movie_title)
    if recs.empty:
        print("No recommendations found.")
    else:
        print("\nTop Recommendations:")
        for i, row in recs.iterrows():
            print(f"{row['Title']} (Similarity: {row['Similarity']:.2f})")


 
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
        movie_title=args.t
        #new_movie_features=new_movie
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
    