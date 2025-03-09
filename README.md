# Research Daily Update Bot 🔬

A Slackbot that automatically delivers daily research updates by finding relevant arXiv papers and formatting them into readable Slack messages. 

## Key Features ✨
- **Automated arXiv Monitoring**  
   Tracks new papers based on configured research topics
- **Smart Summarization**  
   Uses NVIDIA NIMs (LLama 3 70B) to generate concise summaries
- **Slack Integration**  
   Posts formatted updates with proper markdown links and emojis
- **Custom Scheduling**  
   Configurable update frequency (daily/weekly) and lookback period
- **Multi-Topic Support**  
   Monitor multiple research areas simultaneously

## Setup 🔧

### Prerequisites
- Python 3.9+
- Slack workspace with admin permissions
- NVIDIA API key for LLM access

### Installation
1. Clone the repository
   ```bash
   git clone https://github.com/your-org/research-daily-update-bot.git
   cd research-daily-update-bot
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables (create `.env` file)
   ```ini
   SLACK_BOT_TOKEN=xoxb-...
   SLACK_APP_TOKEN=xapp-...
   NVIDIA_API_KEY=your-nvidia-key
   DB_PATH=research_bot.db
   ```

### Slack App Configuration
1. Create new Slack App at [api.slack.com](https://api.slack.com/apps)
2. Add following OAuth scopes:
   - `chat:write`
   - `commands`
   - `channels:read`
3. Install app to your workspace
4. Enable Socket Mode in app settings

## Usage :rocket:

### Running the Bot
```bash
# Using Docker
docker-compose up --build

# Or directly via Python
python -m src.main
```

### Configuring Research Topics
1. In Slack, use the command:
   ```
   /configure-research-bot
   ```
2. Fill in the modal:
   - Main research topic
   - Additional topics (optional)
   - Update frequency (daily/weekly)
   - Lookback period (1-30 days)
   - Target channel

3. Sample configuration:
   ```plaintext
   Main Topic: Computer Vision
   Additional Topics: Neural Rendering, Diffusion Models
   Frequency: Daily
   Lookback: 3 days
   Channel: #research-updates
   ```

### Example Output 📑
```markdown
📖 *Recent Papers in Computer Vision*

✨ <https://arxiv.org/pdf/2503.04634v1|PathoPainter: Tumor-aware Inpainting>
📌 _Key Contribution_: Novel inpainting method for histopathology images
🔎 _Why It Matters_: Improves segmentation accuracy by 15%

📄 <https://arxiv.org/pdf/2503.05112v1|Diffusion Models for 3D Shape Generation>
📌 _Key Contribution_: New sampling strategy for 3D diffusion
🔎 _Why It Matters_: Reduces generation time by 40%

🕞 Papers from last 3 days | 🔢 12 papers found
```

## Commands ⌨️
- `/configure-research-bot` - Set up new monitoring configuration
- `/test-research-update` - Trigger immediate update for testing
- `/list-research-configs` - Show active configurations
- `/delete-research-config` - Remove a configuration

## Troubleshooting 🚑
**Common Issues:**
1. *"Invalid Blocks" Error*  
   Ensure summaries are under 3000 characters per section

2. *Missing Papers*  
   Verify arXiv search terms and time range configuration

3. *Slack Permission Errors*  
   Reinstall app with correct OAuth scopes:
   - `chat:write`
   - `commands`
   - `channels:read`

**Logs:**
```bash
# View Docker logs
docker-compose logs -f

# Debug mode
DEBUG=true python -m src.main
```
