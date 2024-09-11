import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import geopandas as gpd
import shapely.wkb as sh

def import_sql_to_postgis(table_name, file, user, password, host, port, database):
    """
    Imports data from an SQL file into a PostGIS table in a PostgreSQL database.

    Args:
        table_name (str): Name of the table to import data into.
        file (str): Path to the SQL file containing the data.
        user (str): Database username.
        password (str): Database user password.
        host (str): Database host address.
        port (str): Server port number.
        database (str): Name of the database.

    Raises:
        KeyError: Raised if the 'wkb_geometry' column is missing in the SQL file.
        FileNotFoundError: Raised if the SQL file cannot be found.
        Exception: Any other errors that may occur.
    """

    # Create the engine
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")

    # Function to extract the data inside INSERT statements from the SQL file
    def display_insert_lines(file_path):
        data_list = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if 'INSERT INTO' in line:
                        values_part = line.split('VALUES')[1].strip()[1:-2]
                        values = values_part.replace("'", "").split(', ')
                        data_list.append(values)
                return data_list
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Function to extract column names
    def get_columns(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if 'INSERT INTO' in line:
                        columns_part = line.split('(')[1].split(')')[0].strip()
                        columns = columns_part.replace('"', "").split(', ')
                        return columns
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    data = display_insert_lines(file)
    columns = get_columns(file)

    try:
        # Create a flat DataFrame
        df = pd.DataFrame(data=data, columns=columns)

        df['wkb_geometry'] = df['wkb_geometry'].str.strip().str.replace("'", "")  # Remove quotes and spaces

        # Create a geometry column by mapping the WKB data using Shapely
        df['geometry'] = df['wkb_geometry'].map(sh.loads)

        # Convert geometry into a 1D vector
        geometry = np.array(df['geometry'])
        geometry = geometry.flatten()

        # Convert the DataFrame to a GeoDataFrame
        gdf = gpd.GeoDataFrame(df, crs="EPSG:2180", geometry=geometry)
        # Transform the coordinate system
        gdf = gdf.to_crs(2180)

        # Load data into PostGIS table
        gdf.to_postgis(table_name, engine, if_exists='replace', index=False)
        print(f"Data from the SQL file has been successfully loaded into the {table_name} table in the {database} database.")

    except KeyError as e:
        print(f"Error: {e}. Please ensure the 'wkb_geometry' column exists in the SQL file.")
    except Exception as e:
        print(f"An error occurred: {e}")