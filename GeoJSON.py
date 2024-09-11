from sqlalchemy import create_engine
import geopandas as gpd


def import_geojson_to_postgis(table_name, geojson, user, password, host, port, database):

    """
    Importuje dane z pliku shapefile do bazy danych PostGIS.

    Args:
        table_name (str): Nazwa tabeli, do której będą importowane dane.
        geojosn (str): Ścieżka do pliku geojson.
        user (str): Nazwa użytkownika bazy danych.
        password (str): Hasło użytkownika bazy danych.
        host (str): Adres hosta bazy danych.
        port (str): Numer portu serwera.
        database (str): Nazwa bazy danych.

    """

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    try:
        gdf = gpd.read_file(geojson)
        gdf = gdf.to_crs(2180)
        gdf.to_postgis(table_name, engine, if_exists='replace', index=False)
        print(f"Wczytano dane z pliku {geojson} do tabeli {table_name} w bazie danych {database}")
    except FileNotFoundError as e:
        print(f"Błąd: {e}. Upewnij się, że plik GeoJSON o podanej nazwie istnieje.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")