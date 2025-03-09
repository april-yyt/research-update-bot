"""
Functions for fetching and processing Jira tickets.
"""
from src.jira_integration.client import get_jira_client

def get_tickets_from_epic(epic_id):
    """
    Fetch all tickets belonging to a specific Jira epic.
    
    Args:
        epic_id (str): The ID of the Jira epic
        
    Returns:
        list: List of ticket dictionaries with relevant information
    """
    jira = get_jira_client()
    
    # JQL query to get all issues in the epic
    jql_query = f'parent = {epic_id} OR "Epic Link" = {epic_id}'
    issues = jira.search_issues(jql_query)
    
    # Extract relevant information
    tickets = []
    for issue in issues:
        tickets.append({
            "key": issue.key,
            "summary": issue.fields.summary,
            "description": issue.fields.description,
            "status": issue.fields.status.name,
            "labels": issue.fields.labels
        })
    
    return tickets

def extract_topics_from_tickets(tickets):
    """
    Extract potential research topics from ticket information.
    
    Args:
        tickets (list): List of ticket dictionaries
        
    Returns:
        list: List of extracted topics
    """
    # Extract keywords from ticket summaries and descriptions
    topics = set()
    for ticket in tickets:
        # Add labels as topics
        topics.update(ticket.get("labels", []))
        
        # Extract key terms from summary
        if ticket.get("summary"):
            summary_words = ticket["summary"].lower().split()
            topics.update([word for word in summary_words if len(word) > 5])
        
    return list(topics)