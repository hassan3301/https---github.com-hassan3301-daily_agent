# local.py

import os
import sys

# Load .env BEFORE anything else
from dotenv import load_dotenv
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT_DIR, ".env"))

# Now continue with the rest
import vertexai
from vertexai.preview import reasoning_engines

from daily_agent.agent import root_agent
from daily_agent.utils.date_ranges import get_named_date_ranges

def main():
    # Load environment variables

    print("Loaded project ID:", os.getenv("GOOGLE_CLOUD_PROJECT"))
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")

    if not project_id:
        print("❌ Missing required environment variable: GOOGLE_CLOUD_PROJECT")
        sys.exit(1)
    if not location:
        print("❌ Missing required environment variable: GOOGLE_CLOUD_LOCATION")
        sys.exit(1)

    print(f"✅ Initializing Vertex AI with project={project_id}, location={location}")
    vertexai.init(project=project_id, location=location)

    # Build initial state
    today = os.getenv("TODAY", None)
    if today:
        from datetime import date
        today = date.fromisoformat(today)
    else:
        from datetime import date
        today = date.today()

    initial_state = {
        "user_id": "hnishat@hotmail.com",  # Use email as user_id for clarity
        "user_db_id": 1,  # So the agent or subagent tools can filter by this if needed
        "today": today.isoformat(),
        "date_ranges": get_named_date_ranges(today),
    }


    # Initialize ADK app
    app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )

    print("✅ Creating session...")
    session = app.create_session(
        user_id="test_user",
        session_id="test_session",
        state=initial_state,
    )
    print(f"🟢 Session created: {session.id}")

    # Send a realistic query
    test_message = "Can you show me my total revenue from last month?"

    print(f"\n📨 User: {test_message}\n🧠 Agent:")
    for event in app.stream_query(
        user_id="test_user",
        session_id=session.id,
        message=test_message,
    ):
        print(event)


if __name__ == "__main__":
    main()

