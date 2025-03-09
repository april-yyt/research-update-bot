"""
Database connection and initialization.
"""
import sqlite3
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database file location
DB_PATH = os.environ.get("DB_PATH", "research_bot.db")

def get_db_connection():
    """
    Create and return a database connection.
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    conn = sqlite3.connect(DB_PATH)
    # Enable row factory to return rows as dictionaries
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Initialize the database schema if it doesn't exist.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS configurations (
            id INTEGER PRIMARY KEY,
            frequency TEXT,
            time_range INTEGER,
            topic TEXT,
            additional_topics TEXT,
            channel TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
    finally:
        conn.close()