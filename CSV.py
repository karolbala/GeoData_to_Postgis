from sqlalchemy import create_engine
import geopandas as gpd
import pandas as pd



def import_csv_to_postgis(table_name, plik_csv, user, password, host, port, database):

    """
    Importuje dane z pliku CSV do bazy danych PostGIS.

    Args:
        table_name (str): Nazwa tabeli, do której będą importowane dane.
        plik_csv (str): Ścieżka do pliku CSV.
        user (str): Nazwa użytkownika bazy danych.
        password (str): Hasło użytkownika bazy danych.
        host (str): Adres hosta bazy danych.
        port (str): Numer portu serwera.
        database (str): Nazwa bazy danych.

    """


    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    try:
        df=pd.read_csv(plik_csv)
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.WspX, df.WspY, crs="EPSG:2180"))
        gdf = gdf.to_crs(2180)
        gdf.to_postgis(table_name, engine, if_exists='replace', index=False)
        print(f"Wczytano dane z pliku {plik_csv} do tabeli {table_name} w bazie danych {database}")
    except FileNotFoundError as e:
        print(f"Błąd: {e}. Upewnij się, że plik csv o podanej nazwie istnieje.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")




