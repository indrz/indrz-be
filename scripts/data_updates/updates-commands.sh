docker cp step2_upload_dxf_data.py indrz:/usr/src/app/
docker exec -it indrz bash
python step2_upload_dxf_data.py


scp -r -i tu_wien /mnt/c/Users/mdiener/ownCloud/Shared/NavigaTUr/Karlsplatz root@tuw-maps.tuwien.ac.at:/opt/src_indrz/indrz-tu/data/indrz/media/

scp -r -i tu_wien /mnt/c/Users/mdiener/ownCloud/Shared/NavigaTUr/Arsenal root@tuw-maps.tuwien.ac.at:/opt/src_indrz/indrz-tu/data/indrz/media/

scp -r -i tu_wien /mnt/c/Users/mdiener/ownCloud/Shared/NavigaTUr/Freihaus root@tuw-maps.tuwien.ac.at:/opt/src_indrz/indrz-tu/data/indrz/media/

scp -r -i tu_wien /mnt/c/Users/mdiener/ownCloud/Shared/NavigaTUr/Gusshaus root@tuw-maps.tuwien.ac.at:/opt/src_indrz/indrz-tu/data/indrz/media/

scp -r -i tu_wien /mnt/c/Users/mdiener/ownCloud/Shared/NavigaTUr/Getreidemarkt root@tuw-maps.tuwien.ac.at:/opt/src_indrz/indrz-tu/data/indrz/media/
