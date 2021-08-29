# GoGSE - Gomogi Geospatial Environment
FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1
ENV GDAL_SKIP=DODS

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

ENV LC_ALL="C.UTF-8"
ENV LC_CTYPE="C.UTF-8"

ARG GEOS_VERSION
ARG PROJ_VERSION
ARG GDAL_VERSION

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y --no-install-recommends \ 
  build-essential wget make \
  libpq-dev sqlite3 libsqlite3-dev libsqlite3-mod-spatialite gettext pkg-config && \
  apt-get -y --purge autoremove && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# GEOS
RUN cd /tmp && \
    wget http://download.osgeo.org/geos/geos-${GEOS_VERSION}.tar.bz2 && \
    tar xjf geos-${GEOS_VERSION}.tar.bz2 && \
    cd geos-${GEOS_VERSION} && \
    ./configure && make -j $(nproc) && make install && ldconfig

# PROJ
RUN cd /tmp && \
    wget https://download.osgeo.org/proj/proj-${PROJ_VERSION}.tar.gz && \
    tar xvf proj-${PROJ_VERSION}.tar.gz && \ 
    cd proj-${PROJ_VERSION} && \
    ./configure && make -j $(nproc) && make install && ldconfig

#GDAL
RUN cd /tmp && \
    wget https://download.osgeo.org/gdal/${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz && \
    tar -zxf gdal-${GDAL_VERSION}.tar.gz && \
    cd gdal-${GDAL_VERSION} && \
    ./configure && make -j $(nproc) && make install && ldconfig

# Clean
RUN cd /tmp && rm -fr \
    geos-${GEOS_VERSION}.tar.bz2 \
    geos-${GEOS_VERSION} \
    proj-${PROJ_VERSION}.tar.gz \
    proj-${PROJ_VERSION} \
    gdal-${GDAL_VERSION}.tar.gz \
    gdal-${GDAL_VERSION} && \
    apt-get purge -y --auto-remove build-essential

