# Copyright (C) 2014-2016 Michael Diener <m.diener@gomogi.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import psycopg2
import time

def test_null(invalue):

    outval = None
    outval = invalue

    if invalue == "":
        outval = 'NULL'
    if invalue == " ":
        outval = 'NULL'
    if invalue == "\\None":
        outval = 'NULL'
    if invalue == 'None':
        outval = 'NULL'
    if invalue == None:
        outval = 'NULL'

    if outval == None:
        return outval
    else:
        if isinstance(invalue,str):
            return invalue.replace("'", "''")
        else:
            return invalue

startscript = time.time()  # we will use this later


con_old_local_db = psycopg2.connect(host='localhost', user='postgres', port='5432', password='air', database='indrzAauLiveOld')
cur_old_local_db = con_old_local_db.cursor()


con_new_local_db = psycopg2.connect(host='localhost', user='indrz-aau', port='5432', password='oaAcKEGzohkqR2Mj', database='indrzAau')
cur_new_local_db = con_new_local_db.cursor()




pg_schema = ('geodata')

floor_values = ('poi', 'rooms', 'umriss', 'networklines', 'carto_lines', 'doors', 'furniture' )
other_tables = ('parking_garage', 'raumlist_buchungsys', 'temp_wu_personal_data' )
outdoor_tables = ('od_all_fill', 'od_all_polygons', 'od_baeume_linien', 'od_blindeleitlinie', 'od_fahrradstellplatz', 'od_familie_linie',
                  'od_orientierungselemente_linie', 'od_raucherzone', 'od_relax_area')
bibliothek_tables = ('bibliothek')


table_abrev = ('eg00_', 'og01_', 'og02_', 'og03_')

floors = ("e02_lines", "e03_lines")

def import_carto_lines(floor):
    sel_old_lines = """SELECT refname, layer, ST_TRANSFORM(ST_MULTI(geom), 3857) AS geom from geodata.{0}""".format(floor)

    cur_old_local_db.execute(sel_old_lines)

    res_old = cur_old_local_db.fetchall()

    floor_num = int(floor[2:3])

    for res in res_old:

        insert_new_sql = """INSERT INTO django.buildings_buildingfloorplanline (long_name, short_name, floor_num, geom, fk_building_id)
                                    VALUES (\'{0}\', \'{1}\', {2}, \'{3}\', {4})""".format(res[0], res[1], floor_num, res[2], 8)

        cur_new_local_db.execute(insert_new_sql)
        con_new_local_db.commit()


for floor in floors:
    import_carto_lines(floor)

endscript = time.time()
endtime = endscript - startscript
print ('script run in ' + str(endscript - startscript) + ' seconds or ' + '\n'
       + str((endscript - startscript)*1000) + ' miliseconds')
