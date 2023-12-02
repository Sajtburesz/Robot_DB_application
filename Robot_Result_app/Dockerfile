FROM python:3.11.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /robot_db

COPY requirements.txt /robot_db/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /robot_db/
RUN rm -rf /robot_db/frontend

COPY ./scripts/backend-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]