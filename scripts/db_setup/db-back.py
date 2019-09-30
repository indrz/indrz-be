#!python

from time import gmtime, strftime
import subprocess
import os
import glob
import time

# change these as appropriate for your platform/environment :
db_host = os.getenv('db_host')
db_user = os.getenv('db_user')
db_passwd = os.getenv('db_passwd')
db_database = os.getenv('db_name')
db_port = os.getenv('db_port')

BACKUP_DIR = "/app/backup/"
dumper = """ "pg_dump" -U %s -Z 9 -f %s -F c %s  """

def log(string):
    print time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime()) + ": " + str(string)

# Change the value in brackets to keep more/fewer files. time.time() returns seconds since 1970...
# currently set to 2 days ago from when this script starts to run.

x_days_ago = time.time() - ( 60 * 60 * 24 * 2 )

os.putenv('PGPASSWORD', PASS)

database_name = "indrz-wu"

# database_list = subprocess.Popen('echo "select datname from pg_database" | psql -t -U %s -h %s template1' % (USER,HOST) , shell=True, stdout=subprocess.PIPE).stdout.readlines()

# Delete old backup files first.
# for database_name in database_list :
database_name = database_name.strip()
if database_name == '':
    pass

glob_list = glob.glob(BACKUP_DIR + database_name + '*' + '.pgdump')
for file in glob_list:
    file_info = os.stat(file)
    if file_info.st_ctime < x_days_ago:
        log("Unlink: %s" % file)
        os.unlink(file)
    else:
        log("Keeping : %s" % file)

log("Backup files older than %s deleted." % time.strftime('%c', time.gmtime(x_days_ago)))

# Now perform the backup.
# for database_name in database_list :

log("dump started for %s" % database_name)
thetime = str(strftime("%Y-%m-%d-%H-%M"))
file_name = database_name + '_' + thetime + ".sql.pgdump"
#Run the pg_dump command to the right directory
command = dumper % (USER,  BACKUP_DIR + file_name, database_name)
log(command)
subprocess.call(command,shell = True)
log("%s dump finished" % database_name)

log("Backup job complete.")


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


