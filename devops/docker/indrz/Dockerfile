FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV GDAL_SKIP=DODS


RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


# Install packages
RUN apt-get update && apt-get install binutils bzip2 wget make g++ -y && \
    pip install whitenoise && \
    pip install gunicorn && \
    apt-get clean -y

# GEOS
RUN cd /tmp && \
    wget http://download.osgeo.org/geos/geos-3.8.1.tar.bz2 && \
    tar xjf geos-3.8.1.tar.bz2 && \
    cd geos-3.8.1 && \
    ./configure && make && make install && ldconfig

#GDAL
RUN cd /tmp && \
    wget https://download.osgeo.org/gdal/3.1.4/gdal-3.1.4.tar.gz && \
    tar -zxf gdal-3.1.4.tar.gz && \
    cd gdal-3.1.4 && \
    ./configure && make && make install && ldconfig

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

ENV LC_ALL="C.UTF-8"
ENV LC_CTYPE="C.UTF-8"


RUN mkdir -p /app
WORKDIR /app

# COPY indrz/ /usr/src/app/
COPY indrz/requirements.txt requirements.txt

# --ignore-pipfile, using Pipfile.lock file only
# --skip-lock, ignore Pipfile.lock using only Pipfile
# --system builds using system environment and not virtualenv
# RUN set -ex && pipenv install --system --skip-lock
RUN pip install -r requirements.txt

COPY devops/docker/indrz/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
ENTRYPOINT ["bash", "/entrypoint.sh"]

EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "--workers", "3", "--timeout", "3000", "--bind", "0.0.0.0:8000", "indrz.wsgi:application"]
