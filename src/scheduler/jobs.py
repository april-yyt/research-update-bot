"""
Job scheduling and execution functions.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from src.arxiv_integration.client import search_arxiv_papers
from src.llm_integration.summarizer import summarize_papers
from src.slack_app.views import create_research_update_blocks
from src.database.models import get_all_configs
import logging
from datetime import datetime, timezone, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_scheduler():
    """
    Initialize and start the job scheduler.
    
    Returns:
        BackgroundScheduler: Initialized scheduler
    """
    scheduler = BackgroundScheduler()
    scheduler.start()
    return scheduler

def load_existing_jobs(scheduler, app):
    """
    Load and schedule jobs for all existing configurations.
    
    Args:
        scheduler: The job scheduler
        app: Slack app instance
    """
    configs = get_all_configs()
    for config in configs:
        setup_scheduled_job(config, scheduler, app)

def setup_scheduled_job(config, scheduler=None, app=None):
    """
    Set up a scheduled job for a research update configuration.
    
    Args:
        config (dict): The configuration for the job
        scheduler: The job scheduler (optional)
        app: Slack app instance (optional)
    """
    if scheduler is None:
        scheduler = initialize_scheduler()
    
    # Remove any existing job for this config
    job_id = f"research_update_{config['id']}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
    
    # Set up cron schedule
    if config['frequency'] == 'daily':
        trigger = CronTrigger(hour=9, minute=0)  # Run at 9:00 AM daily
    else:  # weekly
        trigger = CronTrigger(day_of_week='mon', hour=9, minute=0)  # Monday at 9:00 AM
    
    # Add the job to the scheduler
    scheduler.add_job(
        run_research_update,
        trigger=trigger,
        id=job_id,
        args=[config, app],
        replace_existing=True
    )
    
    # Format topics for logging
    all_topics = [config["topic"]] + config.get("additional_topics", [])
    topics_text = ", ".join(all_topics)
    
    logger.info(f"Scheduled job {job_id} - {config['frequency']} updates for topics: {topics_text}")

def run_research_update(config, app_or_client):
    """
    Execute a research update job.
    
    Args:
        config (dict): The configuration for the job
        app_or_client: Slack app instance or WebClient
    """
    try:
        # Handle both app object and direct client object
        if hasattr(app_or_client, 'client'):
            client = app_or_client.client
        else:
            client = app_or_client
            
        # Gather all topics
        topics = [config['topic']]
        if config.get('additional_topics'):
            topics.extend(config['additional_topics'])
            
        logger.info(f"Running research update for topics: {', '.join(topics)}")
        
        # Convert time_range to int if it's a string
        time_range = config['time_range']
        if isinstance(time_range, str):
            try:
                time_range = int(time_range)
            except ValueError:
                raise ValueError(f"Invalid time_range value: {time_range}")
        
        # Ensure time_range is valid
        if not isinstance(time_range, int):
            raise ValueError(f"Invalid time_range value: {time_range}")

        # Compute start date for search
        start_date = datetime.now(timezone.utc) - timedelta(days=time_range)
        
        # Search for relevant papers
        papers = search_arxiv_papers(topics, time_range)
        
        if not papers:
            logger.info(f"No relevant papers found for topics: {', '.join(topics)}")
            client.chat_postMessage(
                channel=config['channel'],
                text=f"No new research papers found for topics: {', '.join(topics)} in the past {time_range} days."
            )
            return
        
        # Generate summary with LLM
        summary = summarize_papers(papers, topics)
        
        # Post to Slack
        blocks = create_research_update_blocks(summary, config, papers)
        client.chat_postMessage(
            channel=config['channel'],
            text="Research Update",
            blocks=blocks
        )
        
        logger.info(f"Successfully posted research update for topics: {', '.join(topics)}")
        
    except Exception as e:
        # Log error and notify admin
        error_msg = f"Error in research update job for topics {', '.join(topics)}: {str(e)}"
        logger.error(error_msg)
        
        try:
            client.chat_postMessage(
                channel=config['channel'],
                text=f"Error generating research update: {str(e)}"
            )
        except Exception as inner_e:
            logger.error(f"Failed to send error message to Slack: {str(inner_e)}")