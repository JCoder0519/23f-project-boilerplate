from flask import Blueprint, request, jsonify, make_response, current_app
import json
import urllib.parse
from src import db
from datetime import datetime



comments = Blueprint('comments', __name__)

#Get Comments of an episode by a specific Episode
@comments.route('/comments/<episode_id>', methods=['GET'])
def get_comments_by_episode(episode_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Comments WHERE Episode_ID = %s', (episode_id,))
    row_headers = [x[0] for x in cursor.description]
    json_data = [dict(zip(row_headers, row)) for row in cursor.fetchall()]
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Insert a comment under a specific Episode
@comments.route('/comments/<episode_id>', methods=['POST'])
def insert_comment(episode_id):
    data = request.get_json()
    current_app.logger.info(data)
    
    content = data['Content']
    date_str = data['Date']
    date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string
    user_id = data['User_ID']
    
    query = 'INSERT INTO Comments (Content, Date, User_ID, Episode_ID) VALUES (%s, %s, %s, %s)'
    data = (content, date_obj, user_id, episode_id)
    
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit() 

    return jsonify({"message": "Comment added successfully"}), 201

# Update a comment by Episode ID
@comments.route('/comments/<episode_id>', methods=['PUT'])
def update_comment(episode_id):
    data = request.json
    current_app.logger.info(data)
    
    content = data['Content']
    date_str = data['Date']
    date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d %H:%M:%S') 
    user_id = data['User_ID']

    query = 'UPDATE Comments SET Content = %s, Date = %s, User_ID = %s WHERE Episode_ID = %s'
    data = (content, date_obj, user_id, episode_id)
    
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    
    return jsonify({"message": "Comment updated successfully"}), 200


#Delete a comment by Episode ID
@comments.route('/comments/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    try:
        with db.get_db().cursor() as cursor:
            cursor.execute("SELECT * FROM Comments WHERE Comment_ID = %s",(comment_id))
            comment = cursor.fetchone()
            if comment is None:
                return make_response(jsonify({'error': 'Comment not found or does not belong to user'}), 404)

            cursor.execute("DELETE FROM Comments WHERE Comment_ID = %s ", (comment_id))
            db.get_db().commit()  

            return make_response(jsonify({'message': 'Comment deleted successfully'}), 200)

    except Exception as e:
        print(f"An error occurred: {e}")
        db.get_db().rollback() 
        return make_response(jsonify({'error': 'Internal server error'}), 500)
    