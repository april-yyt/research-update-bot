"""
Database models and operations.
"""
from src.database.connection import get_db_connection
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_config(config):
    """
    Save a new configuration to the database.
    
    Args:
        config (dict): Configuration dictionary
        
    Returns:
        int: ID of the inserted configuration
    """
    conn = get_db_connection()
    try:
        # Convert list of additional topics to JSON string for storage
        additional_topics = json.dumps(config.get('additional_topics', []))
        
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO configurations (frequency, time_range, topic, additional_topics, channel)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            config['frequency'],
            config['time_range'],
            config['topic'],
            additional_topics,
            config['channel']
        ))
        conn.commit()
        
        # Get the ID of the inserted row
        config_id = cursor.lastrowid
        logger.info(f"Saved configuration with ID: {config_id}")
        return config_id
    except Exception as e:
        logger.error(f"Error saving configuration: {str(e)}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_config(config_id):
    """
    Get a specific configuration by ID.
    
    Args:
        config_id (int): Configuration ID
        
    Returns:
        dict: Configuration dictionary or None if not found
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM configurations WHERE id = ?', (config_id,))
        row = cursor.fetchone()
        
        if row:
            config = dict(row)
            # Parse JSON string back to list
            config['additional_topics'] = json.loads(config['additional_topics'])
            return config
        return None
    except Exception as e:
        logger.error(f"Error getting configuration: {str(e)}")
        return None
    finally:
        conn.close()

def get_all_configs():
    """
    Get all saved configurations.
    
    Returns:
        list: List of configuration dictionaries
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM configurations')
        rows = cursor.fetchall()
        
        # Convert rows to dictionaries and parse JSON
        configs = []
        for row in rows:
            config = dict(row)
            config['additional_topics'] = json.loads(config['additional_topics'])
            configs.append(config)
            
        logger.info(f"Retrieved {len(configs)} configurations")
        return configs
    except Exception as e:
        logger.error(f"Error getting configurations: {str(e)}")
        return []
    finally:
        conn.close()

def update_config(config_id, config_data):
    """
    Update an existing configuration.
    
    Args:
        config_id (int): Configuration ID
        config_data (dict): Updated configuration data
        
    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_db_connection()
    try:
        # Convert list of additional topics to JSON string for storage
        additional_topics = json.dumps(config_data.get('additional_topics', []))
        
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE configurations
        SET frequency = ?, time_range = ?, topic = ?, additional_topics = ?, channel = ?
        WHERE id = ?
        ''', (
            config_data['frequency'],
            config_data['time_range'],
            config_data['topic'],
            additional_topics,
            config_data['channel'],
            config_id
        ))
        conn.commit()
        
        logger.info(f"Updated configuration with ID: {config_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating configuration: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()

def delete_config(config_id):
    """
    Delete a configuration.
    
    Args:
        config_id (int): Configuration ID
        
    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM configurations WHERE id = ?', (config_id,))
        conn.commit()
        
        logger.info(f"Deleted configuration with ID: {config_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting configuration: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()