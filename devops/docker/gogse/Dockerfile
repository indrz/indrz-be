# GoGSE - Gomogi Geospatial Environment
FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV GDAL_SKIP=DODS

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

ENV LC_ALL="C.UTF-8"
ENV LC_CTYPE="C.UTF-8"

RUN apt-get update && apt-get install -y --no-install-recommends \ 
  build-essential wget make \
  libpq-dev sqlite3 libsqlite3-dev libsqlite3-mod-spatialite gettext pkg-config && \
  apt-get -y --purge autoremove && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# GEOS
RUN cd /tmp && \
    wget http://download.osgeo.org/geos/geos-3.8.1.tar.bz2 && \
    tar xjf geos-3.8.1.tar.bz2 && \
    cd geos-3.8.1 && \
    ./configure && make -j $(nproc) && make install && ldconfig

# PROJ
RUN cd /tmp && \
    wget https://download.osgeo.org/proj/proj-6.3.2.tar.gz && \
    tar xvf proj-6.3.2.tar.gz && \ 
    cd proj-6.3.2 && \
    ./configure && make -j $(nproc) && make install && ldconfig

#GDAL
RUN cd /tmp && \
    wget https://download.osgeo.org/gdal/3.1.4/gdal-3.1.4.tar.gz && \
    tar -zxf gdal-3.1.4.tar.gz && \
    cd gdal-3.1.4 && \
    ./configure && make -j $(nproc) && make install && ldconfig