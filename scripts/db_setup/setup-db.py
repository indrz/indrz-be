#!/usr/bin/python
# -*- coding: utf-8 -*-

from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import subprocess
import os



# db_host = os.getenv('POSTGRES_HOST')
# db_user = os.getenv('POSTGRES_USER')
# db_pass = os.getenv('POSTGRES_PASS')
# db_name = os.getenv('POSTGRES_DB')
# db_port = os.getenv('POSTGRES_PORT')


# db_host = "localhost"
# db_user = "tutest"
# db_pass = "air"
# db_name = "tutest"
# db_port = "5432"
# db_owner = "tutest"
# db_superuser = "postgres"
# db_schema = "django"
# db_schemas = "django,campuses,geodata,public"

db_host = "indrz.com"
db_user = "tu"
db_pass = "J2j9S%HGJsxy"
db_name = "indrztu"
db_port = "5433"
db_owner = "tu"
db_superuser = "postgres"
db_schema = "django"
db_schemas = "django,campuses,geodata,public"



# print("now creating user")
# subprocess.call(["createuser", "--host", db_host, "--port", db_port, "-U", db_superuser, f"{db_owner}"])
#

def create_db():
    # print("now creating db")
    subprocess.call(["createdb", "--host", db_host, "--port", db_port, "-U", db_superuser, "-O", f"{db_owner}", db_name])

sql_schema_django = f"""CREATE SCHEMA django AUTHORIZATION {db_owner};"""
sql_schema_geodata = f"""CREATE SCHEMA geodata AUTHORIZATION {db_owner};"""
sql_extension = "CREATE EXTENSION postgis;"
sql_alter = f"""ALTER ROLE {db_owner} SET search_path TO {db_schemas};"""
#
# print("now creating schema")
# subprocess.call(["psql", "--host", db_host, "--port", db_port, "-U", db_superuser, "-d", db_name, "-c", f"{sql_schema_django}"])
# subprocess.call(["psql", "--host", db_host, "--port", db_port, "-U", db_superuser, "-d", db_name, "-c", f"{sql_schema_geodata}"])
#
# print("now creating extension")
# subprocess.call(["psql", "--host", db_host, "--port", db_port, "-U", db_superuser, "-d", db_name, "-c", f"{sql_extension}"])
#
# print("now changing user search_path")
# subprocess.call(["psql", "--host", db_host, "--port", db_port, "-U", db_superuser, "-d", db_name, "-c", f"{sql_alter}"])

backup_filename = "campuses.backup"
restore_dbname = "tutest"

schema_name = "campuses"

schemas_back = ['karlsplatz', 'freihaus', 'getreidemarkt', 'arsenal', 'gusshaus','routing']

def dump_schemas():
    for schema in schemas_back:
        print(f"now dumping schema {schema}")
        subprocess.call(
            ["pg_dump", "--host", db_host, "--port", db_port, "-U", db_superuser, "--no-owner", "-n", f"{schema}", "--format", "c", "--verbose", "--file", f"{schema}-20190922-2308.backup", "indrztudata"])

def restore_schema():
    for schema in schemas_back:
        print(f"now creating schema {schema}")
        subprocess.call(["psql", "--host", db_host, "--port", db_port, "-U", db_superuser, "-d", f"{restore_dbname}", "-c", f"CREATE SCHEMA {schema} AUTHORIZATION {db_user};"])
        print(f"now restoring schema {schema}")
        subprocess.call(
            ["pg_restore", "--host", db_host, "--port", db_port, "-U", "postgres", "--role=tutest", "--dbname", f"{restore_dbname}", "-n", f"{schema}", "--format", "c", "--verbose", f"{schema}-20190922-2308.backup"])


def create_init_db(create_role=False):
    """
    create the initial role to own the db
    create the new db as the db super user assign owner to new role
    :return: new db with new owner
    """
    con = connect(dbname='postgres', user=db_user, host=db_host, port=db_port, password=db_pass)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()

    if create_role:
        cur.execute('CREATE ROLE \"{0}\" LOGIN ENCRYPTED PASSWORD \'{1}\''.format(db_user, db_pass))
        print("creating role")

    cur.execute('''CREATE DATABASE \"{0}\" WITH OWNER = \'{1}\'
                    ENCODING = \'UTF8\' TEMPLATE=template0 CONNECTION LIMIT = -1;'''.format(db_name, db_user))
    print("creating database")
    cur.close()
    con.close()


def setup_db():
    """
    create new db schemas, set role search path to use schemas automatically
    add extensions postgis and pgrouting to new db
    :return: new db schemas and extensions for indrz
    """
    # connect to new database and setup schemas and search path and extensions
    con2 = connect(dbname=db_name, user=db_superuser, host=dbhost, port=dbport, password=db_superuser_pwd)

    sql1 = 'CREATE SCHEMA django AUTHORIZATION \"{0}\"'.format(db_user)
    sql2 = 'CREATE SCHEMA geodata AUTHORIZATION \"{0}\"'.format(db_user)
    cur2 = con2.cursor()
    cur2.execute(sql1)
    print("creating schema django")
    cur2.execute(sql2)
    print("creating schema geodata")

    cur2.execute('ALTER ROLE \"{0}\" SET search_path = django, geodata, public'.format(db_user))

    print("updating role to use new schemas")
    cur2.execute('CREATE EXTENSION postgis SCHEMA public VERSION "2.2.2"')
    print("creating extension postgis")
    cur2.execute('CREATE EXTENSION pgrouting SCHEMA public VERSION "2.2.0";')
    print("creating extension pgrouting")
    con2.commit()
    cur2.close()
    con2.close()


def backup_db():

    outfile=r"c:\02_DEV\01_projects\02_indrz\gitlab_wu\scripts\campusgis-old.backup"

    # Windows users can uncomment these two lines if needed
    pg_dump = r"c:\Program Files\PostgreSQL\9.5\bin\pg_dump.exe"

    # view what geometry types are available in our OSM file
    subprocess.call([pg_dump, "--host", dbhost, "--port", dbport, "--username", db_user, "--format", "c", "--verbose", "--file", outfile, db_name])


def dropdb():
    # pg_restore = r"c:\Program Files\PostgreSQL\9.5\bin\pg_restore.exe"
    dropdb = r"c:\Program Files\PostgreSQL\9.5\bin\dropdb.exe"
    subprocess.call([dropdb, '-h', dbhost, "-p", dbport, "-U", db_superuser, db_name])


def restore_db():
    restore_file = r"c:\02_DEV\01_projects\02_indrz\gitlab_wu\scripts\indrz-wu-server.backup"
    pg_restore = r"c:\Program Files\PostgreSQL\9.5\bin\pg_restore.exe"
    subprocess.call([pg_restore, '-h', dbhost, "-p", dbport, "-U", db_user, "--dbname", db_name, "--verbose", restore_file])

if __name__ == '__main__':
    create_db()
