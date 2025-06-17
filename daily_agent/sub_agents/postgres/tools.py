from google.adk.tools import BaseTool, ToolContext
from pydantic import BaseModel, Field
from google.cloud import secretmanager
import logging
import os
import psycopg2

class QueryInput(BaseModel):
    query: str = Field(description="SQL query to run on the business database")

class QueryPostgresTool(BaseTool):
    name = "query_postgres_tool"
    description = "Runs SQL queries against the business database"
    args_schema = QueryInput

    def __init__(self):
        super().__init__(name=self.name, description=self.description)
        self.connection_string = self.get_secret("POSTGRES_URI")

    def get_secret(self, secret_name: str) -> str:
        from google.cloud import secretmanager
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    def run(self, context: ToolContext) -> str:
        query = context.input
        logging.info(f"[QueryPostgresTool] Received query: {query}")
        try:
            with psycopg2.connect(self.connection_string) as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    results = cur.fetchall()
                    logging.info(f"[QueryPostgresTool] Query results: {results}")
                    return str(results)
        except Exception as e:
            logging.error(f"[QueryPostgresTool] Error: {str(e)}")
            return f"Error executing query: {str(e)}"
