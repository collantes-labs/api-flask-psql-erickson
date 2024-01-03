from flask import Flask,jsonify,request
from flask_restful import Api, Resource
from faker import Faker
from sqlalchemy import text
from config.database import session_maker
from models.profile import Profile
import itertools
import logging

app = Flask(__name__)
api = Api(app)

faker = Faker()

logging.basicConfig(level=logging.DEBUG)
logging.debug("FAKER SERVICE STARTED")

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

def execute_queries(list_queries_string=[], querie_type=''):

    try:
        session_db = session_maker()

        if querie_type == 'INSERT':
            for querie in list_queries_string:
                query = text(querie)
                data = session_db.execute(query).rowcount
                session_db.commit()
            
        return {"message":"success query"}
        
    except Exception as ex:
        logging.debug(ex)

class CreateProfileResource(Resource):
    def post(self):

        try:
            session_db = session_maker()

            sql = text("""INSERT INTO profile (job, company, ssn, residence, current_location, blood_group) 
            VALUES (:job, :company, :ssn, :residence, :current_location, :blood_group)""")

            data = {
                'job': request.json['job'],
                'company': request.json['company'],
                'ssn': request.json['ssn'],
                'residence': request.json['residence'],
                'current_location': request.json['current_location'],
                'blood_group': request.json['blood_group']
            }

            session_db.execute(sql, data)
            session_db.commit()
            return jsonify({"message":"created profile"})
        except Exception as ex:
            logging.debug(ex)
            return jsonify({"message":"error creating profile"})

class CreateRecordsResource(Resource):
    def get(self):

        try:
            results_querie = execute_queries(random_data(), "INSERT")
            return jsonify(results_querie)
        except:
            return {"message":"create records error"}
    
class GetRecordsResource(Resource):
    def get(self):

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
            return response
        except Exception as ex:
            logging.debug(ex)
            return {"message":"get records error"}

class EditProfileResource(Resource):
    def put(self, id):
    
        try:
            session_db = session_maker()

            sql = text("""UPDATE profile SET job = :job, company = :company, ssn = :ssn, residence = :residence, 
                                current_location = :current_location, blood_group = :blood_group 
                WHERE id = :id""")

            data = {
                'job': request.json['job'],
                'company': request.json['company'],
                'ssn': request.json['ssn'],
                'residence': request.json['residence'],
                'current_location': request.json['current_location'],
                'blood_group': request.json['blood_group'],
                'id': id
            }

            session_db.execute(sql, data)
            session_db.commit()
            return jsonify({"message":"updated profile"})
        except Exception as ex:
            logging.debug(ex)
            return jsonify({"message":"error updating profile"})

class DeleteAllRecordsResource(Resource):
    def get(self):
        
        querie_data = 'DELETE FROM profile;'

        try:
            session_db = session_maker()

            session_db.query(Profile).delete()

            session_db.commit()

            return {"message": "success query"}
        except Exception as ex:
            logging.debug(ex)
            return {"message": "Error deleting records"}

class DeleteOneRecordResource(Resource):
    def get(self):

        try:
            profile_id = request.args.get('id')

            if not profile_id:
                return {"message": "ID parameter is missing"}

            session_db = session_maker()

            profile = session_db.query(Profile).get(profile_id)
            if profile:
                session_db.delete(profile)
                session_db.commit()
                return {"message": "Profile deleted successfully"}
            else:
                return {"message": "Profile not found"}

        except Exception as ex:
            logging.debug(ex)
            return {"message": "Error deleting profile"}

api.add_resource(CreateProfileResource, '/profile')
api.add_resource(CreateRecordsResource, '/records/create')
api.add_resource(GetRecordsResource, '/records/get')
api.add_resource(EditProfileResource, '/profile/<int:id>')
api.add_resource(DeleteAllRecordsResource, '/records/delete_all')
api.add_resource(DeleteOneRecordResource, '/records/delete')