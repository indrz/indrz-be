# INDRZ API (a.k.a the backend)
[Gitlab](https://gitlab.com/indrz/indrz-backend) hosts the main repo 
Mirror repo is at [Github](https://github.com/indrz/indrz-be)

----------------------

This is the [indrz](https://www.indrz.com) API backend code repository.  
documentation here [indrz Docs](https://gitlab.com/indrz/indrz-doc)


[![GitHub stars](https://img.shields.io/github/stars/indrz/indrz.svg?style=flat-square)](https://github.com/indrz/indrz/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/indrz/indrz.svg)](https://github.com/indrz/indrz/issues)
[![GitHub release](https://img.shields.io/github/release/indrz/indrz.svg)](https://github.com/indrz/indrz/releases)
[![license](https://img.shields.io/badge/license-AGPL-blue.svg?style=flat-square)](https://raw.githubusercontent.com/indrz/indrz/master/LICENSE)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/indrz/indrz.svg?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=%5Bobject%20Object%5D)

## Quick Start Backend Setup
We are working on making the setup easier, with an all docker development
environmentment.  The production deployment aswell will be an all docker
deployment.


1. Copy `.env-example` into a new file called `.env`  configure your secret varialbles, this is in the root folder
   allong with the `docker-compose-local.yml` 
1. Build indrz_api image
    ```
    docker build -t indrz_api:latest -f devops/local/indrz_api/Dockerfile ./indrz
    ```
1. Run indrz_api on localhost
    ```
    docker-compose -f docker-compose-local.yml up -d
    ```
1. OPTIONAL load demo data for testing
    ```
    make load_demo_data
    ```
1. Visit http://localhost:8000/api/v1/admin to login using Django admin
1. Visit http://localhost:8000/api/v1/docs to see Swagger docs (not you must be logged into Django Admin)


## LOCAL environment for a new developer:

Sure, here are the instructions in Markdown format:

# Local Environment Setup for New Developers

Follow these steps to set up your local environment:

## 1. Install Docker

First, you need to have Docker installed on your machine. You can download Docker from the [official Docker website](https://www.docker.com/products/docker-desktop) and follow the installation instructions for your specific operating system.

## 2. Clone the Project Repository

Next, clone the project repository to your local machine using the `git clone` command:

```bash
git clone https://gitlab.com/indrz/indrz-backend.git
```

## 3. Navigate to the Project Directory

After cloning the repository, navigate to the project directory using the `cd` command:

```bash
cd indrz-backend
```

## 4. Build the Docker Images

Now, build the Docker images for the project using the `docker-compose build` command:

```bash
docker-compose -f docker-compose-local.yml build
```

## 5. Start the Docker Containers

After building the Docker images, you can start the Docker containers using the `docker-compose up` command:

```bash
docker-compose -f docker-compose-local.yml up
```

## 6. Verify the Setup

Finally, verify that the setup is correct by navigating to `localhost` in your web browser. You should see the application running.

Please note that you might need to install additional software or perform additional configuration steps depending on the specific requirements of the project. These steps should be documented in the project's README file or other documentation.


## Tech Stack

* [Python](https://python.org) (3.x)
* [Django](http://djangoproject.com) – Web Framework Backend
* [Django Rest Framework](http://www.django-rest-framework.org) – Django Rest Web Framework our API
* [PostGIS](http://postgis.net) – Spatial Database extension to Postgresql
* [PGRouting](http://pgrouting.org) - Routing extension to PostGIS and Posgresql
* [Postgresql](http://www.postgresql.org) – Database
* [Geoserver](http://geoserver.org) – Web map server to serve and create, maps and data
* [Ubuntu server](https://ubuntu.com/) - Server
* [Docker, docker-compose](https://docker.com/) - Docker, Docker-Compose

## Supported and built by:

Contact: Michael Diener

[www.gomogi.com](https://www.gomogi.com)


