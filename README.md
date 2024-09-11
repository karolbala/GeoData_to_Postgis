# GeoData_to_Postgis

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)

## Overview

This project provides a set of tools for processing and managing geospatial data. It includes functionalities to import geospatial data from various formats (CSV, Shapefile, GeoJSON, SQL) into a PostGIS-enabled PostgreSQL database and export data to Shapefiles. The project also supports fetching parcel data from the ULDK API The uldk_api function is designed to interact with the ULDK (Unified Land Registry Database) API, which provides geospatial data about land parcels in Poland.

To import data from various file formats (CSV, Shapefile, GeoJSON, SQL) into PostGIS, use the `import_to_postgis` function. This function determines the file format based on the file extension and calls the appropriate import function.


## Features

- **Connect to PostgreSQL**: Establish a connection to a PostgreSQL database with PostGIS extension enabled.
- **Import Data**:
  - From CSV files to PostGIS.
  - From Shapefiles to PostGIS.
  - From GeoJSON files to PostGIS.
  - From SQL files to PostGIS.
- **Export Data**:
  - Convert `GeoDataFrame` to Shapefile for use in GIS applications.

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
  - `numpy`




