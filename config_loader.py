import json
import os
from pathlib import Path

def load_config():
    """Load configuration from config.json file"""
    config_path = Path(__file__).parent.parent / "config.json"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Set environment variables
    os.environ['OPENAI_API_KEY'] = config['open_ai_api_key']
    os.environ['JIRA_USER'] = config['jira_user']
    os.environ['JIRA_API_TOKEN'] = config['jira_api_token']
    os.environ['JIRA_URL'] = config['jira_url']
    os.environ['GITHUB_TOKEN'] = config['github_token']
    os.environ['GITHUB_USERNAME'] = config['github_username']
    os.environ['SLACK_TOKEN'] = config.get('slack_token', '')
    os.environ['SLACK_CHANNEL_ID'] = config.get('slack_channel_id', '')
    
    return config

# Load configuration when module is imported
config = load_config()
