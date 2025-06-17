import os
from datetime import date

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from daily_agent.prompt import ROOT_AGENT_INSTRUCTION
from daily_agent.sub_agents.postgres.agent import postgres_agent
from daily_agent.sub_agents.postgres.tools import QueryPostgresTool
from daily_agent.tools import GenerateReportTool

# Optional: inject per-session setup (e.g. user ID, schema)
def setup_before_agent_call(callback_context: CallbackContext):
    if "user_id" not in callback_context.state:
        callback_context.state["user_id"] = "demo_user"

    if "database_settings" not in callback_context.state:
        # You can dynamically fetch schema or table structure if needed
        callback_context.state["database_settings"] = {
            "schema": """
            Table: contacts(id, name, email, company, phone)
            Table: invoices(id, contact_id, amount, status, date)
            Table: revenue(id, amount, category, date)
            Table: expenses(id, amount, category, date)
            """
        }

    # Append schema and user context to prompt
    schema = callback_context.state["database_settings"]["schema"]
    callback_context._invocation_context.agent.instruction = (
        ROOT_AGENT_INSTRUCTION
        + f"\n\nToday's date: {date.today()}"
        + f"\n\nHere is the database schema:\n{schema}"
    )

# Root agent that delegates to tools and a subagent
root_agent = Agent(
    name="daily_agent",
    model="gemini-2.0-flash",  # Replace with your preferred model
    description=(
        "A business assistant that chats with users to provide insights, "
        "generate business reports, and delegate data queries to a subagent."
    ),
    instruction=ROOT_AGENT_INSTRUCTION,
    sub_agents=[postgres_agent],
    tools=[
        QueryPostgresTool(),
        GenerateReportTool(),
    ],
    before_agent_callback=setup_before_agent_call,
    generate_content_config=types.GenerateContentConfig(temperature=0.3),
)