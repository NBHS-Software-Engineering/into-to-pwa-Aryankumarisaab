CREATE TABLE extension(extID INTEGER NOT NULL PRIMARY KEY,name TEXT NOT NULL, hyperlink TEXT NOT NULL,about TEXT NOT NULL,image TEXT NOT NULL,language TEXT NOT NULL);

INSERT INTO extension(extID,name,hyperlink,about,image,language) VALUES (1,'Live Server','https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer','Launch a development local Server with live reload feature for static & dynamic pages','https://ritwickdey.gallerycdn.vsassets.io/extensions/ritwickdey/liveserver/5.7.9/1736542717282/Microsoft.VisualStudio.Services.Icons.Default','HTML CSS JS');
INSERT INTO extension(extID,name,hyperlink,about,image,language) VALUES (2,"Render CR LF","https://marketplace.visualstudio.com/items?itemName=medo64.render-crlf","Displays the line ending symbol and optionally extra whitespace when 'Render whitespace' is turned on.","https://medo64.gallerycdn.vsassets.io/extensions/medo64/render-crlf/1.7.1/1689315206970/Microsoft.VisualStudio.Services.Icons.Default","#BASH");
INSERT INTO extension(extID,name,hyperlink,about,image,language) VALUES (3,"Start GIT BASH","https://marketplace.visualstudio.com/items?itemName=McCarter.start-git-bash","Adds a bash command to VSCode that allows you to start git-bash in the current workspace's root folder.","https://mccarter.gallerycdn.vsassets.io/extensions/mccarter/start-git-bash/1.2.1/1499505567572/Microsoft.VisualStudio.Services.Icons.Default","#BASH");
INSERT INTO extension(extID,name,hyperlink,about,image,language) VALUES (4,"SQLite3 Editor","https://marketplace.visualstudio.com/items?itemName=yy0931.vscode-sqlite3-editor","Edit SQLite3 files like you would in spreadsheet applications.","https://yy0931.gallerycdn.vsassets.io/extensions/yy0931/vscode-sqlite3-editor/1.0.85/1690893830873/Microsoft.VisualStudio.Services.Icons.Default","SQL");

SELECT * FROM extension;
SELECT * FROM extension WHERE language LIKE '#BASH';

CREATE TABLE IF NOT EXISTS users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Movies table
CREATE TABLE IF NOT EXISTS movies (
    movieID INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    genre TEXT,
    release_year INTEGER,
    rating REAL,
    image_url TEXT,
    duration TEXT,
    is_free BOOLEAN DEFAULT 0,
    is_hot BOOLEAN DEFAULT 0
);

-- TV Shows table
CREATE TABLE IF NOT EXISTS shows (
    showID INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    genre TEXT,
    release_year INTEGER,
    rating REAL,
    image_url TEXT,
    seasons INTEGER,
    is_free BOOLEAN DEFAULT 0,
    is_hot BOOLEAN DEFAULT 0
);

-- Streaming platforms
CREATE TABLE IF NOT EXISTS platforms (
    platformID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    logo_url TEXT,
    base_url TEXT,
    is_free BOOLEAN DEFAULT 0
);

-- Movie-platform relationships
CREATE TABLE IF NOT EXISTS movie_platforms (
    movieID INTEGER,
    platformID INTEGER,
    direct_url TEXT,
    PRIMARY KEY (movieID, platformID),
    FOREIGN KEY (movieID) REFERENCES movies(movieID),
    FOREIGN KEY (platformID) REFERENCES platforms(platformID)
);

-- Show-platform relationships
CREATE TABLE IF NOT EXISTS show_platforms (
    showID INTEGER,
    platformID INTEGER,
    direct_url TEXT,
    PRIMARY KEY (showID, platformID),
    FOREIGN KEY (showID) REFERENCES shows(showID),
    FOREIGN KEY (platformID) REFERENCES platforms(platformID)
);

-- User watchlist
CREATE TABLE IF NOT EXISTS watchlist (
    userID INTEGER,
    itemID INTEGER,
    item_type TEXT, -- 'movie' or 'show'
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (userID, itemID, item_type),
    FOREIGN KEY (userID) REFERENCES users(userID)
);

-- Insert platforms
INSERT INTO platforms (name, logo_url, base_url, is_free) VALUES 
('Netflix', '/static/images/netflix.png', 'https://netflix.com', 0),
('Disney+', '/static/images/disney.png', 'https://disneyplus.com', 0),
('Amazon Prime', '/static/images/prime.png', 'https://primevideo.com', 0),
('Hulu', '/static/images/hulu.png', 'https://hulu.com', 0),
('Max', '/static/images/max.png', 'https://max.com', 0),
('Tubi', '/static/images/tubi.png', 'https://tubitv.com', 1),
('YouTube Free', '/static/images/youtube.png', 'https://youtube.com', 1),
('Peacock', '/static/images/peacock.png', 'https://peacocktv.com', 0);

-- Insert 17 movies
INSERT INTO movies (title, description, genre, release_year, rating, image_url, duration, is_free, is_hot) VALUES 
('Inception', 'A thief who steals corporate secrets through dream-sharing technology.', 'Sci-Fi', 2010, 8.8, '/static/images/inception.jpg', '2h 28m', 0, 1),
('The Dark Knight', 'Batman faces the Joker, a criminal mastermind seeking to create chaos.', 'Action', 2008, 9.0, '/static/images/dark_knight.jpg', '2h 32m', 0, 1),
('Parasite', 'Greed and class discrimination threaten the newly formed symbiotic relationship.', 'Thriller', 2019, 8.6, '/static/images/parasite.jpg', '2h 12m', 1, 1),
('Avatar', 'A paraplegic Marine dispatched to the moon Pandora on a unique mission.', 'Sci-Fi', 2009, 7.8, '/static/images/avatar.jpg', '2h 42m', 0, 0),
('The Shawshank Redemption', 'Two imprisoned men bond over a number of years, finding solace.', 'Drama', 1994, 9.3, '/static/images/shawshank.jpg', '2h 22m', 1, 1),
('Pulp Fiction', 'The lives of two mob hitmen, a boxer, and a pair of diner bandits intertwine.', 'Crime', 1994, 8.9, '/static/images/pulp_fiction.jpg', '2h 34m', 0, 0),
('Forrest Gump', 'The presidencies of Kennedy and Johnson through the eyes of an Alabama man.', 'Drama', 1994, 8.8, '/static/images/forrest_gump.jpg', '2h 22m', 1, 0),
('The Matrix', 'A computer hacker learns about the true nature of his reality.', 'Sci-Fi', 1999, 8.7, '/static/images/matrix.jpg', '2h 16m', 0, 1),
('Goodfellas', 'The story of Henry Hill and his life in the mob.', 'Crime', 1990, 8.7, '/static/images/goodfellas.jpg', '2h 26m', 0, 0),
('The Godfather', 'The aging patriarch of an organized crime dynasty transfers control to his son.', 'Crime', 1972, 9.2, '/static/images/godfather.jpg', '2h 55m', 1, 1),
('Fight Club', 'An insomniac office worker forms an underground fight club.', 'Drama', 1999, 8.8, '/static/images/fight_club.jpg', '2h 19m', 0, 0),
('Interstellar', 'A team of explorers travel through a wormhole in space.', 'Sci-Fi', 2014, 8.6, '/static/images/interstellar.jpg', '2h 49m', 0, 1),
('The Silence of the Lambs', 'A young F.B.I. cadet must receive the help of an incarcerated cannibal.', 'Thriller', 1991, 8.6, '/static/images/silence_lambs.jpg', '1h 58m', 1, 0),
('Gladiator', 'A former Roman General sets out to exact vengeance against the corrupt emperor.', 'Action', 2000, 8.5, '/static/images/gladiator.jpg', '2h 35m', 0, 0),
('Back to the Future', 'A teenager is accidentally sent 30 years into the past in a time-traveling car.', 'Adventure', 1985, 8.5, '/static/images/back_future.jpg', '1h 56m', 1, 1),
('The Lion King', 'Lion prince Simba flees his kingdom only to learn the true meaning of responsibility.', 'Animation', 1994, 8.5, '/static/images/lion_king.jpg', '1h 28m', 0, 0),
('Avengers: Endgame', 'The Avengers take one final stand against Thanos.', 'Action', 2019, 8.4, '/static/images/endgame.jpg', '3h 1m', 0, 1);

-- Insert 17 TV shows
INSERT INTO shows (title, description, genre, release_year, rating, image_url, seasons, is_free, is_hot) VALUES 
('Stranger Things', 'When a young boy vanishes, a small town uncovers a mystery involving secret experiments.', 'Sci-Fi', 2016, 8.7, '/static/images/stranger_things.jpg', 4, 0, 1),
('Breaking Bad', 'A high school chemistry teacher diagnosed with cancer turns to a life of crime.', 'Drama', 2008, 9.5, '/static/images/breaking_bad.jpg', 5, 1, 1),
('The Mandalorian', 'The travels of a lone bounty hunter in the outer reaches of the galaxy.', 'Sci-Fi', 2019, 8.8, '/static/images/mandalorian.jpg', 3, 0, 1),
('Game of Thrones', 'Nine noble families fight for control over the lands of Westeros.', 'Fantasy', 2011, 9.3, '/static/images/got.jpg', 8, 0, 1),
('The Office', 'A mockumentary on a group of typical office workers.', 'Comedy', 2005, 8.9, '/static/images/office.jpg', 9, 0, 0),
('Friends', 'Follows the personal and professional lives of six twenty-something-year-old friends.', 'Comedy', 1994, 8.9, '/static/images/friends.jpg', 10, 1, 1),
('The Crown', 'Follows the political rivalries and romance of Queen Elizabeth II''s reign.', 'Drama', 2016, 8.7, '/static/images/crown.jpg', 6, 0, 0),
('The Witcher', 'Geralt of Rivia, a mutated monster-hunter for hire, journeys toward his destiny.', 'Fantasy', 2019, 8.2, '/static/images/witcher.jpg', 3, 0, 1),
('Black Mirror', 'An anthology series exploring a twisted, high-tech multiverse.', 'Sci-Fi', 2011, 8.8, '/static/images/black_mirror.jpg', 6, 0, 0),
('The Boys', 'A group of vigilantes set out to take down corrupt superheroes.', 'Action', 2019, 8.7, '/static/images/boys.jpg', 4, 0, 1),
('Money Heist', 'Eight thieves take hostages and lock themselves in the Royal Mint of Spain.', 'Crime', 2017, 8.2, '/static/images/money_heist.jpg', 5, 1, 1),
('The Queen''s Gambit', 'Orphaned chess prodigy struggles with addiction while mastering the game of chess.', 'Drama', 2020, 8.6, '/static/images/queens_gambit.jpg', 1, 0, 1),
('Wednesday', 'Follows Wednesday Addams'' years as a student, mastering her psychic ability.', 'Comedy', 2022, 8.2, '/static/images/wednesday.jpg', 1, 0, 1),
('The Bear', 'A young chef from the fine dining world returns to Chicago to run his family''s sandwich shop.', 'Drama', 2022, 8.6, '/static/images/bear.jpg', 2, 1, 1),
('Squid Game', 'Hundreds of cash-strapped players accept a strange invitation to compete in children''s games.', 'Thriller', 2021, 8.0, '/static/images/squid_game.jpg', 1, 0, 1),
('House of the Dragon', 'The story of House Targaryen set 200 years before the events of Game of Thrones.', 'Fantasy', 2022, 8.5, '/static/images/hotd.jpg', 1, 0, 1),
('The Last of Us', 'After a global pandemic destroys civilization, a hardened survivor takes charge of a 14-year-old girl.', 'Drama', 2023, 8.8, '/static/images/last_of_us.jpg', 1, 0, 1);

-- Insert movie-platform relationships
INSERT INTO movie_platforms (movieID, platformID, direct_url) VALUES 
(1, 1, 'https://netflix.com/title/70131314'),
(1, 3, 'https://primevideo.com/dp/B003W0C020'),
(2, 1, 'https://netflix.com/title/70079583'),
(3, 6, 'https://tubitv.com/movies/12345'),
(4, 2, 'https://disneyplus.com/movies/avatar'),
(5, 6, 'https://tubitv.com/movies/12346'),
(6, 3, 'https://primevideo.com/dp/B000U7NB2U'),
(7, 6, 'https://tubitv.com/movies/12347'),
(8, 1, 'https://netflix.com/title/20557938'),
(9, 5, 'https://max.com/movies/goodfellas'),
(10, 6, 'https://tubitv.com/movies/12348'),
(11, 3, 'https://primevideo.com/dp/B000U7NB2U'),
(12, 1, 'https://netflix.com/title/70305903'),
(13, 6, 'https://tubitv.com/movies/12349'),
(14, 5, 'https://max.com/movies/gladiator'),
(15, 6, 'https://tubitv.com/movies/12350'),
(16, 2, 'https://disneyplus.com/movies/lion-king'),
(17, 2, 'https://disneyplus.com/movies/avengers-endgame');

-- Insert show-platform relationships
INSERT INTO show_platforms (showID, platformID, direct_url) VALUES 
(1, 1, 'https://netflix.com/title/80057281'),
(2, 6, 'https://tubitv.com/series/12345'),
(3, 2, 'https://disneyplus.com/series/the-mandalorian'),
(4, 5, 'https://max.com/series/game-of-thrones'),
(5, 3, 'https://primevideo.com/dp/B000U7NB2U'),
(6, 6, 'https://tubitv.com/series/12346'),
(7, 1, 'https://netflix.com/title/80025678'),
(8, 1, 'https://netflix.com/title/80189685'),
(9, 1, 'https://netflix.com/title/70264888'),
(10, 3, 'https://primevideo.com/dp/B07QX2SVLC'),
(11, 1, 'https://netflix.com/title/80192098'),
(12, 1, 'https://netflix.com/title/80234304'),
(13, 1, 'https://netflix.com/title/81231974'),
(14, 5, 'https://max.com/series/the-bear'),
(15, 1, 'https://netflix.com/title/81040344'),
(16, 5, 'https://max.com/series/house-of-the-dragon'),
(17, 5, 'https://max.com/series/the-last-of-us');