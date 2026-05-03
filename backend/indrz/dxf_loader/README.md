# DXF Loader How To

## Description
This module is designed to import DXF files into a PostgreSQL PostGIS database, apply and manage georeferencing 
transformations, and manage metadata using Django models. It scans a directory to find all .dxf files,
registers those files if not already registered.  Once registered it attemps to georeference based on data
the user provides in the django admin form.  It allows user to re-run the georefernce function many times until they are
happy that the data is correctly georeferenced, never duplicating data.  The module is also designed so that it can run as a cron
job everynight and search if any of the registered files were changed if so it runs the pipeline to re-register,
georeference the data.  Users can upload a new .dxf file using the django admin. Users can replace an existing .dxf file
that was already georeferenced with a new non georeferenced dxf file, keeping the original georeferencing information and replacing
the original raw imported dxf data.

## Prerequisites

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**:

   Copy the example environment file and update it with your paths and database credentials:

   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file to set the following variables:
   - `DXF_FOLDER`: Path to the directory containing DXF files.
   - `TARGET_SRID`: Spatial Reference ID for georeferencing (default: 3857).
   - `PG_DSN`: PostgreSQL connection string.

3. **Database Setup**:

   Initialize the database schema:

   ```bash
   psql -d gis -f schema.sql
   ```

   Replace `gis` with your database name if different.

4. **Django Migrations**:

   Apply Django migrations to set up the necessary tables:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Import raw DXF data to create list of all dxf files**

   Run onetime script to import all .dxf files to be used for import

6. **Add data to the DXF Layers table**

   Manually login to Django admin to enter which dxf layers will be used for import

   1. Login Django Admin
   2. Edit layers

## Running the DXF Loader

1. **Run Once**:

   To test the loader, run it manually:

   ```bash
   python3 -m dxf_loader --once
   ```

2. **Automate with Cron** (Linux):

   Schedule the loader to run daily at 11 PM:

   ```bash
   0 23 * * * /usr/bin/python -m dxf_loader --once >> /var/log/dxf_loader.log 2>&1
   ```

## How It Works

1. **Bulk Import DXF File Naming Convention For Bulk Import**:
   - Bulk dxf file import requires users to follow a naming convention to allow mapping the file to the correct building and building floor.
   - Ensure DXF files included the naming convention `{building_name}_{floor_name}.dxf` (e.g., filename `A1_01.dxf` here the A1 is the building name and the floor number is 1). 
   - A dxf filename can optionallly include any text before or after the naming convention as optional `{building_name}_{floor_name}.dxf` for example `zulio_2025_d1_{building_name}_{floor_name}_876bd.dxf`
   - Floor numbers can optionally include half floors in the form 01_5 for floor number 1.5 an example filename is `A1_01_5.dxf`. 
   - Floor numbers are stored as floats in the database to account for floors between main floors.

2. **File Import**:
   - The `importer.py` module scans the directory specified in `DXF_FOLDER` for DXF files.
   - It imports raw DXF data into PostgreSQL using `ogr2ogr`.
   - Metadata about the imported files is stored in the `FileRegistry` model.

3. **Georeferencing**:
   - The `georef.py` module applies georeferencing transformations to the raw data.
   - Parameters are fetched from the `GeorefParams` model.
   - Transformed data is stored in a new table with a `geo_` prefix.

4. **Monitoring**:
   - The `monitor.py` script runs the import and georeferencing process in a loop or as a one-time execution.

## Troubleshooting

- **Database Connection**:
  Verify the `PG_DSN` in your `.env` file is correct.
- **Logs**:
  Check logs for errors in `/var/log/dxf_loader.log` (if using cron).

## Additional Notes

- The loader uses Django ORM for metadata management but directly interacts with PostgreSQL for raw and georeferenced data tables.
- Dynamic models have been removed for simplicity; only metadata is managed via Django.
