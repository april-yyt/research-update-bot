"""
Functions for parsing and processing arXiv paper data.
"""

def format_papers_for_llm(papers):
    """
    Format paper information in a structure suitable for LLM input.
    
    Args:
        papers (list): List of paper dictionaries
        
    Returns:
        str: Formatted paper information
    """
    formatted_papers = []
    
    for i, paper in enumerate(papers, 1):
        authors = ", ".join(paper["authors"][:3])
        if len(paper["authors"]) > 3:
            authors += ", et al."
            
        formatted_paper = f"""
Paper {i}:
Title: {paper["title"]}
Authors: {authors}
Published: {paper["published"].strftime('%Y-%m-%d')}
Summary: {paper["summary"][:300]}...
URL: {paper["entry_id"]}
"""
        formatted_papers.append(formatted_paper)
    
    return "\n".join(formatted_papers)