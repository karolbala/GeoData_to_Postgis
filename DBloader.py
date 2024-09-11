from sqlalchemy import create_engine
import psycopg2
from config import load_config

def connect(config):
    try:
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

conn=connect(load_config())

def table_loader(gdf,name, engine='postgresql',user='igp419798', password='igp563669', host='ak.geod.agh.edu.pl',port='5432',db='igp419798'):
    db_connection_url = f"{engine}://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(db_connection_url)
    gdf.to_postgis(name, con=engine, if_exists= "replace")


