#!/usr/bin/env python3
"""
Main entry point for the Research Daily Update Bot.
Initializes all components and starts the application.
"""
import os
from dotenv import load_dotenv
from src.slack_app.app import create_slack_app, start_socket_mode
from src.database.connection import init_db
from src.scheduler.jobs import initialize_scheduler, load_existing_jobs

def main():
    # Load environment variables
    load_dotenv()
    
    print("Environment loaded")
    print(f"Bot token starts with: {os.environ.get('SLACK_BOT_TOKEN', 'Not found')[:10]}...")
    print(f"App token starts with: {os.environ.get('SLACK_APP_TOKEN', 'Not found')[:10]}...")
    
    # Initialize database
    init_db()
    
    # Create and configure the Slack app
    print("Creating Slack app...")
    app = create_slack_app()
    
    # Initialize scheduler and load existing jobs
    print("Initializing scheduler...")
    scheduler = initialize_scheduler()
    load_existing_jobs(scheduler, app)
    
    print("Research Daily Update Bot is ready! Starting socket mode...")
    try:
        # Start the Slack app in socket mode
        start_socket_mode(app)
        print("Socket mode started successfully")
    except Exception as e:
        print(f"Error starting socket mode: {str(e)}")

if __name__ == "__main__":
    main()