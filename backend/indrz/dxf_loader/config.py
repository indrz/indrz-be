import os
from pathlib import Path
from typing import Tuple

# DATA_DIR = Path(os.getenv("DXF_RSYNC_SOURCE")).resolve()
DATA_DIR = Path("/opt/data/cad/dwg_src")
RAW_PREFIX = "raw_"
GEO_PREFIX = "geo_"
TARGET_SRID = int(os.getenv("TARGET_SRID", "3857"))  # web mercator default

db_user = os.getenv('PG_USER')
db_name = os.getenv('PG_DB')
db_host = os.getenv('PG_HOST')
db_pass = os.getenv('PG_PASS')
db_port = os.getenv('PG_PORT')
PG_DSN = f"host={db_host} user={db_user} dbname={db_name} password={db_pass} port={db_port}"

def parse_filename(file: Path) -> Tuple[str, str]:

    """
    Parse the filename to extract building and floor names.
    
    Args:
        file: Path object of the DXF file.
        
    Returns:
        Tuple[str, str]: Building name and floor name.

    Example: using -2 and -3 as the positions of building and floor names
        >>> parse_filename(Path("V_PLLCCG_001_LC_OG01_08HB1021.dxf"))
        ('LC', 'OG01')
    """
    BUILDING_CODE_POS = -2 # postion of builidng name in filename
    FLOOR_NAME_POS = -3 # postion of floor name in filename

    original_filename = file.stem
    building_code = original_filename.split('_')[BUILDING_CODE_POS]
    floor_name = original_filename.split('_')[FLOOR_NAME_POS]

    return (building_code, floor_name)
