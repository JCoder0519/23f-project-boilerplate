from faker import Faker
import pymysql
import random



fake = Faker()

connection = pymysql.connect(host='localhost', user='root', password='321123', db='WYY', port=3200)


cursor = connection.cursor()


# Assuming Artist, Listener, and other IDs are consecutive starting from 1 after initial inserts.
def generate_listeners():
    for _ in range(50):
        name = fake.name()
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=70).isoformat()
        gender = fake.random_element(elements=('Male', 'Female', 'Non-binary'))
        email = fake.email()
        cursor.execute('INSERT INTO Listeners (Name, Birthday, Gender, Email) VALUES (%s, %s, %s, %s);',
                       (name, birthday, gender, email))

def generate_artists():
    for _ in range(50):
        name = fake.name()
        bio = fake.text(max_nb_chars=500)
        num_followers = fake.random_int(min=0, max=1000000)
        gender = fake.random_element(elements=('Male', 'Female', 'Non-binary'))
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=70).isoformat()
        cursor.execute('INSERT INTO Artists (Name, Bio, Num_Followers, Gender, Birthday) VALUES (%s, %s, %s, %s, %s);',
                       (name, bio, num_followers, gender, birthday))

def generate_albums():
    for _ in range(50):
        title = fake.sentence(nb_words=5)
        artist_id = fake.random_int(min=1, max=50)
        release_date = fake.date_between(start_date='-10y', end_date='today').isoformat()
        cursor.execute('INSERT INTO Albums (Title, Artist_ID, Release_date) VALUES (%s, %s, %s);',
                       (title, artist_id, release_date))

def generate_songs():
    for _ in range(50):
        name = fake.sentence(nb_words=3)
        release_date = fake.date_between(start_date='-10y', end_date='today').isoformat()
        audio_file = str(name) + "mp3"
        album_id = fake.random_int(min=1, max=50)
        cursor.execute('INSERT INTO Songs (Name, Release_date, audio_File, Album_ID) VALUES (%s, %s, %s, %s);',
                       (name, release_date, audio_file, album_id))

def generate_genres_and_sg_genre():
    
    
    genres = ['Pop', 'Rock', 'Jazz', 'Hip Hop', 'Classical', 'Metal', 'Country', 'Blues', 'Electronic', 'Folk']
    for genre in genres:
        cursor.execute('INSERT INTO Genres (Genre_name) VALUES (%s);', (genre,))
    connection.commit()  # Commit to ensure genres are available for foreign key relations

    
    # Fetch genre IDs from the database
    cursor.execute('SELECT Genre_ID FROM Genres')
    genre_ids = [row[0] for row in cursor.fetchall()]

    # Fetch song IDs from the database
    cursor.execute('SELECT Song_ID FROM Songs')
    song_ids = [row[0] for row in cursor.fetchall()]

    song_genre_pairs = set()
    for _ in range(200):
        song_id = random.choice(song_ids)
        genre_id = random.choice(genre_ids)
        pair = (song_id, genre_id)
        
        if pair not in song_genre_pairs:
            song_genre_pairs.add(pair)
            cursor.execute('INSERT INTO sg_genre (Song_ID, Genre_ID) VALUES (%s, %s);', (song_id, genre_id))

def generate_playlists_and_pl_songs():
    for _ in range(50):
        title = fake.sentence(nb_words=5)
        description = fake.text(max_nb_chars=200)
        status = fake.random_element(elements=('Public', 'Private'))
        user_id = fake.random_int(min=1, max=50)
        cursor.execute('INSERT INTO Playlists (Title, Description, Status, User_ID) VALUES (%s, %s, %s, %s);',
                       (title, description, status, user_id))
    connection.commit()  # Commit to ensure playlists are available for foreign key relations

# Fetch actual playlist and song IDs
    cursor.execute('SELECT Playlist_ID FROM Playlists')
    playlist_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute('SELECT Song_ID FROM Songs')
    song_ids = [row[0] for row in cursor.fetchall()]

    # Manage playlist-song relationships
    playlist_song_pairs = set()
    for _ in range(200):
        playlist_id = random.choice(playlist_ids)
        song_id = random.choice(song_ids)
        if (playlist_id, song_id) not in playlist_song_pairs:
            playlist_song_pairs.add((playlist_id, song_id))
            cursor.execute('INSERT INTO pl_songs (Playlist_ID, Song_ID) VALUES (%s, %s);', (playlist_id, song_id))
    connection.commit()


def generate_podcasters_and_podcasts():
    # Set to track (Podcast_id, Podcaster_id) pairs
    podcaster_podcast_pairs = set()

    # Insert podcasters
    for _ in range(50):
        name = fake.name()
        location = fake.city()
        birthday = fake.date_of_birth(minimum_age=20, maximum_age=60).isoformat()
        gender = fake.random_element(elements=('Male', 'Female', 'Non-binary'))
        bio = fake.text(max_nb_chars=50)
        age = fake.random_int(min=20, max=60)
        cursor.execute('INSERT INTO Podcasters (Location, Birthday, Name, Gender, Bio, Age) VALUES (%s, %s, %s, %s, %s, %s);',
                       (location, birthday, name, gender, bio, age))
    connection.commit()  # Commit after inserting podcasters

    # Retrieve podcaster IDs
    cursor.execute('SELECT Podcaster_id FROM Podcasters')
    podcaster_ids = [row[0] for row in cursor.fetchall()]

    # Insert podcasts
    for _ in range(50):
        title = fake.sentence(nb_words=6)
        release_date = fake.date_between(start_date='-5y', end_date='today').isoformat()
        description = fake.text(max_nb_chars=1000)
        cursor.execute('INSERT INTO Podcasts (Title, Release_date, Description) VALUES (%s, %s, %s);',
                       (title, release_date, description))
    connection.commit()  # Commit after inserting podcasts

    # Retrieve podcast IDs
    cursor.execute('SELECT Podcast_id FROM Podcasts')
    podcast_ids = [row[0] for row in cursor.fetchall()]

    # Insert pod_hosted entries ensuring unique pairs
    for _ in range(200):
        podcaster_id = random.choice(podcaster_ids)
        podcast_id = random.choice(podcast_ids)

        pair = (podcast_id, podcaster_id)
        if pair not in podcaster_podcast_pairs:
            podcaster_podcast_pairs.add(pair)
            cursor.execute('INSERT INTO pod_hosted (Podcast_id, Podcaster_id) VALUES (%s, %s);',
                           (podcast_id, podcaster_id))
            
            
def generate_episodes_and_analytics():
    podcast_ids = list(range(1, 51))
    
    used_combinations = set() 
    for _ in range(200):
        title = fake.sentence(nb_words=5)
        description = fake.text(max_nb_chars=1000)
        duration_min = fake.random_int(min=1, max=240)
        release_date = fake.date_between(start_date='-5y', end_date='today').isoformat()
        audio_file = str(title) + "mp3"
        analytics_id = fake.random_int(min=1, max=200)  # Assuming you will generate 200 analytics rows separately
        podcast_id = random.choice(podcast_ids)
        
        combination = (analytics_id, podcast_id)
        if combination not in used_combinations:
                used_combinations.add(combination)
                cursor.execute('INSERT INTO Episodes (Audio_file, Title, Description, Duration_min, Release_date, Analytics_id, Podcast_id) VALUES (%s, %s, %s, %s, %s, %s, %s);',
                               (audio_file, title, description, duration_min, release_date, analytics_id, podcast_id))
       

def generate_comments():
    try:
        # Fetch existing IDs to ensure data integrity
        cursor.execute('SELECT User_ID FROM Listeners')
        user_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute('SELECT Song_ID FROM Songs')
        song_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute('SELECT Episode_ID FROM Episodes')
        episode_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute('SELECT Playlist_ID FROM Playlists')
        playlist_ids = [row[0] for row in cursor.fetchall()]

        for _ in range(300):
            content = fake.text(max_nb_chars=200)
            date = fake.date_between(start_date='-2y', end_date='today').isoformat()
            user_id = random.choice(user_ids)
            song_id = random.choice(song_ids)
            episode_id = random.choice(episode_ids)
            playlist_id = random.choice(playlist_ids)
            
            cursor.execute('INSERT INTO Comments (Content, Date, User_ID, Song_ID, Episode_ID, Playlist_ID) VALUES (%s, %s, %s, %s, %s, %s);',
                           (content, date, user_id, song_id, episode_id, playlist_id))
        
        connection.commit()
    except pymysql.Error as e:
        print(f"An error occurred: {e}")
        connection.rollback()
        
        
def generate_relationships_and_supports():
    user_ids = list(range(1, 51))  # Assuming 50 users
    artist_ids = list(range(1, 51))  # Assuming 50 artists

    user_artist_pairs = set()
    for _ in range(200):
        chosen_user_id = random.choice(user_ids)
        chosen_artist_id = random.choice(artist_ids)
        if (chosen_user_id, chosen_artist_id) not in user_artist_pairs:
            user_artist_pairs.add((chosen_user_id, chosen_artist_id))
            cursor.execute('INSERT INTO is_follows (User_ID, Artist_ID) VALUES (%s, %s);', (chosen_user_id, chosen_artist_id))
            donation_amount = random.uniform(10.0, 1000.0)
            date = fake.date_between(start_date='-2y', end_date='today').isoformat()
            cursor.execute('INSERT INTO is_supports (User_ID, Artist_ID, Donation_amount, Date) VALUES (%s, %s, %s, %s);',
                           (chosen_user_id, chosen_artist_id, donation_amount, date))
    
    artist_song_pairs = set()
    song_ids = list(range(1, 51))  # Assuming 50 songs
    for _ in range(200):
        artist_id = random.choice(artist_ids)
        song_id = random.choice(song_ids)
        
        pair = (artist_id, song_id)
        if pair not in artist_song_pairs:
            artist_song_pairs.add(pair)
            cursor.execute('INSERT INTO at_songs (Artist_ID, Song_ID) VALUES (%s, %s);', (artist_id, song_id))

                





def generate_analytics():
    for _ in range(200):
        age_groups = fake.random_element(elements=('18-24', '25-34', '35-44', '45-54', '55+'))
        gender = fake.random_element(elements=('Male', 'Female', 'Non-binary'))
        audience_demo = fake.sentence(nb_words=5)
        listens = fake.random_int(min=100, max=10000)
        downloads = fake.random_int(min=100, max=5000)
        cursor.execute('INSERT INTO Analytics (Age_Groups, Gender, Audience_demo, Listens, Downloads) VALUES (%s, %s, %s, %s, %s);',
                       (age_groups, gender, audience_demo, listens, downloads))

def generate_reviews_critics_and_ratings():
    # Generate music critics
    for _ in range(50):
        name = fake.name()
        email = fake.email()
        cursor.execute('INSERT INTO Music_Critics (Name, Email) VALUES (%s, %s);', (name, email))
    connection.commit()  # Ensure critics are available for foreign key relations

    # Fetch actual IDs for artists and podcasters
    cursor.execute('SELECT Artist_ID FROM Artists')
    artist_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT Podcaster_id FROM Podcasters')
    podcaster_ids = [row[0] for row in cursor.fetchall()]

    # Generate reviews
    for _ in range(50):
        content = fake.text(max_nb_chars=500)
        date = fake.date_between(start_date='-1y', end_date='today').isoformat()
        title = fake.sentence(nb_words=4)
        podcaster_id = random.choice(podcaster_ids)
        artist_id = random.choice(artist_ids)
        cursor.execute('INSERT INTO Reviews (Content, Date, Title, Podcaster_id, Artist_id) VALUES (%s, %s, %s, %s, %s);',
                       (content, date, title, podcaster_id, artist_id))
    
    # Fetch actual IDs for reviews and commentators
    cursor.execute('SELECT Review_id FROM Reviews')
    review_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT Commentator_id FROM Music_Critics')
    commentator_ids = [row[0] for row in cursor.fetchall()]

    # Ensure unique pairing for review critics
    review_commentator_pairs = set()
    for _ in range(200):
        review_id = random.choice(review_ids)
        commentator_id = random.choice(commentator_ids)
        pair = (review_id, commentator_id)

        if pair not in review_commentator_pairs:
            review_commentator_pairs.add(pair)
            cursor.execute('INSERT INTO rev_critics (Review_id, Commentator_id) VALUES (%s, %s);', 
                           (review_id, commentator_id))

    # Generate ratings
    cursor.execute('SELECT Album_id FROM Albums')
    album_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(50):
        comment = fake.text(max_nb_chars=300)
        rate = fake.random_int(min=1, max=5)
        date = fake.date_between(start_date='-1y', end_date='today').isoformat()
        podcast_id = random.choice(podcaster_ids)
        album_id = random.choice(album_ids)
        commentator_id = random.choice(commentator_ids)
        cursor.execute('INSERT INTO Ratings (Comment, Rate, Date, Podcast_id, Commentator_id, Album_id) VALUES (%s, %s, %s, %s, %s, %s);',
                       (comment, rate, date, podcast_id, commentator_id, album_id))
    
    connection.commit()

    # Handling errors and closing connections
    try:
        pass  # Place database operations here
    except pymysql.Error as e:
        print(f"An error occurred: {e}")
        connection.rollback()



def generate_pod_follows():
    try:
        # Fetch existing podcaster and user IDs to ensure data integrity
        cursor.execute('SELECT Podcaster_id FROM Podcasters')
        podcaster_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute('SELECT User_ID FROM Listeners')
        user_ids = [row[0] for row in cursor.fetchall()]

        # Set to track unique (Podcaster_ID, User_ID) pairs
        podcaster_user_pairs = set()

        # Aim to create a large number of follows but limit to the number of possible unique pairs
        for _ in range(min(200, len(podcaster_ids) * len(user_ids))):
            podcaster_id = random.choice(podcaster_ids)
            user_id = random.choice(user_ids)
            pair = (podcaster_id, user_id)

            if pair not in podcaster_user_pairs:
                podcaster_user_pairs.add(pair)
                cursor.execute('INSERT INTO pod_follows (Podcaster_ID, User_ID) VALUES (%s, %s);',
                               (podcaster_id, user_id))
        
        connection.commit()
    except pymysql.Error as e:
        print(f"An error occurred: {e}")
        connection.rollback()








# Run first then comment out
#generate_listeners()
#generate_artists()
#generate_albums()
#generate_songs()
#generate_analytics()



# bridge tables, Please Run one by one!!!
#If shows duplicate then run again

#generate_podcasters_and_podcasts() 
  
#generate_episodes_and_analytics()

#generate_relationships_and_supports()

#generate_reviews_critics_and_ratings()

#generate_genres_and_sg_genre()

#generate_playlists_and_pl_songs()

#generate_comments()

#generate_pod_follows()


connection.commit()

cursor.close()
connection.close()
