from fastapi import FastAPI, Query
from weekle_report_assistace_crew.main import run
from weekle_report_assistace_crew.main import Params
from typing import Annotated

app = FastAPI()

@app.get("/")
async def root():
   return run(
        inputs=Params(
            start_date="2023-01-01",
            end_date="2023-12-31",
            username="Tolosa527",
        )
   ) 


@app.get("/create_report")
async def create_report(
    start_date: str,
    end_date: str,
    username: str
):
    """
    Endpoint to create a report.
    """
    # Here you would call the function to create the report
    # For example: report = create_weekly_report()
    return crew.kickoff(inputs={
        "start_date": start_date,
        "end_date": end_date,
        "username": username
    })