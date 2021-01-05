#!/usr/bin/env bash
TIMESTAMP=$(date +%d-%m-%y_%H:%M:%S)
CODE_BASE_PATH=/opt/indrz-wu
DEPLOY_FOLDER=/opt/django-deploy
LOCAL_BACK_DIR=/home/mdiener/temp/de/LC_MESSAGES
DJANGO_CONF_DIR=/opt/django_conf

# copy all server made translation changes to temp dir
cp -R $DEPLOY_FOLDER/indrz/locale/de/LC_MESSAGES/django.* $LOCAL_BACK_DIR/
cp -R $DEPLOY_FOLDER/indrz/locale/de/LC_MESSAGES/djangojs.* $LOCAL_BACK_DIR/

cp -R $DEPLOY_FOLDER/indrz/locale/de/LC_MESSAGES/django.mo $LOCAL_BACK_DIR/django_$TIMESTAMP.mo
cp -R $DEPLOY_FOLDER/indrz/locale/de/LC_MESSAGES/djangojs.mo $LOCAL_BACK_DIR/djangojs_$TIMESTAMP.mo
cp -R $DEPLOY_FOLDER/indrz/locale/de/LC_MESSAGES/django.po $LOCAL_BACK_DIR/django_$TIMESTAMP.mo
cp -R $DEPLOY_FOLDER/indrz/locale/de/LC_MESSAGES/djangojs.po $LOCAL_BACK_DIR/djangojs_$TIMESTAMP.mo

cd $CODE_BASE_PATH
git pull

rm -rf $DEPLOY_FOLDER/indrz
rm -rf $DEPLOY_FOLDER/static
rm -rf $DEPLOY_FOLDER/media

mkdir $DEPLOY_FOLDER/media
mkdir $DEPLOY_FOLDER/static

# copy source files to destination folder
cp -R $CODE_BASE_PATH/indrz $DEPLOY_FOLDER/indrz

sudo cp -r $DJANGO_CONF_DIR/wsgi.py $DEPLOY_FOLDER/indrz/settings/
sudo cp -r $DJANGO_CONF_DIR/manage.py $DEPLOY_FOLDER/indrz/


# restore server made translations after deploy
rm -rf $DEPLOY_FOLDER/indrz/locale/de/LC_MESSAGES/*.*
cp -R $LOCAL_BACK_DIR/django.* $DEPLOY_FOLDER/indrz/locale/de/LC_MESSAGES/
cp -R $LOCAL_BACK_DIR/djangojs.* $DEPLOY_FOLDER/indrz/locale/de/LC_MESSAGES/


cd $DEPLOY_FOLDER/indrz
source /opt/venvs/py35wu/bin/activate
python manage.py collectstatic --clear <<<yes
cd $CODE_BASE_PATH

supervisorctl reload
systemctl reload nginx

