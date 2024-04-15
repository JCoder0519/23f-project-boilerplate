from flask import Blueprint, request, jsonify, make_response
import json
from src import db

artists = Blueprint('artists', __name__)

@artists.route('/artists/<Artist_ID>', methods=['GET'])
def get_artists(Artist_ID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Songs s JOIN at_songs ass ON s.Song_id = ass.Song_id JOIN Artists a ON ass.Artist_id = a.Artist_id WHERE a.Artist_id = {0}'.format(Artist_ID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@artists.route('/artist_songs/<artistID>', methods=['GET'])
def get_songs(artistID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT s.Song_ID, s.Name, s.Release_date, s.Audio_file, s.Album_ID FROM Songs s \
                   JOIN at_songs ass ON s.Song_ID = ass.Song_ID JOIN Artists a ON ass.Artist_ID = a. Artist_ID WHERE a.Artist_ID = {0}'.format(artistID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

        
        
@artists.route('/artist/<int:artist_id>', methods=['GET'])
def get_artist_songs(artist_id):
    try:
        with db.get_db().cursor() as cursor:
            # SQL query to fetch all songs by a specific artist
            query = """
            SELECT * FROM Songs s JOIN at_songs ass ON s.Song_id = ass.Song_id
            JOIN Artists a ON ass.Artist_id = a.Artist_id WHERE a.Artist_id = %s
            """
            cursor.execute(query, (artist_id,))
            row_headers = [x[0] for x in cursor.description]  # Extract column headers
            results = cursor.fetchall()

            if results:
                json_data = [dict(zip(row_headers, row)) for row in results]
                return jsonify(json_data), 200
            else:
                return jsonify({'message': 'No info found for this artist'}), 404

    except Exception as e:
        # It's good practice to log the exception here
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Internal server error'}), 500
