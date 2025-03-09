"""
Slack event and command handlers.
"""
from src.slack_app.views import get_config_modal
from src.database.models import save_config, get_all_configs
from src.scheduler.jobs import setup_scheduled_job, run_research_update

def register_handlers(app):
    """
    Register all event and command handlers with the Slack app.
    
    Args:
        app: Slack Bolt app
    """
    # Register slash command handler
    app.command("/configure-research-bot")(open_config_modal)
    
    # Register view submission handler
    app.view("research_config")(handle_config_submission)
    
    # Add test command
    app.command("/test-research-update")(test_research_update)

def open_config_modal(ack, body, client):
    """
    Open the configuration modal when the slash command is used.
    
    Args:
        ack: Acknowledge function
        body: Request body
        client: Slack client
    """
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view=get_config_modal()
    )

def handle_config_submission(ack, body, view, client):
    """
    Process the submission of the configuration modal.
    
    Args:
        ack: Acknowledge function
        body: Request body
        view: View payload
        client: Slack client
    """
    ack()
    
    # Extract values from submission
    values = view["state"]["values"]
    
    # Parse additional topics
    additional_topics_text = values["additional_topics"]["additional_topics_input"]["value"] if "additional_topics" in values else ""
    additional_topics = [topic.strip() for topic in additional_topics_text.split("\n") if topic.strip()] if additional_topics_text else []
    
    # Convert time_range to integer
    try:
        time_range = int(values["time_range"]["time_range_select"]["selected_option"]["value"])
    except (KeyError, ValueError) as e:
        client.chat_postMessage(
            channel=body["user"]["id"],
            text="Invalid time range value. Please select a valid number of days."
        )
        return

    config = {
        "frequency": values["frequency"]["frequency_select"]["selected_option"]["value"],
        "time_range": time_range,  # Now stored as integer
        "topic": values["main_topic"]["topic_input"]["value"],
        "additional_topics": additional_topics,
        "channel": values["channel"]["channel_select"]["selected_channel"]
    }
    
    # Save configuration to database
    config_id = save_config(config)
    config["id"] = config_id
    
    # Set up the job in the scheduler
    setup_scheduled_job(config)
    
    # Format topics for display
    all_topics = [config["topic"]] + config["additional_topics"]
    topics_text = ", ".join(all_topics)
    
    # Notify the user
    client.chat_postMessage(
        channel=body["user"]["id"],
        text=f"Research bot configured successfully! Updates on topics: {topics_text} will be posted to <#{config['channel']}> {config['frequency']}."
    )

def test_research_update(ack, body, client, logger):
    """
    Test command to manually trigger a research update.
    
    Args:
        ack: Acknowledge function
        body: Request body
        client: Slack client
        logger: Logger instance
    """
    ack()
    
    # Get the first available configuration or use default values
    configs = get_all_configs()
    if configs:
        config = configs[0]
        client.chat_postMessage(
            channel=body["channel_id"],
            text=f"Running test research update using configuration ID: {config['id']}..."
        )
        
        try:
            # Run the update process - pass just the client instead of client.app
            run_research_update(config, client)
        except Exception as e:
            logger.error(f"Error running research update: {str(e)}")
            client.chat_postMessage(
                channel=body["channel_id"],
                text=f"Error running research update: {str(e)}"
            )
    else:
        client.chat_postMessage(
            channel=body["channel_id"],
            text="No configurations found. Please set up a configuration first using /configure-research-bot"
        )