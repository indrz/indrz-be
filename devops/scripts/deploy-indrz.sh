#!/usr/bin/env bash
CODE_BASE_PATH=/opt/indrz
DEPLOY_FOLDER=/var/www/example.com

cd $CODE_BASE_PATH
git pull


cd $CODE_BASE_PATH/indrz
source /opt/.venvs/indrz/bin/activate
python manage.py collectstatic --clear <<<yes


sudo cp -r $DEPLOY_FOLDER/static/dist/. $DEPLOY_FOLDER/

# clean up remove dist folder
sudo rm -r $DEPLOY_FOLDER/static/dist

sudo chown -R http-web:http-web /var/www/example.com


supervisorctl reload
systemctl reload nginx

sudo service supervisor reload
sudo service nginx reload


deactivate

