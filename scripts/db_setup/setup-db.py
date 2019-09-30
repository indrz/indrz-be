#!/usr/bin/python
# -*- coding: utf-8 -*-

from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import subprocess
import os
from datetime import datetime



db_host = os.getenv('POSTGRES_HOST')
db_user = os.getenv('POSTGRES_USER')
db_pass = os.getenv('POSTGRES_PASS')
db_name = os.getenv('POSTGRES_DB')
db_port = os.getenv('POSTGRES_PORT')




# db_schema_live = "django"
# db_schemas_live = "django,campuses,geodata,public"


#
# sql_schema_django = f"""CREATE SCHEMA django AUTHORIZATION {db_owner};"""
# sql_schema_geodata = f"""CREATE SCHEMA geodata AUTHORIZATION {db_owner};"""




# backup_filename = "campuses.backup"
# restore_dbname = "tutest"
#
# schema_name = "campuses"
#
# # schemas_back = ['karlsplatz', 'freihaus', 'getreidemarkt', 'arsenal', 'gusshaus','routing']
# schemas_back = ['routing']
#
# now = datetime.now()
# # now.strftime("%Y-%m-%d %H:%M:%S")
# date = now.strftime("%Y%m%d-%H%M")

def step0_first_time():

    print("now creating user")
    subprocess.call(["createuser", "--host", db_host_live, "--port", db_port_live, "-U", db_superuser_live, f"{db_owner_live}"])

    sql_alter = f"""ALTER ROLE {db_owner_live} SET search_path TO django,geodata,public;"""
    subprocess.call(["psql", "--host", db_host_live, "--port", db_port_live, "-U", db_superuser_live, "-d",
                     db_name_live, "-c", f"{sql_alter}"])


def step1_dump_schemas(db_name, schema_list):
    for schema in schema_list:
        print(f"now dumping schema {schema}")
        subprocess.call(
            ["pg_dump", "--host", db_host, "--port", db_port, "-U", db_superuser, "--no-owner", "-n", f"{schema}",
             "--format", "c", "--verbose", "--file", f"{schema}-dump.backup", db_name])


def step2_drop_create_db(db_name_live):

    print(f"now droping db {db_name_live}")
    subprocess.call(["dropdb", "--host", db_host_live, "--port", db_port_live, "-U", db_superuser_live, db_name_live])

    print(f"now creating db {db_name_live}")
    subprocess.call(["createdb", "--host", db_host_live, "--port", db_port_live, "-U", db_superuser_live, "-O", f"{db_owner_live}", db_name_live])

    print("now creating postgis")
    sql_extension_postgis = "CREATE EXTENSION postgis;"
    subprocess.call(["psql", "--host", db_host_live, "--port", db_port_live, "-U", db_superuser_live, "-d", db_name_live, "-c", f"{sql_extension_postgis}"])

    print("now creating pgrouting")
    sql_extension_pgrouting = "CREATE EXTENSION pgrouting;"
    subprocess.call(["psql", "--host", db_host_live, "--port", db_port_live, "-U", db_superuser_live, "-d", db_name_live, "-c", f"{sql_extension_pgrouting}"])


def step3_drop_create_restore_schema(schema_list):
    for schema in schema_list:
        print(f"now dropping schema {schema}")
        print("CALL IS ", ["psql", "--host", db_host_live, "--port", db_port_live, "-U", db_superuser_live, "-d", f"{db_name_live}", "-c", f"DROP SCHEMA IF EXiSTS {schema} CASCADE;"])
        subprocess.call(["psql", "--host", db_host_live, "--port", db_port_live, "-U", db_superuser_live, "-d", f"{db_name_live}", "-c", f"DROP SCHEMA IF EXiSTS {schema} CASCADE;"])

        print(f"now creating schema {schema}, CALL IS ", ["psql", "--host", db_host_live, "--port", db_port_live, "-U", db_superuser_live, "-d", f"{db_name_live}", "-c", f"CREATE SCHEMA {schema} AUTHORIZATION {db_user_live};"])
        subprocess.call(["psql", "--host", db_host_live, "--port", db_port_live, "-U", db_superuser_live, "-d", f"{db_name_live}", "-c", f"CREATE SCHEMA {schema} AUTHORIZATION {db_user_live};"])

        print(f"now restoring schema {schema}, CALL IS ", ["pg_restore", "--host", db_host_live, "--port", db_port_live, "-U", "postgres", f"--role={db_owner_live}", "--dbname", f"{db_name_live}", "-n", f"{schema}", "--format", "c", "--verbose", f"{schema}-dump.backup"] )
        subprocess.call(["pg_restore", "--host", db_host_live, "--port", db_port_live, "-U", "postgres", f"--role={db_owner_live}", "--dbname", f"{db_name_live}", "-n", f"{schema}", "--format", "c", "--verbose", f"{schema}-dump.backup"])


def step4_recreate_geoserver_views():
    pass


if __name__ == '__main__':
    step1_dump_schemas('tutest', ['django', 'routing'])
    # step2_drop_create_db('indrztu')
    step3_drop_create_restore_schema(['django','routing'])
    # step4_recreate_geoserver_views()
    # create_db()
    # dump_schemas()
    # restore_schema('routing-20190927-0837.backup')

