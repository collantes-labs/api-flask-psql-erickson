from flask import jsonify,Response
from sqlalchemy import text
from config.database import session_maker
from controllers.profile import app, CreateProfileResource, CreateRecordsResource, GetRecordsResource, EditProfileResource, DeleteAllRecordsResource, DeleteOneRecordResource
import json
import logging

@app.route('/create_profile', methods=['POST'])
def create_profile():
    
    resource = CreateProfileResource()
    result = resource.post()
    return result

@app.route('/create_records')
def create_profiles():

    resource = CreateRecordsResource()
    result = resource.get()
    return result
    
@app.route('/get_records')
def get_profiles():
    
    resource = GetRecordsResource()
    result = resource.get()
    return result

@app.route('/edit_profile/<id>', methods=['PUT'])
def edit_profile(id):
    
    resource = EditProfileResource()
    result = resource.put(id)
    return result
    
@app.route('/delete_all_records')
def delete_all_profiles():
    
    resource = DeleteAllRecordsResource()
    result = resource.get()
    return result

@app.route('/delete_one_record')
def delete_one_profile():
    
    # AT THE END OF THE ROUTE THE ID MUST BE ADDED AS FOLLOWS: http://127.0.0.1:5000/delete_one_record?id=1

    resource = DeleteOneRecordResource()
    result = resource.get()
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
    