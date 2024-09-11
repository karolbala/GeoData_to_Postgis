from sqlalchemy import create_engine
import geopandas as gpd

def import_geojson_to_postgis(table_name, geojson, user, password, host, port, database):
    """
    Imports data from a GeoJSON file into a PostGIS database.

    Args:
        table_name (str): Name of the table to import the data into.
        geojson (str): Path to the GeoJSON file.
        user (str): Database username.
        password (str): Database user password.
        host (str): Database host address.
        port (str): Server port number.
        database (str): Name of the database.

    """

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    try:
        gdf = gpd.read_file(geojson)
        gdf = gdf.to_crs(2180)
        gdf.to_postgis(table_name, engine, if_exists='replace', index=False)
        print(f"Data from {geojson} has been successfully loaded into the table {table_name} in the {database} database")
    except FileNotFoundError as e:
        print(f"Error: {e}. Please make sure the GeoJSON file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")