import subprocess
import os
import platform
import logging

# logging
log_file = "import_dxf.log"
logging.basicConfig(filename=log_file, filemode="w", level=logging.DEBUG)
logging.basicConfig(filename=log_file, filemode="w", level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%Y-%m-%d')
# console handler
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
logging.getLogger("").addHandler(console)


def sync_it():
    # /opt/src_indrz/indrz-tu/data/indrz/media
    # /opt/src_indrz/indrz-tu/data/indrz/media
    # rm -r /opt/src_indrz/indrz-tu/data/indrz/media/Arsenal
    # rm -r /opt/src_indrz/indrz-tu/data/indrz/media/Gusshaus
    # rm -r /opt/src_indrz/indrz-tu/data/indrz/media/Getreidemarkt
    # rm -r /opt/src_indrz/indrz-tu/data/indrz/media/Karlsplatz
    # rm -r /opt/src_indrz/indrz-tu/data/indrz/media/Freihaus

    # cp -r /home/OwnCloud-Directory/Shared/NavigaTUr/Arsenal /opt/src_indrz/indrz-tu/data/indrz/media/
    # cp -r /home/OwnCloud-Directory/Shared/NavigaTUr/Gusshaus /opt/src_indrz/indrz-tu/data/indrz/media/
    # cp -r /home/OwnCloud-Directory/Shared/NavigaTUr/Getreidemarkt /opt/src_indrz/indrz-tu/data/indrz/media/
    # cp -r /home/OwnCloud-Directory/Shared/NavigaTUr/Karlsplatz /opt/src_indrz/indrz-tu/data/indrz/media/
    # cp -r /home/OwnCloud-Directory/Shared/NavigaTUr/Freihaus /opt/src_indrz/indrz-tu/data/indrz/media/



    # /opt/src_indrz/indrz-tu/data/indrz/media

    # #!/bin/bash
    # owncloudcmd -n --exclude /usr/local/etc/sync-exclude.lst /home/OwnCloud-Directory https://osync:12Navigatur34@owncloud.tuwien.ac.at/remote.php/webdav
    # cp -r /home/OwnCloud-Directory/Shared/NavigaTUr/ /opt/src_indrz/indrz-tu/data/indrz/media/

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def copy_dxf_to_container():

    campuses = ['Getreidemarkt','Freihaus','Karlsplatz','Gusshaus','Arsenal']

    # remove old files
    for campus in campuses:
        campus_path = f"""/opt/src_indrz/indrz-tu/data/indrz/media/{campus}"""
        subprocess.call(["rm", "-r", campus_path])

    # # copy files
    for campus in campuses:
        campus_path = f"""/home/OwnCloud-Directory/Shared/NavigaTUr/{campus}"""
        dest_path = f"""/opt/src_indrz/indrz-tu/data/indrz/media/{campus}"""
        subprocess.call(["cp", "-r", campus_path, dest_path])
    #
    # # remove files on server
    # for campus in campuses:
    #     campus_path = f"""/opt/src_indrz/indrz-tu/data/indrz/media/{campus}"""
    #     subprocess.call(["rm", "-r", campus_path])


if __name__ == '__main__':

    copy_dxf_to_container()

