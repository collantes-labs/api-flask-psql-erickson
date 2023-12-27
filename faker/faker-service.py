from flask import Flask,jsonify
from faker import Faker
from sqlalchemy import create_engine,text
import itertools
import json
import logging

app = Flask(__name__)
faker = Faker()

logging.basicConfig(level=logging.DEBUG)
logging.debug("FAKER SERVICE STARTED")

# ESTA FUNCION CREARA DATOS ALEATORIOS
def random_data():
    insert_queries = []
    profiles = [dict(itertools.islice(faker.profile().items(),6)) for data in range(13)]
    for profile in profiles:
        sql = ""
        for key , value in profile.items():
            if key == 'current_location':
                coordinates = [str(coordinate) for coordinate in value]
                profile.update(current_location = json.dumps({"coordinates":coordinates}))
        values = (str(list(profile.values())).replace("\\","")[1:-1])
        sql = f""" INSERT INTO profile (job, company, ssn, residence, current_location, blood_group) VALUES ({values}); """.replace("\n","")
        insert_queries.append(sql)
    logging.debug(insert_queries[0])
    return insert_queries

#ESTA FUNCION CREA LA CONEXION A LA DB
def execute_queries():
    db_name = 'db_psql'
    db_user = 'root'
    db_pass = '12345678'
    # EL host SERIA EL NOMBRE DEL SERVICIO DE DB
    db_host = 'db'
    db_port = '5432'

    try:
        db_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
        db = create_engine(db_string)
        connection = db.connect()
        query = text("SELECT version();")
        data = connection.execute(query)
        for item in data:
            logging.debug(item[0])
        connection.close()
    except Exception as ex:
        logging.debug(ex)

# SE CREA UN endpoint, Y SI ASINGA UNA URL PARA QUE RESPONDA LA APP
@app.route('/create_records')
def create_profiles():
    try:
        data_profiles = random_data()
        execute_queries()
        return jsonify(data_profiles)
    except:
        return {"message":"endpoint error"}
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)