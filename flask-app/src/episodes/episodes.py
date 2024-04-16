from flask import Blueprint, request, jsonify, make_response, current_app
import json
import urllib.parse
from src import db
from datetime import datetime


episodes = Blueprint('episodes', __name__)

#Get all episodes in the database
@episodes.route('/episodes', methods=['GET'])
def get_all_episodes():
 
        cursor = db.get_db().cursor()
        cursor.execute('SELECT * FROM Episodes')
        row_headers = [x[0] for x in cursor.description]
        json_data = [dict(zip(row_headers, row)) for row in cursor.fetchall()]
        the_response = make_response(jsonify(json_data))
        the_response.status_code = 200
        the_response.mimetype = 'application/json'
        return the_response

#Upload a new episode into the database
@episodes.route('/episodes', methods=['POST'])
def upload_episode():
    data = request.get_json()
    current_app.logger.info(data)
    
    title = data['Title']
    description = data['Description']
    release_date_str = data['Release_date']
    release_date_obj = datetime.strptime(release_date_str, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string
    duration_min = data['Duration_min']
    audio_file = data['Audio_file']
    
    query = 'INSERT INTO Episodes (Title, Description, Release_date, Duration_min, Audio_file) values ("'
    query += title + '", "'
    query += description + '", "'
    query += release_date_obj + '", "'
    query += str(duration_min) + '", "'
    query += audio_file + '")'
    current_app.logger.info(query)
  
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit() 

    return 'Success!'

#Get an episode by Episode ID
@episodes.route('/episodes/<episode_id>', methods=['GET'])
def get_artist(episode_id):
    
        with db.get_db().cursor() as cursor:
            query = """
            SELECT * FROM Episodes WHERE Episode_id = %s
            """
            cursor.execute(query, (episode_id,))
            row_headers = [x[0] for x in cursor.description]
            results = cursor.fetchall()
            if results:
                json_data = [dict(zip(row_headers, row)) for row in results]
                response = make_response(jsonify(json_data), 200)
            else:
                response = make_response(jsonify({'message': 'No info found for this artist'}), 404)
            response.mimetype = 'application/json'
            return response
        
#Update an episode
@episodes.route('/episodes', methods=['PUT'])
def update_episode():
    ep_info = request.json
    title = ep_info['Title']
    episode_id = ep_info['Episode_id']
    description = ep_info['Description']
    release_date_str = ep_info['Release_date']
    release_date_obj = datetime.strptime(release_date_str, '%a, %d %b %Y %H:%M:%S %Z')
    duration_min = ep_info['Duration_min']
    audio_file = ep_info['Audio_file']

    query = 'UPDATE Episodes SET title = %s, description = %s, release_date = %s, duration_min = %s, audio_file = %s WHERE episode_id = %s'
    data = (title, description, release_date_obj, duration_min, audio_file, episode_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'episodes updated'
    
#Delete an episode by Episode ID
@episodes.route('/episodes/<episode_id>', methods=['DELETE'])
def delete_comment(episode_id):
    try:
        with db.get_db().cursor() as cursor:
            cursor.execute("SELECT * FROM Episodes WHERE Episode_id = %s",(episode_id))
            episode = cursor.fetchone()
            if episode is None:
                return make_response(jsonify({'error': 'Episode not found or does not belong to user'}), 404)

            cursor.execute("DELETE FROM Episodes WHERE Episode_id = %s ", (episode_id))
            db.get_db().commit()  

            return make_response(jsonify({'message': 'Episode deleted successfully'}), 200)

    except Exception as e:
        print(f"An error occurred: {e}")
        db.get_db().rollback() 
        return make_response(jsonify({'error': 'Internal server error'}), 500)
