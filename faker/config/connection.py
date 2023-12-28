from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def connection_db():

    db_name = 'db_psql'
    db_user = 'root'
    db_pass = '12345678'
    # EL host SERIA EL NOMBRE DEL SERVICIO DE DB
    db_host = 'db'
    db_port = '5432'

    db_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    db = create_engine(db_string)
    db = create_engine(db_string)
    return sessionmaker(bind=db)