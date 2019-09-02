import psycopg2

db_host = os.getenv('db_host')
db_user = os.getenv('db_user')
db_passwd = os.getenv('db_passwd')
db_database = os.getenv('db_name')
db_port = os.getenv('db_port')

con_string = "dbname=" + os.getenv('DB_NAME') + " user=" + os.getenv('DB_USER') + " host=" + os.getenv('DB_HOST') + " password=" + os.getenv('DB_PASSWORD')

conn = psycopg2.connect(con_string)
cur = conn.cursor()

poi_cat_q = """SELECT f.cat_name as foo FROM (
                    SELECT DISTINCT ON (cat_name) cat_name, parent_id
                    FROM django.poi_manager_poicategory) AS f"""

poi_q = """SELECT x.foo as foo FROM (
                    SELECT DISTINCT ON (name) name as foo, fk_poi_category_id
                    FROM django.poi_manager_poi) AS x
            
            ORDER BY foo ASC ;"""


def generate_poi_translation_template(filename, poi_query):
    # query the database table for the list of names you want to translate

    cur.execute(poi_query)
    res_floor_id = cur.fetchall()

    with open(filename, 'w') as f:
        f.write('{% load i18n %}' + '\n\n')
        for r in res_floor_id:
            f.write('{% trans "' + r[0] + '" %}\n')


generate_poi_translation_template('poi-cat-translations.html', poi_cat_q)
generate_poi_translation_template('poi-translations.html', poi_q)
