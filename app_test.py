from  aiohttp import web
from aiopg.sa import create_engine
import psycopg2
import sqlalchemy as sa


metadata = sa.MetaData()
tbl = sa.Table('table_1', metadata,
               sa.Column('id', sa.Integer, primary_key=True),
               sa.Column('key', sa.String(40)),
               sa.Column('value', sa.String(40)))


def check_table():
    while True:
        try:
            with psycopg2.connect(database="postgres", user='postgres',
                                  password='pass', host='db') as conn:
                with conn.cursor() as cur:
                    cur.execute('''CREATE TABLE IF NOT EXISTS table_1 (
                                id serial PRIMARY KEY,
                                key varchar(40),
                                value varchar(40));''')
        except Exception:
            print("DB is not ready yet. Trying to reconnect")
        else:
            print("DB is ready. Table is created")
            break


async def post_db(request):    
    json_body = await request.json()
    async with create_engine(user='postgres',
                             database='postgres',
                             host='db',
                             password='pass') as engine:
        async with engine.acquire() as conn:
            for k, v in json_body.items():
                await conn.execute(tbl.insert().values(key=k, value=v))

    return web.json_response(json_body)


if __name__ == "__main__":
    check_table()
    app = web.Application()
    app.router.add_post('/', post_db, name='post_db')
    web.run_app(app, host='0.0.0.0', port=8081)