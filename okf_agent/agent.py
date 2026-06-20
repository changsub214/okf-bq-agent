import os
import sys
import google.auth
from dotenv import load_dotenv
from functools import cached_property
from google.auth.transport.requests import Request
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from google.adk.agents import Agent
from google.adk.models import Gemini 
from google.genai import Client, types
from google.adk.integrations.bigquery import BigQueryCredentialsConfig, BigQueryToolset
from .prompts import return_prompt


# --- load environment
load_dotenv()

# --- Load Application Default Credentials
credentials, project_id = google.auth.default()

if not credentials.valid:
    credentials.refresh(Request())

# --- gemini connect
PROJECT__ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = os.getenv("GOOGLE_CLOUD_LOCATION")
class GlobalGemini(Gemini):
    @cached_property
    def api_client(self) -> Client:
        return Client(vertexai=True, project=PROJECT__ID, location=REGION)

# --- Initialize BigQuery Toolset
bigquery_tools = BigQueryToolset(
    credentials_config=BigQueryCredentialsConfig(credentials=credentials)
)

# --- Resolve OKF directory dynamically relative to this file
OKF_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "okf"))

# --- mcp
fs_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["--no-install", "@modelcontextprotocol/server-filesystem", OKF_DIR],
        ),
    ),
    tool_filter=["read_file", "list_directory"]
)

# --- gemini-3.5-flash
agent_gemini = Agent(
    # Use the latest stable Flash model identifier
    model=GlobalGemini(model=os.getenv("MODEL")),
    name="ecommerce_agent",
    instruction=return_prompt(OKF_DIR, PROJECT__ID), # Pass dynamic OKF_DIR and PROJECT__ID
    tools=[bigquery_tools, fs_toolset],
)

root_agent = agent_gemini

if __name__ == "__main__":
    print(f"Successfully called : {root_agent.name}")