import pandas as pd
import requests as r
import psycopg

con = psycopg.connect(
    host='localhost, 128.0.0.1, SERVER_HOST',
    dbname = 'DATABASE_NAME',
    user='postgres',
    # If your server has no password just delete the password line 
    password= 'USER_PASSWORD'
)

api_url = 'https://jsonplaceholder.typicode.com'
POST = "/posts"
COMMENTS = "/comments"
ALBUMS = "/albums"
PHOTOS = "/photos"
USERS = "/users"

def api_to_csv(endpoint, filename):
    api_getter = api_url + endpoint
    try:
        response = r.get(api_getter)
        response.raise_for_status()
        json_data = response.json()
        df = pd.json_normalize(json_data,sep='-')
        df.to_csv(f'{filename}.csv',index=False)

    except r.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err}")

    except r.exceptions.ConnectTimeout as conn_timeout:
            print(f"HTTP error: {conn_timeout}")

    except r.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")  

# Total de comentários por posts
def report_creator():
    df_users = pd.read_csv("users.csv")
    df_posts = pd.read_csv("posts.csv")
    df_comments = pd.read_csv("comments.csv")
    
    comments_count = df_comments.groupby("postId").size().reset_index(name="total_comments")

#JOINS
    df = df_posts.merge(comments_count, left_on="id", right_on="postId", how="left")
    df = df.merge(df_users, left_on="userId", right_on="id", how="left", suffixes=('_post', '_user'))

    df_main = df[["userId", "username", "company-name", "id_post", "total_comments"]]    
    df_main = df_main.rename(columns={
        "userId": "user_id",
        "username": "user_name",
        "company-name": "company",
        "id_post": "post_id",
    })
    df_main["total_comments"] = df_main["total_comments"].fillna(0).astype(int)
    df_main.to_csv("df_main.csv", index=False)

def csv_sender():
    caminho_csv = "df_main.csv"

#DONT FORGET THE TABLE NAME
    sql_query = """
        COPY TABLE_NAME (user_id, user_name, company, post_id, total_comments) 
        FROM STDIN 
        WITH (FORMAT CSV, HEADER true, DELIMITER ',');
    """

    try:
        with con.cursor() as cur:
            with open(caminho_csv, 'r', encoding='utf-8') as f:
                with cur.copy(sql_query) as copy:
                    while data := f.read(8192):
                        copy.write(data)
            con.commit()
            print("Loaded successfully into PostgreSQL!")
    except Exception as e:
        print(f"Error loading to database: {e}")
        con.rollback()
    finally:
        con.close()

if __name__ == "__main__":
    api_to_csv(COMMENTS,"comments")
    api_to_csv(POST,"posts")
    api_to_csv(USERS,"users")
    report_creator()
    csv_sender()