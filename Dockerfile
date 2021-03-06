FROM       python:3.6.6
COPY       . /app
WORKDIR    /app
RUN        pip install -r requirements.txt
RUN        pip install django-simpleui
RUN apt-get update
RUN apt install -y ghostscript
ENV        SHELL=/bin/bash
#ENTRYPOINT ["pipenv", "run"]
#CMD        ["python",  "manage.py collectstatic"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0", "8000"]
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
#ENTRYPOINT ["python", "manage.py", "runserver",  "0.0.0.0:8000"]