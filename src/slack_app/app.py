"""
Slack app initialization and configuration.
"""
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from src.slack_app.handlers import register_handlers
from src.slack_app.views import create_home_tab_view

def create_slack_app():
    """
    Create and configure the Slack Bolt app.
    
    Returns:
        App: Configured Slack Bolt app
    """
    # Initialize app with tokens from environment
    app = App(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
    )
    
    # Add home tab handler
    @app.event("app_home_opened")
    def handle_home_tab(client, event, logger):
        try:
            client.views_publish(
                user_id=event["user"],
                view=create_home_tab_view()
            )
        except Exception as e:
            logger.error(f"Error publishing home tab: {e}")

    # Register command and event handlers
    register_handlers(app)
    
    return app

def start_socket_mode(app):
    """
    Start the Slack app in Socket Mode.
    
    Args:
        app: Configured Slack Bolt app
    """
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start() 