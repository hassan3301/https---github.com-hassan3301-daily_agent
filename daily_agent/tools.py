# daily_agent/tools.py (or sub_agents/postgres/tools.py)

from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext

class GenerateReportTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="generate_report_tool",
            description="Generates narrative business reports (e.g., profit/loss summaries) using tabular data.",
        )

    def run(self, tool_context: ToolContext):
        try:
            data = tool_context.input  # Should be {"columns": [...], "rows": [...]}
            columns = data["columns"]
            rows = data["rows"]

            report_lines = ["📊 Business Report", "-" * 40]

            for row in rows:
                line = ", ".join(f"{col}: {val}" for col, val in zip(columns, row))
                report_lines.append(line)

            report_lines.append("-" * 40)
            return "\n".join(report_lines)

        except Exception as e:
            return f"Error generating report: {str(e)}"

