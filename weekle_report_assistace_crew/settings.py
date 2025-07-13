import os
import json
from dataclasses import dataclass
from typing import Optional, Dict
from logging import getLogger

logger = getLogger(__name__)

@dataclass
class Settings:
    model_type: str = "gpt-3.5-turbo"
    llm_type: str = "openai"
    jira_user: str = ""
    jira_api_token: str = ""
    jira_url: str = ""
    github_token: str = ""
    github_username: str = ""
    slack_token: str = ""
    slack_channel_id: str = ""
    github_headers: Optional[Dict[str, str]] = None
    open_ai_api_key: str = ""
    database_name: str = "messages.db"
    debug: bool = False

    def __post_init__(self, **values):
        super().__init__(**values)
        script_directory = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_directory, "config.json")
        with open(config_path) as f:
            data = json.load(f)
            self.debug = data.get('debug', self.debug)
            self.jira_user = data['jira_user']
            self.jira_api_token = data['jira_api_token']
            self.jira_url = data['jira_url']
            self.github_token = data['github_token']
            self.github_headers = {'Authorization': f'token {self.github_token}'}
            self.slack_token = data['slack_token']
            self.github_username = data['github_username']
            self.open_ai_api_key = data['open_ai_api_key']
            self.database_name = data.get('database_name', self.database_name)
            self.model_type = data.get('model_type', self.model_type)
            self.llm_type = data.get('llm_type', self.llm_type)

            self.slack_channel_id = (
                "C075Z414VL5"
                if self.debug
                else data['slack_channel_id']
            )

    @property
    def get_jira_user(self) -> str:
        return self.jira_user
    
    @property
    def get_jira_api_token(self) -> str:
        return self.jira_api_token
    
    @property
    def get_jira_url(self) -> str:
        return self.jira_url
    
    @property
    def get_github_headers(self) -> Dict[str, str]:
        return self.github_headers
    
    @property
    def get_github_username(self) -> str:
        return self.github_username
    
    @property
    def get_slack_token(self) -> str:
        return self.slack_token
    
    @property
    def get_slack_channel_id(self) -> str:
        return self.slack_channel_id
    
    @property
    def get_open_ai_api_key(self) -> str:
        return self.open_ai_api_key
    
    @property
    def get_database_name(self) -> str:
        return self.database_name
    
    @property
    def get_model_type(self) -> str:
        return self.model_type
    
    @property
    def get_llm_type(self) -> str:
        return self.llm_type
   
    
try:
    settings = Settings()
except Exception as e:
    logger.error("Configuration error:", e)