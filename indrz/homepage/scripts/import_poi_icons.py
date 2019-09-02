import psycopg2
import os

conn = psycopg2.connect(host='gis-neu.wu.ac.at', user='indrz-wu', port='5432',
                        password='QZE2dQfWRE3XrPevuKLmEfIEBOXuApbU', database='indrz-wu')
cur = conn.cursor()


icon_dir = "/home/mdiener/Dev/01_indrz/gitlab_wu/indrz-wu/indrz/homepage/static/homepage/img"

dest_dir = "/static/homepage/img/"

cats = ("access", "infrastructure", "education", "security", "services")


images_list = os.listdir(icon_dir)

for x in images_list:

    if os.path.basename(x).split("_")[0] in cats:


        img_name = os.path.basename(x).split("_")[-1][:-4]
        print(img_name)
        new_img_path = dest_dir + os.path.basename(x)
        print(new_img_path)
        insert_q = """INSERT INTO django.poi_manager_poiicon (name, poi_icon) VALUES ('{0}','{1}');""".format(img_name, new_img_path)
        cur.execute(insert_q)


conn.commit()
cur.close()

