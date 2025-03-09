"""
Jira API client for connecting to Jira and fetching data.
"""
import os
from jira import JIRA

def get_jira_client():
    """
    Create and return a configured Jira client.
    
    Returns:
        JIRA: Configured Jira client
    """
    return JIRA(
        server=os.environ["JIRA_SERVER"],
        basic_auth=(os.environ["JIRA_USER"], os.environ["JIRA_API_TOKEN"])
    )