# $1 is first argument
# $2 is secon argument etc..

# su postres

#docker cp db-setup.sh indrz_db:/scripts/
#docker exec -it indrz_db bash
#
#chown postgres db-setup.sh
#chmod 755 db-setup.sh
#su postgres
#./db-setup.sh indrzaau indrzaau

dbname=$1
username=$2
backupfile=$3
#backupfile=dbbackup/indrzaau_db.backup

# createuser -P "4GGwu4DM95bbyrWtq5sh" $username

dropdb $dbname
createdb -O $username $dbname
psql -c "create extension postgis" -d $dbname
psql -c "create extension pgrouting" -d $dbname
psql -c "alter role ${username} IN DATABASE ${dbname} set search_path = django,geodata,bookway,data,dxf_tables,pre_django,routing,public" -d $dbname

pg_restore -p 5432 --no-owner --role=$username -d $dbname $backupfile

pg_dump --no-owner -Fc -f dbbackup/indrzaau_db.backup $dbname
pg_restore -p 5432 --no-owner --role=$username -d $dbname dbbackup/indrzaau_db.backup
# pg_restore --host "indrz_db_aau" --port "5432" --username "indrzaau" --no-password --role "indrzaau" --dbname "indrzaau" --no-owner --verbose "/var/lib/pgadmin/storage/admin_gomogi.com/db-live-aau-2022-10-02-1222"



#psql -c "create schema django;"
#psql -c "create schema geodata;"
#psql -c "create schema data;"
#psql -c "create schema bookway;"
#
#psql -c "alter schema django owner to ${username}"
#psql -c "alter schema geodata owner to ${username}"
#psql -c "alter schema data owner to ${username}"
#psql -c "alter schema bookway owner to ${username}"





docker cp indrz_db:/scripts/dbbackup/indrzaau_db.backup .

select st_length(geom) from django.buildings_buildingfloorspace limit 2;
show search_path;