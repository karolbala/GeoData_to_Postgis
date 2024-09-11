from SHP import import_shapefile_to_postgis
from CSV import import_csv_to_postgis
from GeoJSON import import_geojson_to_postgis
from SQL import import_sql_to_postgis


# Files in different formats
def import_to_postgis(table_name, file, user, password, host, port, database):
    """
    Imports data from files in csv/shapefile/geojson/sql formats into the PostGIS database.

    Args:
        table_name (str): The name of the table where data will be imported.
        file (str): Path to the file (csv, shapefile, geojson, sql).
        user (str): Database username.
        password (str): Database password.
        host (str): Database host address.
        port (str): Database server port number.
        database (str): Database name.

    Raises:
        Exception: If the file format is unsupported.
    """

    ext = file.split(sep=".")[1]

    if ext == "csv":
        import_csv_to_postgis(table_name, file, user, password, host, port, database)
    elif ext == "shp":
        import_shapefile_to_postgis(table_name, file, user, password, host, port, database)
    elif ext == "geojson":
        import_geojson_to_postgis(table_name, file, user, password, host, port, database)
    elif ext == "sql":
        import_sql_to_postgis(table_name, file, user, password, host, port, database)
    else:
        raise Exception("Unsupported format")
