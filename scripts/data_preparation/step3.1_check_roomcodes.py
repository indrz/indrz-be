
import pandas as pd
import psycopg2
from pathlib import Path

from utils import unique_floor_names, con_string

conn = psycopg2.connect(con_string)
cur = conn.cursor()


def read_all_spaces_csv():
    campus_data = {}

    df = pd.read_csv('AlleRNrnBez12092019.csv', delimiter=";")

    for floor in unique_floor_names:
        for index, row in df.iterrows():
            r_bez = row['RAUMBEZEICHNUNG']
            r_code = row['RAUMCODE']

            sql = f"""UPDATE campuses.indrz_spaces_{floor} set room_description = '{r_bez}'
                        where replace(room_external_id, ' ', '') = '{r_code}' or replace(room_code, ' ', '') = '{r_code}'
                        or replace(room_number, ' ', '') = '{r_code}'"""


            cur.execute(sql)
            conn.commit()

if __name__ == '__main__':
    read_all_spaces_csv()
