import requests
import os
from datetime import datetime
from requests.auth import HTTPBasicAuth
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

# Import config loader to set environment variables
from ..config_loader import config

GITHUB_TOKEN: str = os.getenv('GITHUB_TOKEN', '')
if not GITHUB_TOKEN:
    raise ValueError("Missing required GitHub token. Please check your config.json file.")

GITHUB_HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}
GITHUB_BASE_URL = "https://api.github.com"


class GithubToolInput(BaseModel):
    """Input schema for GithubTool."""
    username: str = Field(..., description="Github username.")
    start_date: str = Field(..., description="Start date for fetching data.")
    end_date: str = Field(..., description="End date for fetching data.")


class GithubTool(BaseTool):
    name: str = "Github Tool"
    description: str = (
        "This tool is used to fetch data from Github about user´s activity"
    )
    args_schema: Type[BaseModel] = GithubToolInput

    def _run(self, username: str, start_date: str, end_date: str) -> dict:
        github_data =  self.get_github_data(username, start_date, end_date)
        participation_data = self.get_participation_data(username, start_date, end_date)
        return {
            "personal_data": github_data,
            "participation_data": participation_data
        }

    def get_github_data(self, username: str, start_date: str, end_date: str) -> dict:
        # Search for PRs in the invibeme organization
        url = f'{GITHUB_BASE_URL}/search/issues?q=author:{username}+org:invibeme+type:pr+created:{start_date}..{end_date}'
        response = requests.get(url, headers=GITHUB_HEADERS)
        if not response.ok or response.status_code != 200:
            raise Exception(f"Failed to fetch data from Github. Response: {response.text}")
        
        response_data = response.json()
        
        # Log the query for debugging
        print(f"GitHub API Query: {url}")
        print(f"Total PRs found: {response_data.get('total_count', 0)}")
        
        return response_data


    def get_participation_data(self, username: str, start_date: str, end_date: str) -> dict:
        # Search for PRs where the user commented in the invibeme organization
        url = f'{GITHUB_BASE_URL}/search/issues?q=commenter:{username}+org:invibeme+type:pr+created:{start_date}..{end_date}'
        response = requests.get(url, headers=GITHUB_HEADERS)
        if not response.ok or response.status_code != 200:
            raise Exception(f"Failed to fetch data from Github. Response: {response.text}")
        
        response_data = response.json()

        index_to_remove = []
        for i, item in enumerate(response_data['items']):
            if item['user']['login'] == username:
                index_to_remove.append(i)

        for i in index_to_remove:
            response_data['items'].pop(i)

        return response_data

if __name__ == "__main__":
    github_tool = GithubTool()
    print(github_tool._run(
        username="Tolosa527",
        start_date="2025-07-07",
        end_date="2025-07-12"
    ))
