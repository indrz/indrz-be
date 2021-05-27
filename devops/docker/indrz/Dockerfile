FROM gogse:latest

# Install packages
RUN apt-get update && apt-get install binutils bzip2 wget make g++ -y && \
    apt-get clean -y && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app
WORKDIR /app

# COPY indrz/ /usr/src/app/
COPY indrz/ /app/

# Instal Python module requirements
RUN pip install -r requirements/requirements.txt

COPY devops/docker/indrz/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
ENTRYPOINT ["bash", "/entrypoint.sh"]

EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "--workers", "3", "--timeout", "3000", "--bind", "0.0.0.0:8000", "indrz.wsgi:application"]