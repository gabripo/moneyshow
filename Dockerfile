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

# launch Django server
CMD python manage.py runserver 0.0.0.0:8000