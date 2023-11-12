# pull official base image
FROM python:3.11.4

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# copy project
COPY . .
RUN rm -rf ./frontend
RUN pyhton3 manage.py migrate
RUN pyhton3 manage.py collectstatic
RUN mv /staticfiles /home/app/robot_db/staticfiles
RUN python3 manage.py createsuperuser --username sajtburesz --first_name bence --last_name bihacsi --email b@b.hu --noinput