import requests
import pandas as pd
import shapely as sh
import geopandas as gpd
from DBloader import table_loader




def uldk_api(dane):
    """
        Funkcja pobiera identyfikatory działek z pliku CSV,
        wysyła zapytania do serwisu ULDK w celu pobrania danych na temat działek,
        a następnie przetwarza te dane do postaci ramki danych geopandas.

        Args:
            dane (str): Ścieżka do pliku CSV zawierającego identyfikatory działek.

        Returns:
            GeoDataFrame: Ramka danych geopandas zawierająca dane na temat działek.
    """
    def df_to_list(df):
        """
            Funkcja przekształca ramkę danych pandas do listy identyfikatorów działek.

            Args:
                df (DataFrame): Ramka danych pandas zawierająca identyfikatory działek.

            Returns:
                list: Lista identyfikatorów działek.
            """
        list=[]
        for i in range(len(df.index)):
            list.append(df.at[i, df.columns[0]])
        return list

    def request(list):
        """
           Funkcja wysyła zapytania HTTP do serwisu ULDK w celu pobrania danych na temat działek na podstawie ich identyfikatorów.

           Args:
               id_list (list): Lista identyfikatorów działek.

           Returns:
               list: Lista odpowiedzi HTTP zawierających dane na temat działek.
           """
        result=[]
        for i in list:
            result.append(requests.get("https://uldk.gugik.gov.pl/?request=GetParcelById&id=" + i + "&result=teryt,commune,region,geom_wkb").text)
        return result

    def result_to_df(result):
        """
            Funkcja przetwarza odpowiedzi HTTP z serwisu ULDK do postaci ramki danych pandas.

            Args:
                result (list): Lista odpowiedzi HTTP zawierających dane na temat działek.

            Returns:
                DataFrame: Ramka danych pandas zawierająca dane na temat działek.
            """
        to_df_list=[]
        for i in result:
            i = i.strip()
            to_df_list.append(i.split(sep='|'))
            df = pd.DataFrame({'TERYT': ['Null'] * len(to_df_list), 'Miasto': ['Null'] * len(to_df_list), 'Region': ['Null'] * len(to_df_list),'WKB': ['Null'] * len(to_df_list)})
            for i in range(len(to_df_list)):
                for l in range(len(to_df_list[i])):
                    df.iloc[i, l] = to_df_list[i][l]
        return df

    def df_to_gdf(df):
        df = df[df['WKB'] != 'Null']
        geometry = df['WKB'].map(sh.wkb.loads)
        gdf = gpd.GeoDataFrame(df, crs="EPSG:2180", geometry=geometry)
        return gdf


    return df_to_gdf(result_to_df(request(df_to_list(pd.read_csv(dane)))))


def gdf_to_shp(gdf):
    """
        Konwertuje ramkę danych geopandas na plik shapefile.

        Args:
            gdf (GeoDataFrame): Ramka danych geopandas zawierająca geometrię.
            filename (str): Nazwa pliku shapefile.

    """
    gdf.to_file(filename=f'{dane}.shp', driver='ESRI Shapefile')




table_loader(uldk_api("ewid_id.csv"),"Parcele")

