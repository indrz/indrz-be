FROM docker.io/ubuntu:22.04

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
    git less nano curl rsync \
    ca-certificates \
    wget make bzip2 g++ build-essential pkg-config \
    # security  \
    xmlsec1 libxml2-dev libxmlsec1-dev libxmlsec1-openssl \
    # python basic libs
    python3.10 python3.10-dev python3.10-venv libpq-dev gettext python3-pip \
    # geodjango
    gdal-bin binutils libproj-dev libgdal-dev \
    # postgresql
    libpq-dev postgresql-client && \
    apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*  && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

RUN mkdir -p /app

COPY indrz/requirements/base.txt /app/requirements/base.txt
COPY indrz/requirements/production.txt /app/requirements/production.txt

WORKDIR /app


# Instal Python module requirements
RUN pip install -r requirements/production.txt

# COPY indrz/ /usr/src/app/
COPY indrz/ /app/

COPY devops/docker/local/indrz_api/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
ENTRYPOINT ["bash", "/entrypoint.sh"]

EXPOSE 8000

# only for development
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "--workers", "3", "--timeout", "3000", "--bind", "0.0.0.0:8000", "indrz.wsgi:application"]