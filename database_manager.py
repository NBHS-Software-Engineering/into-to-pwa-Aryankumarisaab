import sqlite3 as sql
import hashlib

def get_db_connection():
    return sql.connect("database/data_source.db")

def init_tables():
    """Initialize database tables if they don't exist"""
    conn = get_db_connection()
    
    tables = [
        # Users table for authentication
        """CREATE TABLE IF NOT EXISTS users (
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        
        # Movies table
        """CREATE TABLE IF NOT EXISTS movies (
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
        )""",
        
        # TV Shows table
        """CREATE TABLE IF NOT EXISTS shows (
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
        )""",
        
        # Streaming platforms
        """CREATE TABLE IF NOT EXISTS platforms (
            platformID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            logo_url TEXT,
            base_url TEXT,
            is_free BOOLEAN DEFAULT 0
        )""",
        
        # Movie-platform relationships
        """CREATE TABLE IF NOT EXISTS movie_platforms (
            movieID INTEGER,
            platformID INTEGER,
            direct_url TEXT,
            PRIMARY KEY (movieID, platformID),
            FOREIGN KEY (movieID) REFERENCES movies(movieID),
            FOREIGN KEY (platformID) REFERENCES platforms(platformID)
        )""",
        
        # Show-platform relationships
        """CREATE TABLE IF NOT EXISTS show_platforms (
            showID INTEGER,
            platformID INTEGER,
            direct_url TEXT,
            PRIMARY KEY (showID, platformID),
            FOREIGN KEY (showID) REFERENCES shows(showID),
            FOREIGN KEY (platformID) REFERENCES platforms(platformID)
        )""",
        
        # User watchlist
        """CREATE TABLE IF NOT EXISTS watchlist (
            userID INTEGER,
            itemID INTEGER,
            item_type TEXT,
            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (userID, itemID, item_type),
            FOREIGN KEY (userID) REFERENCES users(userID)
        )"""
    ]
    
    for table_sql in tables:
        try:
            conn.execute(table_sql)
        except sql.Error as e:
            print(f"Error creating table: {e}")
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User authentication functions
def create_user(username, email, password):
    conn = get_db_connection()
    try:
        password_hash = hash_password(password)
        conn.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", 
                    (username, email, password_hash))
        conn.commit()
        return True
    except sql.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = get_db_connection()
    password_hash = hash_password(password)
    user = conn.execute("SELECT userID, username FROM users WHERE username = ? AND password_hash = ?", 
                       (username, password_hash)).fetchone()
    conn.close()
    return user

# Movie functions
def get_all_movies():
    conn = get_db_connection()
    movies = conn.execute("SELECT * FROM movies").fetchall()
    conn.close()
    return movies

def get_hot_movies():
    conn = get_db_connection()
    movies = conn.execute("SELECT * FROM movies WHERE is_hot = 1").fetchall()
    conn.close()
    return movies

def get_free_movies():
    conn = get_db_connection()
    movies = conn.execute("SELECT * FROM movies WHERE is_free = 1").fetchall()
    conn.close()
    return movies

def search_movies(query):
    conn = get_db_connection()
    movies = conn.execute("SELECT * FROM movies WHERE title LIKE ? OR genre LIKE ?", 
                         (f'%{query}%', f'%{query}%')).fetchall()
    conn.close()
    return movies

def get_movie_platforms(movie_id):
    conn = get_db_connection()
    platforms = conn.execute('''
        SELECT p.name, p.logo_url, mp.direct_url, p.is_free 
        FROM movie_platforms mp 
        JOIN platforms p ON mp.platformID = p.platformID 
        WHERE mp.movieID = ?
    ''', (movie_id,)).fetchall()
    conn.close()
    return platforms

# Show functions
def get_all_shows():
    conn = get_db_connection()
    shows = conn.execute("SELECT * FROM shows").fetchall()
    conn.close()
    return shows

def get_hot_shows():
    conn = get_db_connection()
    shows = conn.execute("SELECT * FROM shows WHERE is_hot = 1").fetchall()
    conn.close()
    return shows

def get_free_shows():
    conn = get_db_connection()
    shows = conn.execute("SELECT * FROM shows WHERE is_free = 1").fetchall()
    conn.close()
    return shows

def search_shows(query):
    conn = get_db_connection()
    shows = conn.execute("SELECT * FROM shows WHERE title LIKE ? OR genre LIKE ?", 
                        (f'%{query}%', f'%{query}%')).fetchall()
    conn.close()
    return shows

def get_show_platforms(show_id):
    conn = get_db_connection()
    platforms = conn.execute('''
        SELECT p.name, p.logo_url, sp.direct_url, p.is_free 
        FROM show_platforms sp 
        JOIN platforms p ON sp.platformID = p.platformID 
        WHERE sp.showID = ?
    ''', (show_id,)).fetchall()
    conn.close()
    return platforms

# Watchlist functions
def add_to_watchlist(user_id, item_id, item_type):
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO watchlist (userID, itemID, item_type) VALUES (?, ?, ?)", 
                    (user_id, item_id, item_type))
        conn.commit()
        return True
    except sql.IntegrityError:
        return False
    finally:
        conn.close()

def get_watchlist(user_id):
    conn = get_db_connection()
    watchlist = conn.execute('''
        SELECT w.itemID, w.item_type, 
               CASE WHEN w.item_type = 'movie' THEN m.title ELSE s.title END as title,
               CASE WHEN w.item_type = 'movie' THEN m.image_url ELSE s.image_url END as image_url,
               CASE WHEN w.item_type = 'movie' THEN m.rating ELSE s.rating END as rating
        FROM watchlist w
        LEFT JOIN movies m ON w.itemID = m.movieID AND w.item_type = 'movie'
        LEFT JOIN shows s ON w.itemID = s.showID AND w.item_type = 'show'
        WHERE w.userID = ?
    ''', (user_id,)).fetchall()
    conn.close()
    return watchlist

# Extension functions (keeping your original functionality)
def listExtension():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM extension').fetchall()
    conn.close()
    return data

# Initialize tables when this module is imported
init_tables()
# Add this function to your database_manager.py to check what's in the database

def debug_database():
    """Debug function to check database contents"""
    conn = get_db_connection()
    
    print("=== DATABASE DEBUG INFO ===")
    
    # Check tables
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print("Tables:", [table[0] for table in tables])
    
    # Check movie count
    movie_count = conn.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
    print(f"Movies in database: {movie_count}")
    
    # Check show count
    show_count = conn.execute("SELECT COUNT(*) FROM shows").fetchall()[0][0]
    print(f"Shows in database: {show_count}")
    
    # Check platform count
    platform_count = conn.execute("SELECT COUNT(*) FROM platforms").fetchone()[0]
    print(f"Platforms in database: {platform_count}")
    
    # Sample some movies
    sample_movies = conn.execute("SELECT movieID, title FROM movies LIMIT 3").fetchall()
    print("Sample movies:", sample_movies)
    
    # Sample some shows
    sample_shows = conn.execute("SELECT showID, title FROM shows LIMIT 3").fetchall()
    print("Sample shows:", sample_shows)
    
    conn.close()
    print("=== END DEBUG INFO ===")

# Call this at the end of the file to see debug info when the module loads
if __name__ == '__main__':
    debug_database()