from setuptools import setup, find_packages

setup(
    name="research-daily-update-bot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "slack-bolt>=1.16.0",
        "jira>=3.4.1",
        "arxiv>=1.4.7",
        "openai>=1.0.0",
        "apscheduler>=3.10.0",
        "python-dotenv>=1.0.0",
    ],
    author="April Yang",
    author_email="yutongy@nvidia.com",
    description="A Slackbot that syncs Jira tickets with relevant arXiv papers and delivers research summaries.",
    keywords="slack, jira, arxiv, research, bot",
    python_requires=">=3.7",
)