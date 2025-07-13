import requests
import os
from datetime import datetime
from requests.auth import HTTPBasicAuth
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

# Import config loader to set environment variables
from ..config_loader import config

JIRA_USER: str = os.getenv('JIRA_USER', '')
JIRA_API_TOKEN: str = os.getenv('JIRA_API_TOKEN', '')
JIRA_URL: str = os.getenv('JIRA_URL', '')

# Validate required environment variables
if not JIRA_USER or not JIRA_API_TOKEN or not JIRA_URL:
    raise ValueError("Missing required Jira configuration. Please check your config.json file.")


class JiraToolInput(BaseModel):
    """Input schema for JiraTool."""
    username: str = Field(..., description="Jira username.")
    start_date: str = Field(..., description="Start date for fetching data.")
    end_date: str = Field(..., description="End date for fetching data.")

class JiraTool(BaseTool):
    name: str = "Jira Tool"
    description: str = (
        "This tool is used to fetch data from Jira."
    )
    args_schema: Type[BaseModel] = JiraToolInput

    def _run(self, username: str, start_date: str, end_date: str) -> dict:
        jira_data = self.get_jira_data(username, start_date, end_date)
        return jira_data


    def verify_date_format(self, start_date: str, end_date: str) -> bool:
        try:
            datetime.strptime(start_date, '%Y/%m/%d')
            datetime.strptime(end_date, '%Y/%m/%d')
            return True
        except ValueError:
            return False


    def get_jira_data(self, username: str, start_date: str, end_date: str) -> dict:

        if not self.verify_date_format(start_date, end_date):
            start_date = start_date.replace('-', '/')
            end_date = end_date.replace('-', '/')

        auth = HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN)
        headers = {"Accept": "application/json"}
        jql = (
            f'assignee = "{username}" '
            + (f'AND updated >= startOfDay("-7d") ' if not start_date else f'AND updated >= "{start_date}" ')
            + (f'AND updated <= endOfDay() ' if not end_date else f'AND updated <= "{end_date}" ')
            + 'ORDER BY updated DESC'
        )
        url = f'{JIRA_URL}/rest/api/3/search?jql={jql}'
        response = requests.get(url, headers=headers, auth=auth)
        return response.json()

    def get_statuses(self) -> dict:
        auth = HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN)
        headers = {"Accept": "application/json"}
        url = f'{JIRA_URL}/rest/api/3/status'
        response = requests.get(url, headers=headers, auth=auth)
        return response.json()


if __name__ == "__main__":
    jira_tool = JiraTool()
    print(jira_tool._run(
        username=JIRA_USER,
        start_date="2025-05-01",
        end_date="2025-05-09"
    ))