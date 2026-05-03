from pathlib import Path
from datetime import datetime
from psycopg2 import sql
from django.db import connection
from django.utils import timezone
from .config import DATA_DIR, RAW_PREFIX, GEO_PREFIX, parse_filename
from .utils import ogr2ogr_import
from .models import FileRegistry, DxfImportedTable


def _registry_row(cur, file_path: Path):
    cur.execute(
        "SELECT mtime FROM file_registry WHERE path = %s",
        (str(file_path),)
    )
    return cur.fetchone()

def _register(cur, file_path: Path, mtime: float, table_raw: str):
    cur.execute(
        """
        INSERT INTO file_registry(path, mtime, table_raw)
        VALUES(%s, to_timestamp(%s), %s)
        ON CONFLICT (path) DO UPDATE SET mtime = EXCLUDED.mtime
        """,
        (str(file_path), mtime, table_raw)
    )


def import_firsttime(file_path: Path):
    mtime = file_path.stat().st_mtime
    table_raw = file_path.stem.lower()
    table_geo = GEO_PREFIX + file_path.stem.lower()

    # Use Django connection for SQL operations
    with connection.cursor() as cur:
        # drop old tables quietly
        cur.execute(sql.SQL("DROP TABLE IF EXISTS dxf_original.{} CASCADE").format(
            sql.Identifier(table_geo)))
        print(f"Dropping table: {table_geo}")
        cur.execute(sql.SQL("DROP TABLE IF EXISTS dxf_original.{} CASCADE").format(
            sql.Identifier(table_raw)))
        print(f"Dropping table: {table_raw}")

    # Import the DXF file using ogr2ogr
    ogr2ogr_import(file_path, table_raw)

    # Update or create FileRegistry entry
    registry_obj, created = FileRegistry.objects.update_or_create(
        path=str(file_path),
        defaults={
            'mtime': timezone.make_aware(datetime.fromtimestamp(mtime)),
            'table_raw': table_raw
        }
    )

    # Create or update DxfImportedTable for the raw table
    DxfImportedTable.objects.update_or_create(
        table_name=table_raw,
        defaults={
            'schema_name': 'dxf_original',
            'file_registry': registry_obj,
            'srid': int(3857),  # From config.TARGET_SRID
            'has_georef': False,
            'georef_table_name': table_geo
        }
    )

def import_if_changed(file_path: Path):
    mtime = file_path.stat().st_mtime
    # table_raw = RAW_PREFIX + file_path.stem.lower()
    table_raw = file_path.stem.lower()
    table_geo = GEO_PREFIX + file_path.stem.lower()

    # Try to get existing registry entry from Django ORM
    try:
        registry = FileRegistry.objects.get(path=str(file_path))
        print(f"Registry entry found: {registry}")
        if abs(registry.mtime.timestamp() - mtime) < 1:
            return False  # no change
    except FileRegistry.DoesNotExist:
        registry = None

    return True

def list_changed_files():
    """
    Import all DXF files from the DATA_DIR if they have changed
    
    Returns:
        list: Names of the files that were imported
    """
    changed = []
    print(f"Importing DXF files from {DATA_DIR}")

    root_dir = Path(DATA_DIR)
    if not root_dir.exists():
        print(f"Error: DATA_DIR does not exist: {root_dir}")
        return changed

    root_dir = Path(DATA_DIR)
    print(f"Root dir: {root_dir}")
    for f in root_dir.rglob("*.dxf"):
        changed.append(f)
        print(f"Importing {f.name}")
        # if import_if_changed(f):
        #     changed.append(f.name)
    return changed
