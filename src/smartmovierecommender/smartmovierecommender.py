

# import pandas as pd 
# import logging 
# import argparse
# from smartmovierecommender.transformer.gemini_query import process_movies
# from smartmovierecommender.collector.datascraper import scraper 
# from smartmovierecommender.utils.combining_data import movie_combiner
# from smartmovierecommender.calculation.cosine_sim import convert_duration, convert_ratings, cosine_sim, cosine_max, convert_to_title



# logging.basicConfig(
#     level=logging.INFO,
#     filename='../../../../logs.txt',
#     filemode='w', 
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# def main(link_for_scraping, to_scrape, to_gemini, to_cosine_score, movie): 
#     if to_scrape:
#         scraper(link_for_scraping)
    
#     movie_combiner("../../output_data/", "../../processed-data/output_file.csv")
    
#     if to_gemini:
#         process_movies()
        
#     if to_cosine_score:   
#             # Reading in CSV
#         movies = pd.read_csv("../../processed-data/output_file.csv")
#         # Converting duration to numeric
#         movies['Duration'] = movies['Duration'].astype(str)
#         movies['Duration'] = movies['Duration'].apply(convert_duration)

#         # converting MPAA rating to numeric
#         rating_mapping = {
#             'nan': 0,
#             'G': 1,
#             'PG': 2,
#             'PG-13': 3,
#             'R': 4,
#             'NC-17': 5,
#             'Unrated': 6
#         }
#         movies['Rated'] = movies['Rated'].map(rating_mapping)
            
#         movies['Number of Ratings'] = movies['Number of Ratings'].astype(str).fillna('0')
#         movies['Number of Ratings'] = movies['Number of Ratings'].apply(convert_ratings)

#         # dropping variables:
#         columns_to_drop = ['Description', 'Descrption', 'Genre', 'Runtime', 'Director', 'Writer', 'Actors', 'Rating', 'Awards', 'Description']
#         movies = movies.drop(columns=columns_to_drop)

#         # filling the missing with zeros
#         movies = movies.fillna(0)

#         # normalizing all the variables to 0-1
#         movie_titles = movies['Title']
#         movies = movies.drop(columns=['Title']).apply(lambda x: (x - x.min()) / (x.max() - x.min()))
#         movies['Title'] = movie_titles
            
#         # Getting movie title from user
   
            
 
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Movie_recommender_script")
#     parser.add_argument("-l", "--link", required=True, help="link to scrape")
#     parser.add_argument("-s", "--to_scrape", action="store_true", help="Flag to scrape or not")
#     parser.add_argument("-g", "--to_gemini", action="store_true", help="Flag to gemini score")
#     parser.add_argument("-cs", "--to_cosine_score", action="store_true", help="Flag to gemini score")
#     parser.add_argument("-t", "--title", required=True, help="Title of Movie")
    
#     args = parser.parse_args()
   
    
#     main(args.link, args.to_scrape, args.to_gemini, args.cosine_score, args.title)
#     logging.info('Scoring is completed')  
#     logging.shutdown()  
    


