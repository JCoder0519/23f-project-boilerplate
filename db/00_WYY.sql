SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE DATABASE IF NOT EXISTS WYY;
USE WYY;

-- Listeners
CREATE TABLE IF NOT EXISTS Listeners (
    User_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Birthday DATE,
    Gender VARCHAR(45),
    Email VARCHAR(255) NOT NULL
);

-- Artists
CREATE TABLE IF NOT EXISTS Artists (
    Artist_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Bio TEXT,
    Num_Followers INT,
    Gender VARCHAR(45),
    Birthday DATE
);

-- Albums
CREATE TABLE IF NOT EXISTS Albums (
    Album_ID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Artist_ID INT,
    Release_date DATE,
    FOREIGN KEY (Artist_ID) REFERENCES Artists(Artist_ID) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Songs
CREATE TABLE IF NOT EXISTS Songs (
    Song_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Release_date DATE,
    Audio_File VARCHAR(255),
    Album_ID INT,
    FOREIGN KEY (Album_ID) REFERENCES Albums(Album_ID) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Genres
CREATE TABLE IF NOT EXISTS Genres (
    Genre_ID INT AUTO_INCREMENT PRIMARY KEY,
    Genre_name VARCHAR(255) NOT NULL
);

-- sg_genre (junction table between Songs and Genres)
CREATE TABLE IF NOT EXISTS sg_genre (
    Song_ID INT,
    Genre_ID INT,
    PRIMARY KEY (Song_ID, Genre_ID),
    FOREIGN KEY (Song_ID) REFERENCES Songs(Song_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Genre_ID) REFERENCES Genres(Genre_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Playlists
CREATE TABLE IF NOT EXISTS Playlists (
    Playlist_ID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Description TEXT,
    Status VARCHAR(45),
    User_ID INT,
    FOREIGN KEY (User_ID) REFERENCES Listeners(User_ID) ON DELETE SET NULL ON UPDATE CASCADE
);

-- pl_songs (junction table between Playlists and Songs)
CREATE TABLE IF NOT EXISTS pl_songs (
    Playlist_ID INT,
    Song_ID INT,
    PRIMARY KEY (Playlist_ID, Song_ID),
    FOREIGN KEY (Playlist_ID) REFERENCES Playlists(Playlist_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Song_ID) REFERENCES Songs(Song_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Analytics
CREATE TABLE IF NOT EXISTS Analytics(
    Analytics_id  INT AUTO_INCREMENT,
    Age_Groups    VARCHAR(50),
    Gender        VARCHAR(45),
    Audience_demo VARCHAR(250),
    Listens       INT,
    Downloads     INT,
    PRIMARY KEY (Analytics_id)
);

-- Podcasters
CREATE TABLE IF NOT EXISTS Podcasters (
    Podcaster_id INT AUTO_INCREMENT,
    Location VARCHAR(250),
    Birthday DATE,
    Name VARCHAR(50),
    Gender VARCHAR(45),
    Bio VARCHAR(250),
    Age INT,
    PRIMARY KEY (Podcaster_id)
);

-- Podcasts
CREATE TABLE IF NOT EXISTS Podcasts(
    Podcast_id   INT AUTO_INCREMENT,
    Release_date DATE,
    Description  VARCHAR(2500),
    Title        VARCHAR(250),
    PRIMARY KEY (Podcast_id)
);

-- Episodes
CREATE TABLE IF NOT EXISTS Episodes(
    Episode_id  INT AUTO_INCREMENT,
    Audio_file   VARCHAR(250),
    Release_date DATE,
    Title        VARCHAR(250),
    Description  VARCHAR(2500),
    Duration_min     INT,
    Analytics_id INT,
    Podcast_id   INT,
    PRIMARY KEY (Episode_id),
    FOREIGN KEY (Analytics_id) REFERENCES Analytics (Analytics_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Podcast_id) REFERENCES Podcasts (Podcast_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Comments
CREATE TABLE IF NOT EXISTS Comments (
    Comment_ID INT AUTO_INCREMENT PRIMARY KEY,
    Content TEXT NOT NULL,
    Date DATE,
    User_ID INT,
    Song_ID INT,
    Episode_ID INT,
    Playlist_ID INT,
    FOREIGN KEY (User_ID) REFERENCES Listeners(User_ID) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (Song_ID) REFERENCES Songs(Song_ID) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (Episode_ID) REFERENCES Episodes(Episode_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (Playlist_ID) REFERENCES Playlists(Playlist_ID) ON DELETE SET NULL ON UPDATE CASCADE
);

-- pod_follows (junction table between Podcasters and Listeners)
CREATE TABLE IF NOT EXISTS pod_follows (
    Podcaster_ID INT,
    User_ID INT,
    PRIMARY KEY (Podcaster_ID, User_ID),
    FOREIGN KEY (Podcaster_ID) REFERENCES Podcasters(Podcaster_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (User_ID) REFERENCES Listeners(User_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- is_follows (junction table between Listeners and Artists)
CREATE TABLE IF NOT EXISTS is_follows (
    User_ID INT,
    Artist_ID INT,
    PRIMARY KEY (User_ID, Artist_ID),
    FOREIGN KEY (User_ID) REFERENCES Listeners(User_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Artist_ID) REFERENCES Artists(Artist_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- is_supports (junction table between Listeners and Artists for donations)
CREATE TABLE IF NOT EXISTS is_supports (
    User_ID INT,
    Artist_ID INT,
    Donation_amount DECIMAL(10, 2),
    Date DATE,
    PRIMARY KEY (User_ID, Artist_ID),
    FOREIGN KEY (User_ID) REFERENCES Listeners(User_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Artist_ID) REFERENCES Artists(Artist_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- at_songs (junction table between Artists and Songs)
CREATE TABLE IF NOT EXISTS at_songs (
    Artist_ID INT,
    Song_ID INT,
    PRIMARY KEY (Artist_ID, Song_ID),
    FOREIGN KEY (Artist_ID) REFERENCES Artists(Artist_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Song_ID) REFERENCES Songs(Song_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- pod_hosted
CREATE TABLE IF NOT EXISTS pod_hosted(
    Podcast_id INT,
    Podcaster_id INT,
    PRIMARY KEY (Podcast_id, Podcaster_id),
    FOREIGN KEY (Podcast_id) REFERENCES Podcasts(Podcast_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Podcaster_id) REFERENCES Podcasters(Podcaster_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Music_Critics
CREATE TABLE IF NOT EXISTS Music_Critics(
    Commentator_id INT AUTO_INCREMENT,
    Name VARCHAR(50),
    Email VARCHAR(250),
    PRIMARY KEY (Commentator_id)
);

-- Reviews
CREATE TABLE IF NOT EXISTS Reviews(
    Review_id INT AUTO_INCREMENT,
    Content VARCHAR(5000),
    Date DATE,
    Title VARCHAR(250),
    Podcaster_id INT,
    Artist_id INT,
    PRIMARY KEY (Review_id),
    FOREIGN KEY (Artist_id) REFERENCES Artists(Artist_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Podcaster_id) REFERENCES Podcasters(Podcaster_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- rev_critics
CREATE TABLE IF NOT EXISTS rev_critics(
    Review_id INT,
    Commentator_id INT,
    PRIMARY KEY (Review_id, Commentator_id),
    FOREIGN KEY (Review_id) REFERENCES Reviews(Review_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Commentator_id) REFERENCES Music_Critics(Commentator_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Ratings
CREATE TABLE IF NOT EXISTS Ratings(
    Rating_id INT AUTO_INCREMENT,
    Comment VARCHAR(2500),
    Rate INT,
    Date DATE,
    Podcast_id INT,
    Commentator_id INT,
    Album_id INT,
    PRIMARY KEY (Rating_id),
    FOREIGN KEY (Podcast_id) REFERENCES Podcasts(Podcast_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Commentator_id) REFERENCES Music_Critics(Commentator_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Album_id) REFERENCES Albums(Album_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
