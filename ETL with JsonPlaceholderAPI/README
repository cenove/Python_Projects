# ETL Pipeline: JSONPlaceholder to PostgreSQL

This project consists of a Python-based ETL (Extract, Transform, Load) script that extracts public data from the JSONPlaceholder API, performs transformations and aggregations using Pandas, and loads the consolidated results into a PostgreSQL database using the `psycopg` library.

## Process Overview

1. **Extract:** User, post, and comment data are fetched from the JSONPlaceholder REST API and saved locally as CSV files.
2. **Transform:** The script reads the CSV files, calculates the total number of comments per post, performs joins to enrich the data with user details, and saves the final output to `df_main.csv`.
3. **Load:** It uses PostgreSQLs native "COPY" command via the "psycopg" library to efficiently bulk-insert the transformed data into the database.

## Prerequisites

The prerequisites can be downloaded using the 'requirements.txt' attached to the repository.
Additionally, you need a running PostgreSQL instance and a target table created with columns matching the output schema.

##Configuration
Before running the script, update your PostgreSQL database credentials in the connection section:

'''python
con = psycopg.connect(
    host='localhost', # or your server host/IP
    dbname='DATABASE_NAME',
    user='postgres',
    password='USER_PASSWORD'
)
'''

Make sure to replace TABLE_NAME with your actual table name inside the csv_sender() function:

'''SQL
COPY TABLE_NAME (user_id, user_name, company, post_id, total_comments) 
FROM STDIN 
WITH (FORMAT CSV, HEADER true, DELIMITER ',');
'''
