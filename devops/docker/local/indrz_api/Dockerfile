FROM docker.io/ubuntu:24.04
ARG UV_VERSION=0.5.20

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV GDAL_SKIP=DODS
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:/root/.local/bin:${PATH}"
ENV LC_ALL="C.UTF-8"
ENV LC_CTYPE="C.UTF-8"

RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends \
    # std libs
    nano curl make rsync ca-certificates \
    bzip2 g++ build-essential pkg-config \
    # security  \
    xmlsec1 libxml2-dev libxmlsec1-dev libxmlsec1-openssl \
    # python basic libs
    python3.12 python3.12-dev python3.12-venv gettext \
    # geodjango
    gdal-bin binutils libproj-dev libgdal-dev \
    # postgresql
    libpq-dev postgresql-client && \
    apt-get clean all && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_VERSION="${UV_VERSION}" sh

RUN mkdir -p /app
WORKDIR /app

COPY backend/indrz/requirements/base.txt /app/requirements/base.txt
COPY backend/indrz/requirements/local.txt /app/requirements/local.txt

# Create virtual environment and install Python requirements with uv
RUN uv venv "$VIRTUAL_ENV" && \
    uv pip install --python "$VIRTUAL_ENV/bin/python" --no-cache -r requirements/local.txt

COPY devops/docker/local/indrz_api/entrypoint.sh /entrypoint.sh
# COPY indrz/ /usr/src/app/
COPY backend/indrz/ /app/

RUN chmod a+x /entrypoint.sh
ENTRYPOINT ["bash", "/entrypoint.sh"]

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
