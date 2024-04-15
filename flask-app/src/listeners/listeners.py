from flask import Blueprint, request, jsonify, make_response
from src import db
from datetime import datetime

listeners = Blueprint('listeners', __name__)

# Get all listeners information
@listeners.route('/listeners', methods=['GET'])
def get_listeners():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT * FROM Listeners')
        row_headers = [x[0] for x in cursor.description]  # this will extract row headers
        results = cursor.fetchall()
        json_data = [dict(zip(row_headers, result)) for result in results]

        return make_response(jsonify(json_data), 200)
    except Exception as e:
        print(f"An error occurred: {e}")
        return make_response(jsonify({'error': 'Internal server error'}), 500)

# Get all followed artists info for a listener
@listeners.route('/listeners/<int:user_id>/followed_artists', methods=['GET'])
def get_followed_artists(user_id):
    try:
        with db.get_db().cursor() as cursor:
            query = """
                SELECT *
                FROM Artists a
                JOIN is_follows f ON a.artist_id = f.artist_id
                WHERE f.user_id = %s
            """
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()
            if results:
                json_data = [dict(zip([col[0] for col in cursor.description], row)) for row in results]
                return jsonify(json_data), 200
            else:
                return jsonify({'message': 'No followed artists found'}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500


# recommend 10 songs to the listener based on their favorite artists
@listeners.route('/listeners/<int:user_id>/20_recommended_songs', methods=['GET'])
def get_random_songs(user_id):
    try:
        with db.get_db().cursor() as cursor:
            # Adjusted SQL query to join Songs to Albums to Artists
            query = """
            SELECT DISTINCT s.song_id, s.name, a.artist_id
            FROM Songs s
            JOIN Albums al ON s.album_id = al.album_id 
            JOIN Artists a ON al.artist_id = a.artist_id  
            JOIN is_follows ifo ON a.artist_id = ifo.artist_id  
            WHERE ifo.user_id = %s
            ORDER BY RAND()  # Randomize the selection
            LIMIT 20  
            """
            cursor.execute(query, (user_id,))
            row_headers = [x[0] for x in cursor.description]  # Extract column headers
            results = cursor.fetchall()

            if results:
                json_data = [dict(zip(row_headers, row)) for row in results]
                response = make_response(jsonify(json_data), 200)
            else:
                # If no songs are found, return a message indicating so
                response = make_response(jsonify({'message': 'No random songs found for this listener from followed artists'}), 404)

            response.mimetype = 'application/json'
            return response
    except Exception as e:
        # Log and return an error message if something goes wrong
        print(f"An error occurred: {e}")
        return make_response(jsonify({'error': 'Internal server error'}), 500)

    
# Unfollow a artist from a listener
@listeners.route('/listeners/<int:user_id>/<int:artist_id>', methods=['DELETE'])
def remove_artist_from_follows(user_id, artist_id):
    try:
        with db.get_db().cursor() as cursor:
            # First, check if the following relationship exists
            cursor.execute("SELECT * FROM is_follows WHERE User_ID = %s AND Artist_ID = %s", (user_id, artist_id))
            if cursor.fetchone() is None:
                return make_response(jsonify({'message': 'No following relationship exists'}), 404)

            # If the relationship exists, proceed to delete
            cursor.execute("DELETE FROM is_follows WHERE User_ID = %s AND Artist_ID = %s", (user_id, artist_id))
            db.get_db().commit()  # Commit to save changes

            return make_response(jsonify({'message': 'Artist unfollowed successfully'}), 200)

    except Exception as e:
        # Log and return an error message if something goes wrong
        print(f"An error occurred: {e}")
        db.get_db().rollback()  # Rollback in case of error
        return make_response(jsonify({'error': 'Internal server error'}), 500)
    


# Get donation information history for a user
@listeners.route('/listeners/<int:user_id>/donations', methods=['GET'])
def get_user_donations(user_id):
    
        with db.get_db().cursor() as cursor:
            # SQL query to fetch all donations made by a specific user from is_supports
            query = """
            SELECT ls.user_id, ls.artist_id, a.name as artist_name, ls.Donation_amount, ls.date
            FROM is_supports ls
            JOIN Artists a ON ls.artist_id = a.artist_id
            WHERE ls.user_id = %s
            ORDER BY ls.date DESC
            """
            cursor.execute(query, (user_id,))
            row_headers = [x[0] for x in cursor.description]  # Extract column headers
            results = cursor.fetchall()

            if results:
                json_data = [dict(zip(row_headers, row)) for row in results]
                response = make_response(jsonify(json_data), 200)
            else:
                # If no donations are found, return a message indicating so
                response = make_response(jsonify({'message': 'No donations found for this user'}), 404)

            response.mimetype = 'application/json'
            return response

    
# Get all playlists from a user
@listeners.route('/listeners/<int:user_id>/playlists', methods=['GET'])
def get_playlists(user_id):
    try:
        with db.get_db().cursor() as cursor:
            # SQL query to fetch all playlists associated with the user_id
            query = """
            SELECT Playlist_ID, Title, Description, Status
            FROM Playlists
            WHERE User_ID = %s
            ORDER BY Playlist_ID
            """
            cursor.execute(query, (user_id,))
            row_headers = [x[0] for x in cursor.description]  # Extract column headers
            results = cursor.fetchall()

            if results:
                json_data = [dict(zip(row_headers, row)) for row in results]
                response = make_response(jsonify(json_data), 200)
            else:
                # If no playlists are found, return a message indicating so
                response = make_response(jsonify({'message': 'No playlists found for this user'}), 404)

            response.mimetype = 'application/json'
            return response

    except Exception as e:
        # Log and return an error message if something goes wrong
        print(f"An error occurred: {e}")
        return make_response(jsonify({'error': 'Internal server error'}), 500)

# Retrieve all songs from a selected playlist
@listeners.route('/listeners/<int:user_id>/playlists/<int:playlist_id>/songs', methods=['GET'])
def get_songs_in_playlist(user_id, playlist_id):
    try:
        with db.get_db().cursor() as cursor:
            query = """
            SELECT s.Song_ID, s.Name, s.Audio_File, s.Release_date, a.Album_ID
            FROM Songs s
            JOIN pl_songs ps ON s.Song_ID = ps.Song_ID
            JOIN Playlists p ON ps.Playlist_ID = p.Playlist_ID
            JOIN Albums a ON s.Album_ID = a.Album_ID
            WHERE p.Playlist_ID = %s AND p.User_ID = %s
            ORDER BY s.Name
            """
            cursor.execute(query, (playlist_id, user_id))
            results = cursor.fetchall()

            if not results:
                return make_response(jsonify({'message': 'No songs found in this playlist'}), 404)

            json_data = [
                {
                    'Song_ID': row[0],
                    'Name': row[1],
                    'Audio_File': row[2],
                    'Release_date': row[3].strftime('%Y-%m-%d'),
                    'Album_ID': row[4]
                } for row in results
            ]
            return make_response(jsonify(json_data), 200)

    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


# Create a new playlist for a user
@listeners.route('/listeners/<int:user_id>/playlists', methods=['POST'])
def create_playlist(user_id):
    # Retrieve data from the request
    data = request.get_json()
    title = data.get('Title')
    description = data.get('Description')
    status = data.get('Status', 'Public')  # Default status to 'Public' if not provided

    # Validate the necessary information
    if not title:
        return make_response(jsonify({'error': 'Title is required'}), 400)

    try:
        with db.get_db().cursor() as cursor:
            # SQL to insert the new playlist into the database
            query = """
            INSERT INTO Playlists (Title, Description, Status, User_ID)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (title, description, status, user_id))
            db.get_db().commit()  # Commit to save changes

            # Fetch the last inserted id if you want to return it
            playlist_id = cursor.lastrowid

            return make_response(jsonify({'message': 'Playlist created successfully', 'Playlist_ID': playlist_id}), 201)
    
    except Exception as e:
        # Rollback in case of an error
        db.get_db().rollback()
        return make_response(jsonify({'error': 'Failed to create playlist', 'message': str(e)}), 500)
        
# Delete a playlist for a user
@listeners.route('/listeners/playlists/<int:playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    try:
        with db.get_db().cursor() as cursor:
            # First, check if the playlist exists and belongs to the user
            cursor.execute("SELECT User_ID FROM Playlists WHERE Playlist_ID = %s", (playlist_id,))
            result = cursor.fetchone()
            if not result:
                return make_response(jsonify({'error': 'Playlist not found'}), 404)
            

            # Perform the deletion
            cursor.execute("DELETE FROM Playlists WHERE Playlist_ID = %s", (playlist_id,))
            db.get_db().commit()

            # Check if the delete was successful
            if cursor.rowcount == 0:
                return make_response(jsonify({'error': 'No playlist was deleted'}), 404)
            
            return make_response(jsonify({'message': 'Playlist deleted successfully'}), 200)

    except Exception as e:
        db.get_db().rollback()
        return make_response(jsonify({'error': 'Internal server error', 'message': str(e)}), 500)
    

# User retrieve all comments that he/she made
@listeners.route('/listeners/<int:user_id>/comments', methods=['GET'])
def get_user_comments(user_id):
    try:
        with db.get_db().cursor() as cursor:
            query = """
            SELECT comment_id, content, date, song_id, user_id
            FROM Comments
            WHERE user_id = %s
            ORDER BY date DESC
            """
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()

            if results:
                row_headers = [x[0] for x in cursor.description]  # Extract column headers
                json_data = [dict(zip(row_headers, result)) for result in results]
                return make_response(jsonify(json_data), 200)
            else:
                return make_response(jsonify({'message': 'No comments found'}), 404)

    except Exception as e:
        print(f"An error occurred: {e}")
        return make_response(jsonify({'error': 'Internal server error'}), 500)


# User update a existing comment
@listeners.route('/listeners/<int:comment_id>/comments', methods=['PUT'])
def update_comment(comment_id):
    # The comment_id is extracted from the URL.
    
    # Extract the updated comment data from the request body
    data = request.get_json()
    new_content = data.get('content')  # This is the new content of the comment
    
    # Perform input validation
    if not new_content:
        return make_response(jsonify({'error': 'Content is required'}), 400)
    
    try:
        # Assume a database connection function get_db() and a cursor method to execute queries
        with db.get_db().cursor() as cursor:
            # Update the comment in the database using the comment_id
            update_query = """
            UPDATE Comments
            SET content = %s
            WHERE comment_id = %s
            """
            cursor.execute(update_query, (new_content, comment_id))
            
            # Check if the comment exists and has been updated
            if cursor.rowcount == 0:
                return make_response(jsonify({'error': 'No comment found with the provided id'}), 404)
            
            db.get_db().commit()
            return make_response(jsonify({'message': 'Comment updated successfully'}), 200)

    except Exception as e:
        # Rollback in case of error
        db.get_db().rollback()
        return make_response(jsonify({'error': str(e)}), 500)
    
    
# User delete a existing comment
@listeners.route('/listeners/<int:user_id>/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(user_id, comment_id):
    try:
        with db.get_db().cursor() as cursor:
            # First, verify that the comment exists and belongs to the user
            cursor.execute("SELECT * FROM Comments WHERE user_id = %s AND comment_id = %s", (user_id, comment_id))
            comment = cursor.fetchone()
            if comment is None:
                return make_response(jsonify({'error': 'Comment not found or does not belong to user'}), 404)

            # Proceed to delete the comment
            cursor.execute("DELETE FROM Comments WHERE user_id = %s AND comment_id = %s", (user_id, comment_id))
            db.get_db().commit()  # Commit to save the changes

            return make_response(jsonify({'message': 'Comment deleted successfully'}), 200)

    except Exception as e:
        # Log and return an error message if something goes wrong
        print(f"An error occurred: {e}")
        db.get_db().rollback()  # Rollback in case of an error
        return make_response(jsonify({'error': 'Internal server error'}), 500)
    
    
