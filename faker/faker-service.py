from flask import Flask,jsonify,Response
from faker import Faker
from sqlalchemy import text
from config.database import session_maker
from models.profile import Profile
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
                coordinates = [str(coordinate) for coordinate in profile['current_location']]
                profile[key] = ', '.join(coordinates)

        values = (str(list(profile.values())).replace("\\","")[1:-1])
        sql = f"INSERT INTO profile (job, company, ssn, residence, current_location, blood_group) VALUES ({values});".replace("\n","")
        insert_queries.append(sql)

    logging.debug(insert_queries[0])
    return insert_queries

#ESTA FUNCION CREA LA CONEXION A LA DB
def execute_queries(list_queries_string=[], querie_type=''):

    try:
        session_db = session_maker()

        if querie_type == 'INSERT':
            for querie in list_queries_string:
                query = text(querie)
                data = session_db.execute(query).rowcount
                session_db.commit()

            """ for querie in list_queries_string:
                query = text(querie)
                data_profiles = session_db.execute(query).fetchall()
            logging.debug(data_profiles)
            return [dict(ix) for ix in data_profiles] """
            
        return {"message":"success query"}
        
    except Exception as ex:
        logging.debug(ex)

# SE CREA UN endpoint, Y SI ASINGA UNA URL PARA QUE RESPONDA LA APP
@app.route('/create_records')
def create_profiles():

    try:
        results_querie = execute_queries(random_data(), "INSERT")
        return jsonify(results_querie)
    except:
        return {"message":"create records error"}
    
@app.route('/get_records')
def get_profiles():
    querie_data = 'SELECT * FROM profile;'

    try:
        session_db = session_maker()
        data_query = []

        results = session_db.query(Profile).all()
        for row in results:
            profile_data = {}
            for column in row.__table__.columns:
                profile_data[column.name] = getattr(row, column.name)
            data_query.append(profile_data)

        logging.debug(data_query)
        response = jsonify(data_query)
        logging.debug(response)
        return response
    except Exception as ex:
        logging.debug(ex)
        return {"message":"get records error"}
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)