from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import database_manager as dbHandler
import os

app = Flask(__name__)
app.secret_key = 'streamfinder_secret_key_2024'  # Change this in production!

@app.before_request
def before_request():
    # Ensure database tables exist before handling any request
    try:
        # This will initialize tables if they don't exist
        dbHandler.init_tables()
    except Exception as e:
        print(f"Database initialization error: {e}")

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = dbHandler.verify_user(username, password)
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Basic validation
        if not username or not email or not password:
            return render_template('signup.html', error='All fields are required')
        
        if dbHandler.create_user(username, email, password):
            return redirect(url_for('login'))
        else:
            return render_template('signup.html', error='Username or email already exists')
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        hot_movies = dbHandler.get_hot_movies()
        hot_shows = dbHandler.get_hot_shows()
        return render_template('index.html', 
                             hot_movies=hot_movies, 
                             hot_shows=hot_shows,
                             username=session['username'])
    except Exception as e:
        return render_template('error.html', error="Error loading content")

@app.route('/movies')
def movies():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        all_movies = dbHandler.get_all_movies()
        free_movies = dbHandler.get_free_movies()
        return render_template('movies.html', 
                             all_movies=all_movies,
                             free_movies=free_movies)
    except Exception as e:
        return render_template('error.html', error="Error loading movies")

@app.route('/shows')
def shows():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        all_shows = dbHandler.get_all_shows()
        free_shows = dbHandler.get_free_shows()
        return render_template('shows.html', 
                             all_shows=all_shows,
                             free_shows=free_shows)
    except Exception as e:
        return render_template('error.html', error="Error loading shows")

@app.route('/search')
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('q', '')
    if query:
        try:
            movies = dbHandler.search_movies(query)
            shows = dbHandler.search_shows(query)
        except Exception as e:
            movies = []
            shows = []
    else:
        movies = []
        shows = []
    
    return render_template('search.html', 
                         movies=movies, 
                         shows=shows, 
                         query=query)

@app.route('/watchlist')
def watchlist():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        watchlist_items = dbHandler.get_watchlist(session['user_id'])
        return render_template('watchlist.html', watchlist=watchlist_items)
    except Exception as e:
        return render_template('error.html', error="Error loading watchlist")

@app.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    item_id = request.json.get('item_id')
    item_type = request.json.get('item_type')
    
    if dbHandler.add_to_watchlist(session['user_id'], item_id, item_type):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Already in watchlist'})

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        # Get movie details and platforms
        conn = dbHandler.get_db_connection()
        movie = conn.execute('SELECT * FROM movies WHERE movieID = ?', (movie_id,)).fetchone()
        platforms = dbHandler.get_movie_platforms(movie_id)
        conn.close()
        
        if not movie:
            return render_template('error.html', error="Movie not found")
            
        return render_template('movie_detail.html', movie=movie, platforms=platforms)
    except Exception as e:
        return render_template('error.html', error="Error loading movie details")

@app.route('/show/<int:show_id>')
def show_detail(show_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        # Get show details and platforms
        conn = dbHandler.get_db_connection()
        show = conn.execute('SELECT * FROM shows WHERE showID = ?', (show_id,)).fetchone()
        platforms = dbHandler.get_show_platforms(show_id)
        conn.close()
        
        if not show:
            return render_template('error.html', error="Show not found")
            
        return render_template('show_detail.html', show=show, platforms=platforms)
    except Exception as e:
        return render_template('error.html', error="Error loading show details")

# Error handler
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error="Internal server error"), 500

if __name__ == '__main__':
    print("Starting StreamFinder application...")
    print("Initializing database tables...")
    dbHandler.init_tables()
    print("Database initialized successfully!")
    app.run(debug=True, host='0.0.0.0', port=10000)