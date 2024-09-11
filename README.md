# GeoData_to_Postgis

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [1. Importing Parcel Data from ULDK API](#1-importing-parcel-data-from-uldk-api)
  - [2. Loading Data into PostGIS](#2-loading-data-into-postgis)
  - [3. Exporting GeoData to Shapefile](#3-exporting-geodata-to-shapefile)
- [Project Structure](#project-structure)
- [To-Do / Future Enhancements](#to-do--future-enhancements)
- [License](#license)

## Overview

This project demonstrates the process of importing, transforming, and saving geospatial data into a PostGIS database using Python. It integrates with the ULDK API to retrieve parcel data (geometries, regions, etc.), processes it using libraries such as `pandas`, `geopandas`, and `shapely`, and stores the results in a PostGIS-enabled PostgreSQL database.

Additionally, the project supports exporting geospatial data to shapefile format for further analysis or sharing.

## Features

- Fetch parcel data from the ULDK API using parcel identifiers.
- Convert the returned data into a GeoDataFrame for analysis.
- Load the processed geospatial data into a PostGIS database.
- Export the geospatial data to shapefiles (`.shp`) for further use in GIS software.

## Requirements

- Python 3.7 or higher
- PostgreSQL with PostGIS extension enabled
- Libraries:
  - `requests`
  - `pandas`
  - `geopandas`
  - `shapely`
  - `sqlalchemy`
  - `psycopg2`

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/gis-data-import-tool.git
    ```

2. Install required Python libraries using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure PostgreSQL is running, and the PostGIS extension is enabled in your database.

4. Set up your environment variables or edit the `config.py` file to match your PostgreSQL credentials.

## Usage

### 1. Importing Parcel Data from ULDK API

To fetch parcel data based on a CSV file containing parcel identifiers, use the function `uldk_api`. This function will send requests to the ULDK API and retrieve parcel data including geometry in Well-Known Binary (WKB) format.

```python
from uldk_api_tool import uldk_api

# Path to the CSV file containing parcel IDs
csv_file = "parcel_ids.csv"

# Fetch and process data into a GeoDataFrame
gdf = uldk_api(csv_file)
```

### 2. Loading Data into PostGIS

Once you have processed the parcel data, you can load it into a PostGIS-enabled PostgreSQL database. This example shows how to use the table_loader function:

```python
from DBloader import table_loader

# Define your database connection details
db_user = 'your_db_user'
db_password = 'your_db_password'
db_host = 'localhost'
db_port = '5432'
db_name = 'gis_database'

# Load GeoDataFrame into PostGIS
table_loader(gdf, 'parcel_data', 'postgresql', db_user, db_password, db_host, db_port, db_name)
```

### 3. Exporting GeoData to Shapefile

If you need to export your geospatial data into a shapefile, use the gdf_to_shp function. This is useful for further analysis in GIS software like QGIS.

```python
from uldk_parcels import gdf_to_shp

# Export the GeoDataFrame to a shapefile
gdf_to_shp(gdf, "parcel_data_shapefile")
```

###


