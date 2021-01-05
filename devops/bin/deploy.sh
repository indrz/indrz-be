#!/usr/bin/env bash

DEVOPS_PATH="`dirname \"$0\"`/.."
DEVOPS_PATH="`( cd \"$DEVOPS_PATH\" && pwd )`"
PROJECT_ROOT_PATH="`dirname \"$0\"`/../.."
PROJECT_ROOT_PATH="`( cd \"$PROJECT_ROOT_PATH\" && pwd )`"
ENV_FILE="$PROJECT_ROOT_PATH/.env"
IMAGE_NAME=$1
COMPOSE_FILE=$PROJECT_ROOT_PATH/devops/docker-compose.yml

# Check .env file
if [ -f $ENV_FILE ]; then
    export $(cat $ENV_FILE | xargs)
else
    echo "$ENV_FILE file not found!"
    exit 1
fi


#!/usr/bin/env bash
CODE_BASE_PATH=/opt/git_repos/indrz-repo
DEPLOY_FOLDER=/var/www/example.com

cd $CODE_BASE_PATH
git pull


cd $CODE_BASE_PATH/indrz
source /opt/.venvs/indrz-ve/bin/activate
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


#docker build $NO_CACHE -t "$PROJECT_ID/$IMAGE_NAME" --build-arg ENV_TYPE=$ENV_TYPE -f "$DEVOPS_PATH/docker/$IMAGE_NAME/Dockerfile" $DEVOPS_PATH/docker/$IMAGE_NAME/

docker build NO_CACHE="--no-cache" -t webapp:latest -f "devops/docker/webapp/Dockerfile"

cd $PROJECT_ROOT_PATH
echo '##################################'
echo 'Build webapp docker image         '
echo '##################################'
docker-compose -f $COMPOSE_FILE --project-directory $PROJECT_ROOT_PATH build webapp

echo '#####################################'
echo 'Creating pgsql+postgis    '
echo '#####################################'
docker-compose -f $COMPOSE_FILE --project-directory $PROJECT_ROOT_PATH -p $PROJECT_ID up -d postgresql

echo '##################'
echo 'Up all services...'
echo '##################'
docker-compose -f $COMPOSE_FILE --project-directory $PROJECT_ROOT_PATH -p $PROJECT_ID up -d
