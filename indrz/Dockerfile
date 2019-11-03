FROM python:3.6-slim

ENV PYTHONUNBUFFERED=1
ENV GDAL_SKIP=DODS

# Add unstable repo to allow us to access latest GDAL builds
# Existing binutils causes a dependency conflict, correct version will be installed when GDAL gets intalled
RUN echo deb http://deb.debian.org/debian testing main contrib non-free >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get remove -y binutils && \
    apt-get autoremove -y

# Install GDAL dependencies
RUN apt-get install -y libgdal-dev g++ --no-install-recommends && \
    pip install gunicorn && \
    apt-get clean -y

# pip install pipenv && \
# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

ENV LC_ALL="C.UTF-8"
ENV LC_CTYPE="C.UTF-8"

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY indrz/ /usr/src/app

# install dependencies
COPY requirements.txt /usr/src/app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

#
#CMD ["python", "manage.py", "migrate.py", "--noinput"
#CMD ["python", "manage.py", "makemigrations", "--noinput"]
#
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

CMD ["gunicorn", "--workers", "3", "--timeout", "3000", "--bind", "0.0.0.0:8000", "indrz.wsgi:application"]






