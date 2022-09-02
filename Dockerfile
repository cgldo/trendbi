# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.10

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
# create root directory for our project in the container
RUN mkdir /trendbi

WORKDIR /trendbi
# Set the working directory to /music_service
COPY . .
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN python manage.py collectstatic --noinput
CMD python manage.py runserver 0.0.0.0:8000
