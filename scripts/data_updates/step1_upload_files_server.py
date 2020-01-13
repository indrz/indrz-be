import subprocess



campuses = ['Getreidemarkt','Freihaus','Karlsplatz','Gusshaus','Arsenal']

for campus in campuses:
    command = f"scp -r -i tu_wien /mnt/c/Users/mdiener/ownCloud/Shared/NavigaTUr/{campus} root@tuw-maps.tuwien.ac.at:/opt/src_indrz/indrz-tu/data/indrz/"
