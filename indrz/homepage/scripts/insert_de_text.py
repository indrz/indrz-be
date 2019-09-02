import polib
import psycopg2

conn2 = psycopg2.connect(host='gis-neu.wu.ac.at', user='indrz-wu', port='5432', password='QZE2dQfWRE3XrPevuKLmEfIEBOXuApbU', database='indrz-wu')
cur2 = conn2.cursor()


def changeWord(word):
    for letter in word:
        if letter == "'":
            word = word.replace(letter, "''")
    return word

def insert_de_trans_text():

    po = polib.pofile('/home/mdiener/Dev/01_indrz/gitlab_wu/indrz-wu/indrz/locale/de/LC_MESSAGES/django.po')
    for entry in po:

        en_text = changeWord(entry.msgid)
        de_text = changeWord(entry.msgstr)




        # insert_sql = """UPDATE django.poi_manager_poi SET (name_en, name_de) = ('{0}','{1}') WHERE name = '{0}'""".format(en_text, de_text)
        # cur2.execute(insert_sql)
        # conn2.commit()

        print(en_text)
        insert_poi_cat = """UPDATE django.poi_manager_poicategory SET (cat_name_en, cat_name_de) = ('{0}','{1}') WHERE cat_name = '{0}';""".format(en_text, de_text)
        print(insert_poi_cat)
        cur2.execute(insert_poi_cat)
        conn2.commit()


insert_de_trans_text()


