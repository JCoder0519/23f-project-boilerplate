from flask import Blueprint, request, jsonify, make_response, current_app
import json
import urllib.parse
from src import db
from datetime import datetime

analytics = Blueprint('analytics', __name__)

#Get Analytics by Analytics_id
@analytics.route('/analytics/<int:analytics_id>', methods=['GET'])
def get_analytics(analytics_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Analytics WHERE Analytics_id = %s', (analytics_id))
    row_headers = [x[0] for x in cursor.description]
    json_data = [dict(zip(row_headers, row)) for row in cursor.fetchall()]
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#Get All Analytics
@analytics.route('/analytics', methods=['GET'])
def get_all_analytics():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Analytics')
    row_headers = [x[0] for x in cursor.description]
    json_data = [dict(zip(row_headers, row)) for row in cursor.fetchall()]
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#Upload a new analytic into the database
@analytics.route('/analytics', methods=['POST'])
def upload_analytics():
    data = request.get_json()
    current_app.logger.info(data)
    
    age_groups = data['Age_Groups']
    gender = data['Gender']
    audience_demo = data['Audience_demo']
    listens = data['Listens']
    downloads = data['Downloads']
    
    query = 'INSERT INTO Analytics (Age_Groups, Gender, Audience_demo, Listens, Downloads) values ("'
    query += age_groups + '", "'
    query += gender + '", "'
    query += audience_demo + '", "'
    query += str(listens) + '", "'
    query += str(downloads) + '")'
    current_app.logger.info(query)
  
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit() 

    return 'Success!'

#Delete an analytic by Analytics ID
@analytics.route('/analytics/<analytics_id>', methods=['DELETE'])
def delete_comment(analytics_id):
    try:
        with db.get_db().cursor() as cursor:
            cursor.execute("SELECT * FROM Analytics WHERE Analytics_id = %s",(analytics_id))
            analytics = cursor.fetchone()
            if analytics is None:
                return make_response(jsonify({'error': 'Analytics not found or does not belong to user'}), 404)

            cursor.execute("DELETE FROM Analytics WHERE Analytics_id = %s ", (analytics_id))
            db.get_db().commit()  

            return make_response(jsonify({'message': 'Analytics deleted successfully'}), 200)

    except Exception as e:
        print(f"An error occurred: {e}")
        db.get_db().rollback() 
        return make_response(jsonify({'error': 'Internal server error'}), 500)
    
 #Update an analytic
@analytics.route('/analytics', methods=['PUT'])
def update_analytics():
    an_data = request.get_json()    
    age_groups = an_data['Age_Groups']
    gender = an_data['Gender']
    audience_demo = an_data['Audience_demo']
    listens = an_data['Listens']
    downloads = an_data['Downloads']
    analytics_id = an_data['Analytics_id']

    query = 'UPDATE Analytics SET Age_Groups = %s, Gender = %s, Audience_demo = %s, Listens = %s, Downloads = %s WHERE Analytics_id = %s'
    data = (age_groups, gender, audience_demo, listens, downloads, analytics_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Analytic updated'