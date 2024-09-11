import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import geopandas as gpd
import shapely.wkb as sh



def import_sql_to_postgis(table_name, file, user, password, host, port, database):
    """
       Importuje dane z pliku SQL do tabeli PostGIS w bazie danych PostgreSQL.

       Args:
           table_name (str): Nazwa tabeli, do której będą importowane dane.
           file (str): Ścieżka do pliku SQL zawierającego dane.
           user (str): Nazwa użytkownika bazy danych.
           password (str): Hasło użytkownika bazy danych.
           host (str): Adres hosta bazy danych.
           port (str): Numer portu serwera.
           database (str): Nazwa bazy danych.

       Raises:
           KeyError: Występuje, gdy kolumna 'wkb_geometry' nie istnieje w pliku SQL.
           FileNotFoundError: Występuje, gdy plik SQL nie zostanie odnaleziony.
           Exception: Inne występujące błędy.

       """

    #Tworzenie silnika
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")

    # Funkcja pozyskująca wnętrze INSERTÓW z pliku SQL
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

    # Funkcja pozyskująca nazwy kolumn
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
        # Tworzenie płaskiej ramki danych
        df = pd.DataFrame(data=data, columns=columns)

        df['wkb_geometry '] = df['wkb_geometry '].str.strip().str.replace("'", "")  # Usunięcie cudzysłowów i spacji

        # Tworzenie kolumny geometrii poprzez mapowanie kolumny z danymi w formacie WKB funkcją z biblioteki Shapely
        df['geometry'] = df['wkb_geometry '].map(sh.loads)

        # Przekształcenie geometrii do 1-wymiarowego wektora
        geometry = np.array(df['geometry'])
        geometry = geometry.flatten()

        # Zamiana ramki na GeoDataFrame
        gdf = gpd.GeoDataFrame(df, crs="EPSG:2180", geometry=geometry)
        # Zmiana układu współrzędnych
        gdf = gdf.to_crs(2180)

        gdf.to_postgis(table_name, engine, if_exists='replace',index=False)  # Aktualizacja zapisu nazwy kolumny geometrii
        print(f"Wczytano dane z pliku SQL do tabeli {table_name} w bazie danych {database}")

    except KeyError as e:
        print(f"Błąd: {e}. Upewnij się, że kolumna 'wkb_geometry' istnieje w pliku SQL.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
