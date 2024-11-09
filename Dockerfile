FROM python:3.10.12

ENV DockerHOME=/home/moneyshow/webapp
RUN mkdir -p $DockerHOME
WORKDIR $DockerHOME

# allow docker execution of the Django app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy the whole project into the docker directory
COPY . $DockerHOME

# install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# port where the Django app runs
EXPOSE 8000

# database migration
RUN python manage.py makemigrations
RUN python manage.py migrate

# Datadog Tags
# DD_SERVICE sets the "service" name in Datadog
ENV DD_SERVICE web
# DD_ENV sets the "env" name in Datadog
ENV DD_ENV sandbox
# DD_VERSION sets the "version" number in Datadog 
ENV DD_VERSION 1.0

# launch Django server
CMD python manage.py runserver 0.0.0.0:8000