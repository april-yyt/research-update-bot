"""
Default configuration settings for the Research Daily Update Bot.
"""
import os

# Application settings
APP_NAME = "Research Daily Update Bot"
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# Scheduler settings
DEFAULT_TIME_HOUR = 9  # 9 AM
DEFAULT_TIME_MINUTE = 0  # 0 minutes

# ArXiv settings
MAX_PAPERS = 10
DEFAULT_TIME_RANGE = 7  # 7 days

# NVIDIA NIMs LLM settings
DEFAULT_LLM_MODEL = "meta/llama-3.3-70b-instruct"
LLM_TEMPERATURE = 0.2
LLM_TOP_P = 0.7
LLM_MAX_TOKENS = 1024