from sqlalchemy import create_engine
import psycopg2
from config import load_config

def connect(config):
    """
    Connects to a PostgreSQL database using the provided configuration.

    Args:
        config (dict): A dictionary containing the database configuration parameters.

    Returns:
        conn: A connection object to the PostgreSQL database.
    """
    try:
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"An error occurred: {error}")

conn = connect(load_config())

def table_loader(gdf, table_name, engine, user, password, host, port, database):
    """
    Loads a GeoDataFrame into a PostGIS table in the PostgreSQL database.

    Args:
        gdf (GeoDataFrame): The GeoDataFrame containing spatial data to be loaded.
        table_name (str): The name of the table to load the data into.
        engine (str): The database engine (e.g., 'postgresql').
        user (str): The database username.
        password (str): The database password.
        host (str): The database host address.
        port (int): The database port number.
        database (str): The name of the database.

    """
    db_connection_url = f"{engine}://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(db_connection_url)
    gdf.to_postgis(table_name, con=engine, if_exists="replace")
    print(f"Data loaded into table {table_name} in the {database} database.")