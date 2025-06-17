
# daily_agent/sub_agents/postgres/agent.py

import os
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from daily_agent.sub_agents.postgres.tools import QueryPostgresTool
from daily_agent.sub_agents.postgres.prompts import return_instructions_postgres

def setup_postgres_agent(callback_context: CallbackContext):
    """Inject user-specific schema and context if needed."""
    if "database_settings" not in callback_context.state:
        callback_context.state["database_settings"] = {
            "schema": """
Table: users
- id (int, primary key)
- email (string)
- name (string)
- ai_session_id (string, optional)

Table: contacts
- id (int, primary key)
- user_id (int, foreign key to users.id)
- name (string)
- email (string)
- phone (string)
- company (string)
- notes (text)
- status (string, default 'lead')

Table: invoices
- id (int, primary key)
- user_id (int, foreign key to users.id)
- contact_id (int, foreign key to contacts.id)
- issue_date (date)
- due_date (date)
- total_amount (float)
- status (string, 'unpaid' or 'paid')
- notes (text)

Table: revenue
- id (int, primary key)
- invoice_id (int, foreign key to invoices.id)
- amount (float)
- date (date)

Table: expenses
- id (int, primary key)
- user_id (int, foreign key to users.id)
- amount (float)
- category (string)
- description (text)
- date (date)

Table: interactions
- id (int, primary key)
- user_id (int, foreign key to users.id)
- contact_id (int, foreign key to contacts.id)
- date (date)
- type (string)  // e.g., 'call', 'email'
- summary (text)

Table: events
- id (int, primary key)
- user_id (int, foreign key to users.id)
- contact_id (int, foreign key to contacts.id)
- title (string)
- date (datetime)
- description (text)
- location (string)
"""
        }

postgres_agent = Agent(
    name="postgres_agent",
    model=os.getenv("POSTGRES_AGENT_MODEL", "gemini-2.0-flash"),
    instruction=return_instructions_postgres(),
    tools=[QueryPostgresTool()],
    before_agent_callback=setup_postgres_agent,
    generate_content_config=types.GenerateContentConfig(temperature=0.01),
)
