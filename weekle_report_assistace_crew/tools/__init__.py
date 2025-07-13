from .github_tool import GithubTool
from .jira_tool import JiraTool

# Create instances of the tools
github_tool = GithubTool()
jira_tool = JiraTool()

__all__ = ['github_tool', 'jira_tool']
