"""
Slack UI elements for the bot configuration.
"""

def get_config_modal():
    """
    Generate the modal view for bot configuration.
    
    Returns:
        dict: Slack Block Kit modal definition
    """
    return {
        "type": "modal",
        "callback_id": "research_config",
        "title": {"type": "plain_text", "text": "Configure Research Bot"},
        "submit": {"type": "plain_text", "text": "Submit"},
        "blocks": [
            # Frequency selector
            {
                "type": "input",
                "block_id": "frequency",
                "element": {
                    "type": "static_select",
                    "action_id": "frequency_select",
                    "options": [
                        {"text": {"type": "plain_text", "text": "Daily"}, "value": "daily"},
                        {"text": {"type": "plain_text", "text": "Weekly"}, "value": "weekly"}
                    ]
                },
                "label": {"type": "plain_text", "text": "Update Frequency"}
            },
            # Time range for arXiv papers
            {
                "type": "input",
                "block_id": "time_range",
                "element": {
                    "type": "static_select",
                    "action_id": "time_range_select",
                    "options": [
                        {"text": {"type": "plain_text", "text": "Past week"}, "value": "7"},
                        {"text": {"type": "plain_text", "text": "Past month"}, "value": "30"}
                    ]
                },
                "label": {"type": "plain_text", "text": "Paper Time Range (days)"}
            },
            # Main topic
            {
                "type": "input",
                "block_id": "main_topic",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "topic_input"
                },
                "label": {"type": "plain_text", "text": "Main Research Topic"}
            },
            # Additional topics
            {
                "type": "input",
                "block_id": "additional_topics",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "additional_topics_input",
                    "multiline": True
                },
                "label": {"type": "plain_text", "text": "Additional Topics (One per line)"},
                "optional": True,
                "hint": {"type": "plain_text", "text": "Enter additional topics, one per line"}
            },
            # Slack channel to post updates
            {
                "type": "input",
                "block_id": "channel",
                "element": {
                    "type": "channels_select",
                    "action_id": "channel_select"
                },
                "label": {"type": "plain_text", "text": "Post Updates To"}
            }
        ]
    }

def create_research_update_blocks(summary, config, papers):
    """
    Create formatted Slack message blocks with proper length validation.
    """
    topics = [config['topic']] + config.get('additional_topics', [])
    
    # Split summary into chunks under 3000 characters
    summary_chunks = []
    current_chunk = []
    current_length = 0
    
    for line in summary.split('\n'):
        line_length = len(line)
        if current_length + line_length > 2500:  # Leave room for markdown formatting
            summary_chunks.append("\n".join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(line)
        current_length += line_length
    
    if current_chunk:
        summary_chunks.append("\n".join(current_chunk))

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f":microscope: Latest Research in {', '.join(topics)}"
            }
        }
    ]
    
    # Add summary chunks as separate sections
    for i, chunk in enumerate(summary_chunks, 1):
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Part {i}:*\n{chunk}"
            }
        })
    
    # Add context block at the end
    blocks.append({
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": f":clock3: Papers from last {config['time_range']} days | "
                        f":1234: {len(papers)} papers found"
            }
        ]
    })
    
    return blocks

def create_home_tab_view():
    """Create the app home view with introduction and quick actions"""
    return {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🔬 Research Daily Update Bot :lab_coat:",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Welcome to your AI Research Assistant!* \nI automatically track arXiv papers and deliver curated updates to your Slack channels."
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "✨ *Key Features*\n• Daily/weekly research digests\n• Multi-topic monitoring\n• LLM-powered summaries (Llama 3 70B)\n• Customizable filters and schedules"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "⚙️ Configure Bot",
                            "emoji": True
                        },
                        "value": "configure",
                        "action_id": "open_config_modal"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "🔍 Test Update",
                            "emoji": True
                        },
                        "value": "test_update",
                        "action_id": "trigger_test_update"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "📘 *Getting Started*\n1. Use `/configure-research-bot` to set up your first monitor\n2. Specify your research topics (e.g. `LLM`, `Diffusion Models`)\n3. Choose update frequency and channel\n4. Let me handle the rest!"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "🔧 *Commands*\n`/configure-research-bot` - Set up new monitoring\n`/test-research-update` - Trigger immediate update\n`/list-research-configs` - Show active configurations"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "🔍 _Tracking research areas:_ Computer Vision • NLP • Generative AI • Robotics\n"
                                "📆 _Next scheduled update:_ Today at 9:00 AM\n"
                                "📧 _Contact:_ <mailto:yutongy@nvidia.com|April Yang>"
                    }
                ]
            }
        ]
    }