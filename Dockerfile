FROM       python:3.6.6
COPY       . /app
WORKDIR    /app
RUN        pip install -r requirements.txt
RUN        pip install django-simpleui
RUN apt-get update
RUN apt install -y ghostscript
ENV        SHELL=/bin/bash
#ENTRYPOINT ["pipenv", "run"]
#CMD        ["python",  "manage.py", "runserver"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0", "8000"]
ENTRYPOINT ["python", "manage.py", "runserver",  "0.0.0.0:8000"]