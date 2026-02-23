# GitHub agent (GitHub Copilot MCP – issue & PR analysis)

This agent uses **GitHub’s remote MCP server** at `https://api.githubcopilot.com/mcp/` with **Streamable HTTP** so the ADK agent can analyze **issues** and **pull requests** (and repos) in a read-only way.

## Run with ADK web

```bash
# From adk_training directory
adk web --no-reload
```

Open http://localhost:8000 and select **github_agent**.

## Setup

1. **GitHub token**  
   Create a [GitHub Personal Access Token](https://github.com/settings/tokens) (classic or fine-grained). For private repos use a token with `repo` (or the needed scopes). For public-only, read-only is enough.

2. **`.env` in this folder** (or set `GITHUB_TOKEN` in the environment):

   ```bash
   GITHUB_TOKEN=ghp_xxxxxxxxxxxx
   GOOGLE_API_KEY=your_gemini_key
   ```

3. **ADK version**  
   The agent expects ADK to support **Streamable HTTP** for remote MCP (`StreamableHTTPServerParams` or `StreamableHTTPConnectionParams` in `mcp_session_manager`). If you get an import error, try:

   ```bash
   pip install -U google-adk
   ```

## What it does (issue / PR analysis)

- **Toolsets** are set to `issues`, `pull_requests`, and `repos` with `X-MCP-Readonly: true`.
- The agent can:
  - List and summarize issues
  - List and summarize pull requests
  - Answer questions about repo activity using MCP tools

To enable more tools (e.g. `code_security`, `actions`), change the `X-MCP-Toolsets` header in `agent.py` to a comma-separated list or `"all"` (and ensure your token has the right scopes).

## Connection snippet (for reference)

The agent is built from the same pattern you described:

```python
McpToolset(
    connection_params=StreamableHTTPServerParams(
        url="https://api.githubcopilot.com/mcp/",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-MCP-Toolsets": "all",   # or "issues,pull_requests,repos"
            "X-MCP-Readonly": "true"
        },
    ),
)
```

Yes — this MCP setup is exactly what you can use for **issue and PR analysis** with the GitHub Copilot MCP server.
# githubagent
