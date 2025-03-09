"""
Module for summarizing research papers using NVIDIA NIMs.
"""
from typing import List, Dict
import logging
from src.llm_integration.client import get_llm_client

logger = logging.getLogger(__name__)

def summarize_papers(papers: List[Dict], topics: List[str]) -> str:
    """
    Generate a formatted summary of research papers with metadata.
    """
    client = get_llm_client()
    topics_text = ", ".join(topics)
    
    # Format papers with metadata for LLM input
    formatted_papers = "\n\n".join(
        f"Title: {paper['title']}\n"
        f"PDF URL: {paper['pdf_url']}\n"
        f"Abstract: {paper['abstract'][:500]}..."
        for paper in papers[:15]
    )

    try:
        response = client.chat.completions.create(
            model="meta/llama-3.3-70b-instruct",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a research assistant formatting paper summaries for Slack. Use markdown links and emojis."
                },
                {
                    "role": "user",
                    "content": f"""Format these papers about {topics_text} into a Slack message:
                    
                    {formatted_papers}
                    
                    Structure:
                    :books: *Recent Papers in {topics_text}*
                    
                    For each paper:
                    :page_facing_up: <{{pdf_url}}|{{Title}}> 
                    :pushpin: _Key Contribution_: [1-sentence summary]
                    :mag: _Why It Matters_: [1-sentence significance]
                    
                    - Use :star: for important papers. 
                    - Replace {{pdf_url}} with the FULL URL from "PDF URL"
                    - Replace {{Title}} with EXACT paper title
                    - URLs MUST start with https://
                    - Remove any markdown except the <URL|TEXT> format"""
                }
            ],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Summarization error: {str(e)}")
        return f"Error generating research summary: {str(e)}"