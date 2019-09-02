import psycopg2
import geojson

con_string = "dbname=" + os.getenv('DB_NAME') + " user=" + os.getenv('DB_USER') + " host=" + os.getenv('DB_HOST') + " password=" + os.getenv('DB_PASSWORD')

conn = psycopg2.connect(con_string)
cur = conn.cursor()


sql = f""" SELECT jsonb_build_object(
    'type',     'FeatureCollection',
    'features', jsonb_agg(feature)
)
FROM (
  SELECT jsonb_build_object(
    'type',       'Feature',
    'id',         id,
    'geometry',   ST_AsGeoJSON(geometry)::jsonb,
    'properties', to_jsonb(row) - 'id' - 'geometry'
  ) AS feature
  FROM (SELECT id, damage_id, external_id, notes, geometry  FROM django.insights_damage where survey_id=54 and is_damage = True and geometry IS NOT NULL) row) features;
  """

cur.execute(sql)

x = cur.fetchone()

with open("mygeo.geojson", "w") as f:
    f.write(str(x[0]))

cur.close()
