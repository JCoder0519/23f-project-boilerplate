from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db
from datetime import datetime

comments = Blueprint('comments', __name__)

# Get all comment for a song
@comments.route('/comments/<int:song_id>/comments', methods=['GET'])
def get_comments_for_song(song_id):
    try:
        with db.get_db().cursor() as cursor:
            query = """
            SELECT comment_id, content, date, user_id
            FROM Comments
            WHERE song_id = %s
            ORDER BY date DESC
            """
            cursor.execute(query, (song_id,))
            row_headers = [x[0] for x in cursor.description]  # Extract column headers
            results = cursor.fetchall()

            if results:
                # Create a list of dictionaries, each representing a comment
                json_data = [dict(zip(row_headers, row)) for row in results]
                return make_response(jsonify(json_data), 200)
            else:
                # If no comments are found, return a message indicating so
                return make_response(jsonify({'message': 'No comments found for this song'}), 404)

    except Exception as e:
        # Log the error and return an error message
        print(f"An error occurred: {e}")
        return make_response(jsonify({'error': 'Internal server error'}), 500)

# Create a new comment for A song
@comments.route('/comments/<int:song_id>/songs', methods=['POST'])
def add_comment_to_song(song_id):
    # Assuming `request.get_json()` will contain the necessary 'user_id' and 'content' keys
    data = request.get_json()
    current_app.logger.info(data)
    # Check for the presence of 'user_id' and 'content' in the request data
    user_id = data.get('user_id')
    content = data.get('content')
    
    if not user_id or not content:
        return make_response(jsonify({'error': 'Missing required user ID or content'}), 400)

    # For the purposes of this example, the date is automatically set to the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    try:
        # Prepare the parameterized SQL query
        query = """
        INSERT INTO Comments (content, user_id, song_id, date)
        VALUES (%s, %s, %s, %s)
        """
        # Execute the query with the parameters
        with db.get_db().cursor() as cursor:
            cursor.execute(query, (content, user_id, song_id, current_date))
            db.get_db().commit()
        # Insert the new comment into the database
        # Placeholder for actual database insert operation
        # Example: cursor.execute(query, (content, user_id, song_id, current_date))
        print(f"Inserting comment into database: {content}, User ID: {user_id}, Song ID: {song_id}, Date: {current_date}")

        # Assuming the insert operation is successful
        return make_response(jsonify({'message': 'Comment added successfully'}), 201)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return make_response(jsonify({'error': 'Internal server error'}), 500)
    
    
# User retrieves a specific comment
@comments.route('/comments/<int:user_id>/<int:comment_id>', methods=['GET'])
def get_user_comment(user_id, comment_id):
    try:
        with db.get_db().cursor() as cursor:
            query = """
            SELECT comment_id, content, date, song_id
            FROM Comments
            WHERE user_id = %s AND comment_id = %s
            """
            cursor.execute(query, (user_id, comment_id))
            result = cursor.fetchone()

            if result:
                row_headers = [x[0] for x in cursor.description]  # Extract column headers
                json_data = dict(zip(row_headers, result))
                return make_response(jsonify(json_data), 200)
            else:
                return make_response(jsonify({'message': 'Comment not found or access denied'}), 404)

    except Exception as e:
        print(f"An error occurred: {e}")
        return make_response(jsonify({'error': 'Internal server error'}), 500)
    
# User updates a specific comment
@comments.route('/comments/<int:user_id>/<int:comment_id>', methods=['PUT'])
def update_comment(user_id, comment_id):
    data = request.get_json()
    if 'content' not in data:
        return make_response(jsonify({'error': 'Missing required parameter: content'}), 400)

    try:
        with db.get_db().cursor() as cursor:
            # Check if the comment exists and belongs to the user
            check_query = """
            SELECT comment_id FROM Comments WHERE user_id = %s AND comment_id = %s
            """
            cursor.execute(check_query, (user_id, comment_id))
            comment = cursor.fetchone()

            if not comment:
                return make_response(jsonify({'message': 'No comment found or access denied'}), 404)

            # Update the comment
            update_query = """
            UPDATE Comments SET content = %s WHERE user_id = %s AND comment_id = %s
            """
            cursor.execute(update_query, (data['content'], user_id, comment_id))
            db.get_db().commit()

            return make_response(jsonify({'message': 'Comment updated successfully'}), 200)

    except Exception as e:
        print(f"An error occurred: {e}")
        return make_response(jsonify({'error': 'Internal server error'}), 500)

# User delete a specific comment
@comments.route('/comments/<int:user_id>/<int:comment_id>', methods=['DELETE'])
def delete_comment(user_id, comment_id):
    try:
        with db.get_db().cursor() as cursor:
            # First, check if the comment exists and belongs to the user
            check_query = """
            SELECT comment_id FROM Comments WHERE user_id = %s AND comment_id = %s
            """
            cursor.execute(check_query, (user_id, comment_id))
            comment = cursor.fetchone()

            if not comment:
                return make_response(jsonify({'message': 'Comment not found or access denied'}), 404)

            # Delete the comment
            delete_query = """
            DELETE FROM Comments WHERE user_id = %s AND comment_id = %s
            """
            cursor.execute(delete_query, (user_id, comment_id))
            db.get_db().commit()

            return make_response(jsonify({'message': 'Comment deleted successfully'}), 200)

    except Exception as e:
        print(f"An error occurred: {e}")
        return make_response(jsonify({'error': 'Internal server error'}), 500)
    
