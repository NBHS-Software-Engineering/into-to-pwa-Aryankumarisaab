import sqlite3
import os

def init_database():
    # Connect to database
    conn = sqlite3.connect('database/data_source.db')
    cursor = conn.cursor()
    
    # Read and execute the SQL file
    with open('database/my_queries.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    
    # Split the script into individual statements
    statements = sql_script.split(';')
    
    for statement in statements:
        statement = statement.strip()
        if statement:  # Only execute non-empty statements
            try:
                cursor.execute(statement)
                print(f"Executed: {statement[:50]}...")
            except sqlite3.OperationalError as e:
                if "already exists" not in str(e):
                    print(f"Error executing: {statement[:50]}...")
                    print(f"Error: {e}")
    
    conn.commit()
    conn.close()
    print("Database initialization completed!")

if __name__ == '__main__':
    init_database()