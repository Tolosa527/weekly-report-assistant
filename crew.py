from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from weekle_report_assistace_crew.tools import jira_tool, github_tool
from crewai_tools import DirectoryReadTool, FileReadTool
from weekle_report_assistace_crew.models import Params
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

docs_tools = DirectoryReadTool(directory="./reports")
file_tool = FileReadTool()


@CrewBase
class WeekleReportAssistaceCrew():
    """WeekleReportAssistaceCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools    
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True
        )

    @agent
    def reporting_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_creator'], # type: ignore[index]
            verbose=True,
            tools=[jira_tool, github_tool]
        )
    
    @agent
    def reporting_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_reviewer'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
            tools=[jira_tool, github_tool],
        )

    @task
    def reporting_task_creation(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task_creation'], # type: ignore[index]
            tools=[docs_tools, file_tool],
            output_file='reprt.md'
        )
    
    @task
    def reporting_task_review(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task_review'], # type: ignore[index]
            tools=[docs_tools, file_tool],
            input_file='report.md',
            expected_output='report.md',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the WeekleReportAssistaceCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
