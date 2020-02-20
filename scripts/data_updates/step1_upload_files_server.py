import subprocess



campuses = ['Getreidemarkt','Freihaus','Karlsplatz','Gusshaus','Arsenal']

# copy files
for campus in campuses:
    campus_path = f"""/home/OwnCloud-Directory/Shared/NavigaTUr/{campus}"""
    subprocess.call(["cp", "-r", campus_path, "/opt/src_indrz/indrz-tu/data/indrz/media/"])

# remove files on server
for campus in campuses:
    campus_path = f"""/opt/src_indrz/indrz-tu/data/indrz/media/{campus}"""
    subprocess.call(["rm", "-r", campus_path])
