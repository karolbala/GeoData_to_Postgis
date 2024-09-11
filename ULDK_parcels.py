import requests
import pandas as pd
import shapely as sh
import geopandas as gpd
from DBloader import table_loader

def uldk_api(data):
    """
    The function fetches parcel identifiers from a CSV file, sends requests to the ULDK service
    to retrieve data about the parcels, and then processes this data into a GeoPandas DataFrame.

    Args:
        data (str): Path to the CSV file containing parcel identifiers.

    Returns:
        GeoDataFrame: A GeoPandas DataFrame containing data about the parcels.
    """
    def df_to_list(df):
        """
        Converts a pandas DataFrame into a list of parcel identifiers.

        Args:
            df (DataFrame): A pandas DataFrame containing parcel identifiers.

        Returns:
            list: A list of parcel identifiers.
        """
        parcel_list = []
        for i in range(len(df.index)):
            parcel_list.append(df.at[i, df.columns[0]])
        return parcel_list

    def request(parcel_list):
        """
        Sends HTTP requests to the ULDK service to retrieve data about parcels based on their identifiers.

        Args:
            parcel_list (list): A list of parcel identifiers.

        Returns:
            list: A list of HTTP responses containing data about parcels.
        """
        result = []
        for parcel_id in parcel_list:
            result.append(requests.get(f"https://uldk.gugik.gov.pl/?request=GetParcelById&id={parcel_id}&result=teryt,commune,region,geom_wkb").text)
        return result

    def result_to_df(result):
        """
        Processes the HTTP responses from the ULDK service into a pandas DataFrame.

        Args:
            result (list): A list of HTTP responses containing data about parcels.

        Returns:
            DataFrame: A pandas DataFrame containing data about parcels.
        """
        to_df_list = []
        for response in result:
            response = response.strip()
            to_df_list.append(response.split(sep='|'))
        df = pd.DataFrame({
            'TERYT': ['Null'] * len(to_df_list),
            'City': ['Null'] * len(to_df_list),
            'Region': ['Null'] * len(to_df_list),
            'WKB': ['Null'] * len(to_df_list)
        })
        for i in range(len(to_df_list)):
            for j in range(len(to_df_list[i])):
                df.iloc[i, j] = to_df_list[i][j]
        return df

    def df_to_gdf(df):
        """
        Converts a pandas DataFrame containing parcel data into a GeoPandas DataFrame.

        Args:
            df (DataFrame): A pandas DataFrame containing parcel data, including geometry in WKB format.

        Returns:
            GeoDataFrame: A GeoPandas DataFrame with geometry.
        """
        df = df[df['WKB'] != 'Null']
        geometry = df['WKB'].map(sh.wkb.loads)
        gdf = gpd.GeoDataFrame(df, crs="EPSG:2180", geometry=geometry)
        return gdf

    return df_to_gdf(result_to_df(request(df_to_list(pd.read_csv(data)))))

def gdf_to_shp(gdf, filename):
    """
    Converts a GeoPandas DataFrame into a shapefile.

    Args:
        gdf (GeoDataFrame): A GeoPandas DataFrame containing geometry.
        filename (str): Name of the shapefile to be saved.

    """
    gdf.to_file(filename=filename, driver='ESRI Shapefile')
