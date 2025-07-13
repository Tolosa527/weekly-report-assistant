#!/usr/bin/env python3
"""
Simple script to run the Weekly Report Assistant Crew
"""
import os
from weekle_report_assistace_crew.crew import WeekleReportAssistaceCrew
from weekle_report_assistace_crew.models import Params
from weekle_report_assistace_crew.config_loader import config

def main():
    print("🚀 Starting Weekly Report Assistant Crew...")
    print("📝 Configuration loaded from config.json")
    
    # Create parameters using config values
    params = Params(
        start_date='2025-07-07',
        end_date='2025-07-12',
        username=config['github_username']
    )
    
    print(f"📅 Period: {params.start_date} to {params.end_date}")
    print(f"👤 Username: {params.username}")
    
    try:
        # Run the crew
        crew = WeekleReportAssistaceCrew()
        result = crew.crew().kickoff(inputs=params.dict())
        
        print("\n✅ Crew execution completed successfully!")
        print("\n📊 Results:")
        print("="*50)
        print(result)
        
    except Exception as e:
        print(f"\n❌ Error during crew execution: {e}")

if __name__ == "__main__":
    main()
