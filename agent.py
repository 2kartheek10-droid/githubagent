"""
GitHub agent with MCP integration for issue and PR analysis.
Uses GitHub Copilot's remote MCP server (api.githubcopilot.com).

Run from repo root: adk web --no-reload
Then open http://localhost:8000 and select github_agent.

Requires: GITHUB_TOKEN in .env (GitHub PAT with repo scope for private repos).
"""
import os
from pathlib import Path

# Load .env if present (GITHUB_TOKEN, GOOGLE_API_KEY)
_env = Path(__file__).resolve().parent / ".env"
if _env.exists():
    for line in _env.read_text().strip().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
# GitHub MCP uses Streamable HTTP. ADK may expose StreamableHTTPServerParams or
# StreamableHTTPConnectionParams depending on version.
try:
    from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams as GitHubMCPParams
except ImportError:
    try:
        from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams as GitHubMCPParams
    except ImportError:
        GitHubMCPParams = None

if GitHubMCPParams is None:
    raise ImportError(
        "Your ADK version may not support Streamable HTTP for remote MCP. "
        "Try upgrading: pip install -U google-adk"
    )

# Retry config for Gemini
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# GitHub Copilot MCP – issue and PR analysis (read-only)
# Toolsets: issues, pull_requests, repos, etc. Use "all" for every toolset.
mcp_github = McpToolset(
    connection_params=GitHubMCPParams(
        url="https://api.githubcopilot.com/mcp/",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-MCP-Toolsets": "issues,pull_requests,repos",
            "X-MCP-Readonly": "true",
        },
    ),
)

# Root agent for adk web
root_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="github_agent",
    description="Analyzes GitHub issues and pull requests using the GitHub MCP.",
    instruction=(
        "Use the GitHub MCP tools to analyze issues and pull requests. "
        "Summarize PRs, list or describe issues, and answer questions about repo activity. "
        "You have read-only access to issues, pull_requests, and repos toolsets."
    ),
    tools=[mcp_github],
)
