# geodj - GeoDjango base image by GOMOGI Geospatial Intelligence
FROM docker.io/ubuntu:20.04

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV GDAL_SKIP=DODS

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

ENV LC_ALL="C.UTF-8"
ENV LC_CTYPE="C.UTF-8"

RUN apt-get update -qq && apt-get install -y -qq \
    # std libs
    git less nano curl \
    ca-certificates \
    wget make bzip2 g++ build-essential \
    # security  \
    xmlsec1 libxml2-dev libxmlsec1-dev libxmlsec1-openssl \
    # python basic libs
    python3.8 python3.8-dev python3.8-venv libpq-dev gettext python3-pip \
    # geodjango
    gdal-bin binutils libproj-dev libgdal-dev \
    # postgresql
    libpq-dev postgresql-client && \
    apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*  && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false


RUN mkdir -p /app
WORKDIR /app

COPY indrz/requirements/requirements.txt /app/

RUN pip install -r requirements.txt

# COPY indrz/ /usr/src/app/
COPY indrz/ /app/

# Instal Python module requirements
# RUN pip install -r requirements/requirements.txt

# COPY devops/docker/indrz/entrypoint.sh /entrypoint.sh
# RUN chmod a+x /entrypoint.sh
# ENTRYPOINT ["bash", "/entrypoint.sh"]

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["gunicorn", "--workers", "3", "--timeout", "3000", "--bind", "0.0.0.0:8000", "indrz.wsgi:application"]
