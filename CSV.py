from sqlalchemy import create_engine
import geopandas as gpd
import pandas as pd

def import_csv_to_postgis(table_name, csv_file, user, password, host, port, database):
    """
    Imports data from a CSV file into a PostGIS database.

    Args:
        table_name (str): Name of the table to import the data into.
        csv_file (str): Path to the CSV file.
        user (str): Database username.
        password (str): Database user password.
        host (str): Database host address.
        port (str): Server port number.
        database (str): Name of the database.
    """

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    try:
        df = pd.read_csv(csv_file)
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.WspX, df.WspY, crs="EPSG:2180"))
        gdf = gdf.to_crs(2180)
        gdf.to_postgis(table_name, engine, if_exists='replace', index=False)
        print(f"Data from {csv_file} has been successfully loaded into the table {table_name} in the {database} database")
    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure the CSV file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")


