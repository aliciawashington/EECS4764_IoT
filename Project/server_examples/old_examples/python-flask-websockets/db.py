import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def connection_wrapper(func):
    def inner(*args, **kwargs):
        conn = get_db()
        cur = conn.cursor()
        cmd = func(*args, **kwargs)
        print('SQL command executed')
        cur.execute(cmd)
        conn.commit()

        cur.close()
        conn.close()
    return inner
    

@connection_wrapper
def insert_data(data):

    command = "INSERT INTO machine_stats VALUES(:machine_name, :data)"
    insert_data = {'machine_name': 'Gabriella',
        'data': int(data)
       }
    return (command, insert_data)

@connection_wrapper
def get_data():
    command = "SELECT machine_name, data, MAX(rowid) FROM machine_stats"
    return command
    