from sqlalchemy import create_engine
import geopandas as gpd



def import_shapefile_to_postgis(table_name, shapefile, user, password, host, port, database):

    """
    Importuje dane z pliku shapefile do bazy danych PostGIS

    Args:
        table_name (str): Nazwa tabeli, do której będą importowane dane.
        shapefile (str): Ścieżka do pliku shapefile.
        user (str): Nazwa użytkownika bazy danych.
        password (str): Hasło użytkownika bazy danych.
        host (str): Adres hosta bazy danych.
        port (str): Numer portu serwera.
        database (str): Nazwa bazy danych.

    """

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    try:
        gdf = gpd.read_file(shapefile)
        gdf = gdf.to_crs(2180)
        gdf.to_postgis(table_name, engine, if_exists='replace', index=False)
        print(f"Wczytano dane z pliku {shapefile} do tabeli {table_name} w bazie danych {database}")
    except FileNotFoundError as e:
        print(f"Błąd: {e}. Upewnij się, że plik shapefile o podanej nazwie istnieje.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")