from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db
import urllib.parse
artists = Blueprint('artists', __name__)

@artists.route('/artists', methods=['GET'])
def get_all_artists():
    cursor = db.get_db().cursor()
    cursor.execute('select Name, Artist_ID from Artists')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@artists.route('/artist_albums', methods=['GET'])
def get_all_albums():
    cursor = db.get_db().cursor()
    cursor.execute('select Album_ID, Artist_ID, Release_date, Title, Name from Albums natural join Artists')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


@artists.route('/artists/<artist_id>', methods=['GET'])
def get_artist(artist_id):
    
        with db.get_db().cursor() as cursor:
            query = """
            SELECT * FROM Songs s JOIN at_songs ass ON s.Song_id = ass.Song_id JOIN \
                    Artists a ON ass.Artist_id = a.Artist_id WHERE a.Artist_id = %s
            """
            cursor.execute(query, (artist_id,))
            row_headers = [x[0] for x in cursor.description]
            results = cursor.fetchall()
            if results:
                json_data = [dict(zip(row_headers, row)) for row in results]
                response = make_response(jsonify(json_data), 200)
            else:
                response = make_response(jsonify({'message': 'No info found for this artist'}), 404)
            response.mimetype = 'application/json'
            return response
        

        
@artists.route('/artist_songs/<artist_id>', methods=['GET'])
def get_songs(artist_id):
        with db.get_db().cursor() as cursor:
            query = """
            SELECT s.Song_ID, s.Name, s.Release_date, s.Audio_file, s.Album_ID FROM Songs s \
                    JOIN at_songs ass ON s.Song_ID = ass.Song_ID JOIN Artists a ON ass.Artist_ID = a. Artist_ID WHERE a.Artist_ID = %s
            """
            cursor.execute(query, (artist_id,))
            row_headers = [x[0] for x in cursor.description]
            results = cursor.fetchall()
            if results:
                json_data = [dict(zip(row_headers, row)) for row in results]
                response = make_response(jsonify(json_data), 200)
            else:
                response = make_response(jsonify({'message': 'No info found for this artist'}), 404)
            response.mimetype = 'application/json'
            return response

@artists.route('/artist_albums/<artist_id>', methods=['GET'])
def get_albums(artist_id):
        with db.get_db().cursor() as cursor:
            query = """
            SELECT Title, al.Artist_ID, Album_ID \
                FROM Albums al JOIN Artists a ON al.Artist_ID = a.Artist_ID WHERE a.Artist_ID = %s
            """
            cursor.execute(query, (artist_id,))
            row_headers = [x[0] for x in cursor.description]
            results = cursor.fetchall()
            if results:
                json_data = [dict(zip(row_headers, row)) for row in results]
                response = make_response(jsonify(json_data), 200)
            else:
                response = make_response(jsonify({'message': 'No info found for this artist'}), 404)
            response.mimetype = 'application/json'
            return response

#insert album
@artists.route('/add_album', methods=['POST'])
def add_new_album():
    the_data = request.json
    current_app.logger.info(the_data)

    title = the_data['Title']
    artist_ID = the_data['Artist_ID']


    query = 'INSERT INTO Albums (Title, Artist_ID, Release_date) VALUES ('
    query += f'"{title}", '
    query += f'{artist_ID}, '
    query += f'NOW())'

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'
#update album
@artists.route('/update_artist_album', methods=['PUT'])
def update_album():
    album_info = request.json
    title = album_info['Title']
    artist_ID = album_info['Artist_ID']
    album_id = album_info['Album_ID']
    
    query = 'UPDATE Albums SET Title = %s, Artist_ID = %s WHERE Album_ID = %s'
    data = (title, artist_ID, album_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'album updated'
#delete album
@artists.route('/delete_artist_album', methods=['DELETE'])
def delete_album():
    album_info = request.json
    album_ID = album_info['Album_ID']
    
    query = 'DELETE FROM Albums WHERE Album_ID = %s'
    data = (album_ID)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'album deleted'
#update song
@artists.route('/update_artist_song', methods=['PUT'])
def update_song():
    song_info = request.json
    album_ID = song_info['Album_ID']
    audio_File = song_info['Audio_file']
    name = song_info['Name']
    song_ID = song_info['Song_ID']
    
    query = 'UPDATE Songs SET Name = %s, Album_ID = %s, Audio_File = %s WHERE Song_id = %s'
    data = (name, album_ID, audio_File, song_ID)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'song updated'
#delete song
@artists.route('/delete_artist_song', methods=['DELETE'])
def delete_song():
    song_info = request.json
    song_ID = song_info['Song_ID']
    
    query = 'DELETE FROM Songs WHERE Song_ID = %s'
    data = (song_ID)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'song deleted'

@artists.route('/add_song', methods=['POST'])
def add_new_song():
    the_data = request.json
    current_app.logger.info(the_data)

    name = the_data['song_name']
    audio_File = the_data['Audio_File']
    album_id = the_data['Album_ID']

    query = 'INSERT INTO Songs (Name, Release_date, Audio_File, Album_ID) VALUES ('
    query += f'"{name}", '
    query += f'NOW(), '
    query += f'"{audio_File}", '
    query += f'{album_id})'
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    cursor.execute('SELECT LAST_INSERT_ID()')
    song_id = cursor.fetchone()[0]

    artist_id = the_data['Artist_ID']
    query = 'INSERT INTO at_songs (Artist_ID, Song_ID) VALUES ('
    query += f'{artist_id}, '
    query += f'{song_id})'

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    genre_id = the_data['Genre_ID']
    query = 'INSERT INTO sg_genre (Genre_ID, Song_ID) VALUES ('
    query += f'{genre_id}, '
    query += f'{song_id})'

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    
    return 'Success!'



@artists.route('/artist_bridge_songs', methods=['GET'])
def get_all_bridge():
    cursor = db.get_db().cursor()
    query = """
            SELECT g.Genre_ID, s.Song_ID, s.Name as song_name, s.Release_date, s.Audio_File, s.Album_ID, g.Genre_name, a.Artist_ID, a.Name as artist_name\
                FROM Songs s\
                    JOIN sg_genre sg ON s.Song_ID = sg.Song_ID\
                        JOIN Genres g ON sg.Genre_ID = g.Genre_ID\
                            JOIN at_songs ats ON s.Song_ID = ats.Song_ID\
                                JOIN Artists a ON ats.Artist_ID = a.Artist_ID;
            """
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@artists.route('/genres', methods=['GET'])
def get_all_genres():
    cursor = db.get_db().cursor()
    cursor.execute('select * from Genres')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response



# 3.1 rating ------------------------------------------------------------------------

@artists.route('/artist_album_rate', methods=['GET'])
def get_com_albums():
    cursor = db.get_db().cursor()
    cursor.execute('select Title, Album_ID, Commentator_id,Comment, Rate, Date from Albums natural join Ratings')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@artists.route('/rate/album', methods=['POST'])
def add_rate_album():
    the_data = request.json
    current_app.logger.info(the_data)

    comment = the_data['Comment']
    rate = the_data['Rate']
    album_id = the_data['Album_ID']
    commentator_id = the_data['Commentator_id']

    # Build the SQL query
    query = 'INSERT INTO Ratings (Comment, Rate, Date, Album_id, Commentator_id) VALUES (%s, %s, NOW(), %s, %s)'
    values = (comment, rate, album_id, commentator_id)

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({"message": "Rating added successfully"}), 201


@artists.route('/podcast_rate', methods=['GET'])
def get_all_pod():
    cursor = db.get_db().cursor()
    cursor.execute('select Title, Podcast_ID, Commentator_id, Comment, Rate, Date from Podcasts natural join Ratings')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@artists.route('/rate/pod', methods=['POST'])
def add_rate_pod():
    the_data = request.json
    current_app.logger.info(the_data)

    comment = the_data['Comment']
    rate = the_data['Rate']
    podcast_id = the_data['Podcast_ID']
    commentator_id = the_data['Commentator_id']

    # Build the SQL query
    query = 'INSERT INTO Ratings (Comment, Rate, Date, Podcast_id, Commentator_id) VALUES (%s, %s, NOW(), %s, %s)'
    values = (comment, rate, podcast_id, commentator_id)

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    db.get_db().commit()

    return jsonify({"message": "Rating added successfully"}), 201

# 3.2 reviews ------------------------------------------------------------------------


@artists.route('/search/<int:id>', methods=['GET'])
def search_rev(id):
    with db.get_db().cursor() as cursor:
        # SQL query to fetch all artists with a number of followers less than or equal to num
        query = """
        SELECT * FROM Reviews WHERE Review_id = %s
        """
        cursor.execute(query, (id,))
        row_headers = [x[0] for x in cursor.description]  # Extract column headers
        results = cursor.fetchall()

        if results:
            json_data = [dict(zip(row_headers, row)) for row in results]
            response = make_response(jsonify(json_data), 200)
        else:
            # If no artists are found, return a message indicating so
            response = make_response(jsonify({'message': 'Review cant be found'}), 404)

        response.mimetype = 'application/json'
        return response

# 3.4 background ------------------------------------------------------------------------

@artists.route('/get_artist_fol/<int:num>', methods=['GET'])
def get_artist_fol(num):
    with db.get_db().cursor() as cursor:
        # SQL query to fetch all artists with a number of followers less than or equal to num
        query = """
        SELECT * FROM Artists WHERE Num_Followers <= %s
        """
        cursor.execute(query, (num,))
        row_headers = [x[0] for x in cursor.description]  # Extract column headers
        results = cursor.fetchall()

        if results:
            json_data = [dict(zip(row_headers, row)) for row in results]
            response = make_response(jsonify(json_data), 200)
        else:
            # If no artists are found, return a message indicating so
            response = make_response(jsonify({'message': 'No artists found with fewer followers'}), 404)

        response.mimetype = 'application/json'
        return response