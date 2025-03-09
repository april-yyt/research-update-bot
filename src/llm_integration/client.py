"""
Client for interacting with NVIDIA NIMs LLM services.
"""
import os
from openai import OpenAI

def get_llm_client():
    """
    Configure and return the NVIDIA NIMs client using OpenAI-compatible interface.
    
    Returns:
        OpenAI: Configured NVIDIA NIMs client
    """
    api_key = os.environ.get("NVIDIA_API_KEY", "")
    
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )
    
    return client