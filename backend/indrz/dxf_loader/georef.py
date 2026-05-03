from psycopg2 import sql
from django.db import connection
from .config import RAW_PREFIX, GEO_PREFIX
from .models import GeorefParams, DxfImportedTable

def apply_georef(basename: str):
    """
    Apply georeferencing parameters to transform raw DXF data to georeferenced data.
    
    Args:
        basename: Base name of the table to process
        
    Returns:
        bool: True if georeferencing was applied, False if no parameters were found
    """
    raw = basename
    geo = GEO_PREFIX + basename
    building_code = basename.split('_')[-3]  # Extract building code from the basename
    floor_name = basename.split('_')[-2]  # Extract floor name from the basename
    schema_dxf = 'dxf_original'
    schema_pre_django = 'pre_django'
    
    try:
        # Use Django ORM to get georef parameters
        params = GeorefParams.objects.get(table_raw=raw)
        
        # Calculate transformation parameters
        dx = params.x_geo - params.x_org  # x_geo - x_org
        dy = params.y_geo - params.y_org  # y_geo - y_org
        scale = params.scale
        rot = params.rotate  # degrees
    except GeorefParams.DoesNotExist:
        # No params yet → skip
        print(f"No georeferencing parameters found for {raw}.")
        return False
        
    # Use connection from Django
    with connection.cursor() as cur:
        sql_spaces = f"""
        INSERT INTO {schema_pre_django}.indrz_spaces_{floor_name} (geom, tags)
            SELECT (ST_SetSRID(ST_Rotate(ST_Translate(geom, {dx}, {dy}), radians({rot}), {params.x_geo}, {params.y_geo} ), 3857)) as geom,
                ARRAY['{raw}','{building_code}'] as tags
                FROM {schema_dxf}.{raw}
            where layer = '810 Raum'
            AND st_geometrytype(geom) = 'MultiLineString';"""
        
        other_sql = f"""select st_geometrytype(geom) from pre_django.mgpl_ar_ug01_20200728 group by st_geometrytype(geom);
                    truncate table pre_django.indrz_spaces_ug01 restart identity;
  
                    update pre_django.indrz_spaces_ug01 set geom = ST_Rotate(geom, radians(2.0), 1825867.41, 6142997.52 ) where id > 0;

                    update pre_django.indrz_spaces_ug01 set geom = ST_Translate(geom,-2 ,0 ) where id > 0;
                    update pre_django.indrz_spaces_ug01 set geom = ST_Translate(geom,-3,0) where id > 0;
                    update pre_django.indrz_spaces_ug01 set geom = ST_Scale(geom, 'POINT(1825867.41 6142997.52)', 'POINT(1825868.41 6142998.52)'::geometry) where id > 0;


                    update pre_django.indrz_spaces_ug01 set geom = ST_Translate(
                        ST_Scale(
                            ST_Translate(geom, -1825867.41,-6142997.52), -- Translate to origin
                            1.5, 1.5                                     -- Scale by a factor of 2
                        ),
                        1825867.41, 6142997.52                           -- Translate back to original position
                    ) where id > 0;"""



        # Drop the existing georeferenced table if it exists
        cur.execute(f"DROP TABLE IF EXISTS {schema_dxf}.{geo} CASCADE")

        # Create a new georeferenced table with transformed geometry
        geom_expr = sql.SQL(
            "ST_SetSRID(ST_Rotate(ST_Translate(geom, %s, %s), radians(%s), %s, %s), 3857)"
        )

        print(f"Creating georeferenced table {geo} from {raw} with parameters: dx={dx}, dy={dy}, scale={scale}, rot={rot}")


        
    # Update the DxfImportedTable to mark that georeferencing has been applied
    try:
        imported_table = DxfImportedTable.objects.get(table_name=raw)
        imported_table.has_georef = True
        imported_table.georef_table_name = geo
        imported_table.save()
    except DxfImportedTable.DoesNotExist:
        # If the imported table entry doesn't exist, create it
        DxfImportedTable.objects.create(
            table_name=raw,
            schema_name='dxf_original',
            has_georef=True,
            georef_table_name=geo,
            # We don't have a FileRegistry instance here, so leave it null
            # This is not ideal, but should be rare if the import process worked correctly
        )
    
    return True
