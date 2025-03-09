"""
Client for searching and fetching papers from arXiv.
"""
import arxiv
from datetime import datetime, timezone, timedelta
import logging

logger = logging.getLogger(__name__)

def search_arxiv_papers(topics, time_range_days):
    """
    Search arXiv for papers matching the given topics within the time range.
    
    Args:
        topics (list): List of search topics
        time_range_days (int): Number of days to look back
        
    Returns:
        list: List of paper entries
    """
    client = arxiv.Client()
    query = " OR ".join([f'"{topic}"' for topic in topics])
    
    # Calculate cutoff date with UTC timezone
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=time_range_days)
    
    search = arxiv.Search(
        query=query,
        max_results=100,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )
    
    try:
        results = client.results(search)
        papers = []
        
        for result in results:
            # Convert arXiv datetime to UTC-aware datetime
            published_utc = result.published.astimezone(timezone.utc)
            
            if published_utc > cutoff_date:
                papers.append({
                    "title": result.title,
                    "authors": [a.name for a in result.authors],
                    "abstract": result.summary,
                    "published": published_utc,
                    "pdf_url": result.pdf_url.replace("http://", "https://").replace(" ", "%20"),
                    "doi": result.doi or ""
                })
                
        logger.info(f"Found {len(papers)} recent papers matching topics: {', '.join(topics)}")
        return papers
        
    except Exception as e:
        logger.error(f"Error searching arXiv: {str(e)}")
        return []