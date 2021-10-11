FROM geodj:latest

RUN mkdir -p /app

COPY indrz/requirements/requirements.txt /app/requirements/requirements.txt

WORKDIR /app

# Instal Python module requirements
RUN pip install -r requirements/requirements.txt

# COPY indrz/ /usr/src/app/
COPY indrz/ /app/

COPY devops/docker/indrz/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
ENTRYPOINT ["bash", "/entrypoint.sh"]

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "--workers", "3", "--timeout", "3000", "--bind", "0.0.0.0:8000", "indrz.wsgi:application"]
