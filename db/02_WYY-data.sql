SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;

USE WYY;

-- INSERT SAMPLE DATA

-- Inserting into Listeners
INSERT INTO Listeners (Name, Birthday, Gender, Email) VALUES
('John Doe', '1990-05-15', 'Male', 'john.doe@example.com'),
('Jane Smith', '1985-07-20', 'Female', 'jane.smith@example.com'),
('Alex Johnson', '1992-09-10', 'Non-binary', 'alex.johnson@example.com');

-- Inserting into Artists
INSERT INTO Artists (Name, Bio, Num_Followers, Gender, Birthday) VALUES
('The Beatless', 'A popular band from Liverpool.', 1000000, 'Other', '1960-01-01'),
('Rolling Pebbles', 'Rock band known for their blues influences.', 500000, 'Other', '1962-05-02'),
('Elvis Parsley', 'Solo artist with a flair for dramatics.', 200000, 'Male', '1935-01-08');

-- Inserting into Albums
INSERT INTO Albums (Title, Artist_ID, Release_date) VALUES
('Abbey Load', 1, '2020-01-01'),
('Sticky Fingers', 2, '2020-02-01'),
('The Wonder of You', 3, '2020-03-01');

-- Inserting into Songs
INSERT INTO Songs (Name, Release_date, Album_ID, Audio_File) VALUES
('Let It Be', '1970-03-06',1,'lala.mp3'),
('Paint It Black', '1966-05-07',2,'papa.mp3'),
('Suspicious Minds', '1969-08-26', 3,'kaka.mp3');

-- Inserting into Genres
INSERT INTO Genres (Genre_name) VALUES
('Rock'),
('Pop'),
('Blues');

-- Linking Songs to Genres
INSERT INTO sg_genre (Song_ID, Genre_ID) VALUES
(1, 1),
(2, 3),
(3, 2);

-- Inserting into Playlists
INSERT INTO Playlists (Title, Description, Status, User_ID) VALUES
('Workout Hits', 'Upbeat music for working out.', 'Active', 1),
('Chill Vibes', 'Relaxing tunes for a lazy day.', 'Active', 2);

-- Linking Songs to Playlists
INSERT INTO pl_songs (Playlist_ID, Song_ID) VALUES
(1, 1),
(1, 2),
(2, 3);

-- Inserting into Comments
INSERT INTO Comments (Content, Date, User_ID, Song_ID) VALUES
('Love this song!', '2024-03-31', 1, 1),
('Classic hit!', '2024-03-31', 2, 2),
('Great for relaxation.', '2024-03-31', 3, 3);

-- Establishing Follow relationships
INSERT INTO is_follows (User_ID, Artist_ID) VALUES
(1, 1),
(2, 2),
(3, 3);

-- Adding Support transactions
INSERT INTO is_supports (User_ID, Artist_ID, Donation_amount, Date) VALUES
(1, 1, 50.00, '2024-03-31'),
(2, 2, 75.00, '2024-03-31'),
(3, 3, 100.00, '2024-03-31');

-- Linking Artists to Songs (assuming at_songs is Artists to Songs relationship)
INSERT INTO at_songs (Artist_ID, Song_ID) VALUES
(1, 1),
(2, 1),
(3, 3);

-- Inserting into Music Critics
INSERT INTO Music_Critics (Name, Email) VALUES
('Cristiano Junior',  'CR.Jr@example.com'),
('Messi Santos', 'Mes.San@example.com'),
('Neymar Ronaldo', 'Ney.Ron@example.com');

-- Inserting into Podcasters
INSERT INTO Podcasters (location, birthday, name, gender, bio, age) VALUES
('Boston', '1888-03-03', 'Old George', 'Male', 'PHd in NU', 136),
('NewYork', '1988-03-03', 'Kelly', 'Female', 'PHd in NYU', 36),
('Tokyo', '1998-03-03', 'Kaze', 'Male', 'Musician', 26);

-- Inserting into Podcasts
INSERT INTO Podcasts (release_date, description, title) VALUES
('2023-03-03','Back to the past, retro musics!', 'RETRO'),
('2024-03-03','HBD and what a song!', 'BIRTHDAY SPECIAL EDITION'),
('2022-05-02','Sad song analytics', 'SAD!');

-- Inserting into Analytics
INSERT INTO Analytics (Age_Groups, Gender, Audience_demo, Listens, Downloads) VALUES
('50-70', 'Male', 'RETRO.mp3', 10000000, 30),
('20-70', 'Female', 'Happy.mp3', 100000, 3000),
('20-40', 'Male', 'sad.mp3', 1000, 300);

-- Inserting into Epidsodes
INSERT INTO Episodes (Audio_file, Release_date, Title, Description, Duration_min, Analytics_id, Podcast_id) VALUES
('RETRO.mp3', '2023-10-25', 'RETRO', 'ABOUT OLD MUSICS', 90, 1, 1),
('HAPPY.mp3', '2023-9-25', 'YEAH', 'ABOUT HAPPY MUSICS', 60, 2, 2),
('sad.mp3', '2024-3-25', 'SAD', 'ABOUT SAD MUSICS', 90, 3, 3);

-- Inserting into Ratings
INSERT INTO Ratings (Comment, Rate, Date, Album_id, Commentator_id) VALUES
('bad af!', 1, '2024-03-31', 1, 1),
('good af!', 5, '2024-03-31', 2, 2),
('GOOOOOOOD!', 5, '2024-03-31', 3, 3);

-- Inserting into Reviews
INSERT INTO Reviews (Content, Date, Title, Podcaster_id) VALUES
('No way, this episode is insane', '2024-03-31', 'OMG', 1),
('No way, this episode is too bad', '2024-03-31', 'UMM', 2),
('Listen to this is just wasting my time', '2024-03-31', 'TRASH', 3);

-- Inserting into rev_crtics
INSERT INTO rev_critics (Review_id, Commentator_id) VALUES
(1, 1),
(2, 2),
(3, 3);


-- Inserting into pod_hosted
INSERT INTO pod_hosted (podcast_id, podcaster_id) VALUES
(1, 1),
(2, 2),
(3, 3);


-- Insert into Episodes
INSERT INTO Episodes (Title, Description, Release_date, Duration_min, Audio_file) VALUES
('PawsLife', 'A day in Paws Life', '2024-04-02', 30, 'audio_file.mp3'),
('Adventures in the Wild', 'Exploring the wilderness', '2024-03-28', 45, 'wild_adventures.mp3'),
('TechTalk', 'Latest in technology news', '2024-03-30', 50, 'techtalk_audio.mp3');


-- Insert a collaboration episode 
INSERT INTO Episodes (Title, Description, Release_date, Duration_min, Audio_file) VALUES
('Collaboration with BU', 'Made a new friend at BU', '2024-04-05', 60, 'collaboration_audio.mp3'),
('Cross-Campus Project', 'Collaborative project between universities', '2024-04-07', 55, 'cross_campus_project.mp3'),
('Joint Research Initiative', 'Exploring joint research opportunities', '2024-04-10', 40, 'research_initiative_audio.mp3');


-- Insert into Comments
INSERT INTO Comments (Content, Date, User_ID, Episode_ID) VALUES
('Great episode!', '2024-04-02', 1, 4),
('Really enjoyed this one!', '2024-04-05', 2, 2),
('Interesting discussion!', '2024-04-02', 3, 3);



SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
