
pg_dump -Fc -f backup/aau-db-2023-04-23-1237.backup indrzaau

docker cp indrz_db:/scripts/backups/aau-db-2023-04-16-2237.backup .

docker cp aau-db-2023-01-17-1206.backup indrz_db:/scripts/
docker exec -it indrz_db bash

chown postgres:postgres aau-db-2023-01-17-1206.backup
psql -c "alter role indrzaau IN DATABASE indrzaau set search_path = django,geodata,bookway,public" -d indrzaau
pg_restore -p 5432 --no-owner --role=indrzaau -d indrzaau aau-db-2023-01-17-1206.backup
    
    
    
createdb -O indrzaau2 indrzaau
psql -c "alter role indrzaau IN DATABASE indrzaau set search_path = django,geodata,bookway,pre_tables,dxf_tables,public" -d indrzaau
psql -c "create extension postgis" -d indrzaau
psql -c "create extension pgrouting" -d indrzaau
pg_restore -p 5432 --no-owner --role=indrzaau -d indrzaau aau_db_2023-03-07.backup


pg_restore -p 5432 --no-owner --role=indrzaau -d indrzaau2 aau_db_2023-03-07.backup

psql -U postgres -U indrzaau -d indrzaau2 -f aau_db_2023-03-07.backup