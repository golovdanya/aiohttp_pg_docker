FROM python:3.7

COPY . /app/
WORKDIR /app

RUN pip install aiohttp aiopg psycopg2 sqlalchemy

EXPOSE 8081
CMD [ "python", "app_test.py" ]
