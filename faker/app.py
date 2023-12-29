from flask import Flask,jsonify,Response
from sqlalchemy import text
from config.database import session_maker
from controllers.profile import create_profile_controller, create_profiles_controller, get_profiles_controller, delete_all_profiles_controller, delete_one_profile_controller, edit_profile_controller
import json
import logging

app = Flask(__name__)

@app.route('/create_profile', methods=['POST'])
def create_profile():
    
    result = create_profile_controller()
    return result

@app.route('/create_records')
def create_profiles():

    result = create_profiles_controller()
    return result
    
@app.route('/get_records')
def get_profiles():
    
    result = get_profiles_controller()
    return result

@app.route('/edit_profile/<id>', methods=['PUT'])
def edit_profile(id):
    
    result = edit_profile_controller(id)
    return result
    
@app.route('/delete_all_records')
def delete_all_profiles():
    
    result = delete_all_profiles_controller()
    return result

@app.route('/delete_one_record')
def delete_one_profile():
    
    # AT THE END OF THE ROUTE THE ID MUST BE ADDED AS FOLLOWS: http://127.0.0.1:5000/delete_one_record?id=1

    result = delete_one_profile_controller()
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
    