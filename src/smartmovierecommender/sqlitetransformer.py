import sqlite3
import json
import os
import logging

def sqlite_json_to_database_exporter(json_directory, db_file, table):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table} (
            id INTEGER PRIMARY KEY,
            Title TEXT,
            Year TEXT,
            Duration TEXT,
            Rated TEXT,
            IMDB_Rating REAL,
            Number_of_Ratings TEXT,
            Description TEXT
        )
    ''')

    for filename in os.listdir(json_directory):
        if filename.endswith(".json"):
            path = os.path.join(json_directory, filename)
            with open(path, 'r') as f:
                try:
                    json_data = json.load(f)
                    if isinstance(json_data, list):
                        for js in json_data:  
                            dump_json_data(js, cursor, table)
                    elif isinstance(json_data, dict):  
                        dump_json_data(json_data, cursor, table)
                    else:
                        logging.error(f"wrong file {filename}")
                
                except json.JSONDecodeError as e:
                    logging.error(f"file reading error {filename} : {e}")

    connection.commit()
    connection.close()

def dump_json_data(js, cursor, table):
    title = js.get("Title", None)
    year = js.get("Year", None)
    duration = js.get("Duration", None)
    rated = js.get("Rated", None)
    imdb_rating = float(js.get("IMDB Rating", 0)) if "IMDB Rating" in js else None
    number_of_ratings = js.get("Number of Ratings", None)
    description = js.get("Description", None)

    cursor.execute(f'''
        INSERT INTO {table} (
            Title, Year, Duration, Rated, IMDB_Rating, Number_of_Ratings, Description
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, year, duration, rated, imdb_rating, number_of_ratings, description))

sqlite_json_to_database_exporter("../../data/",  "../../data/SmartMoviesRecomender.db", "smart_movie_table")
