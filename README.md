# Anthropic Takehome Plugin

A plugin for Claude Code for the purpose of demoing this feature for an enablement scenario. 

Prepared by David Lucas, May 2026

**Summary:**

This is a working demo of a Claude Code plugin that includes an MCP server, skills, and subagent prompts. After installing and running the command /intel-report Claude will spawn 4 parallel subagents that will search different aspects of a Github repo and generate an engineering intelligence report. By defualt, the plugin MCP is pointed at the publicly available repository anthropics/anthropic-sdk-python.

**Getting up and running:**

Prerequisites: [Claude Code](https://claude.ai/code) and [uv](https://docs.astral.sh/uv/getting-started/installation/)

1. Clone the repo
git clone https://github.com/taroburrito/anthropic_takehome_plugins.git
cd anthropic_takehome_plugins

2. Launch Claude Code from the project directory
claude 

That's it. The MCP server starts automatically.

**Run the report:**
Once Claude Code is open, type:

/intel-report

Watch four subagents fan out in parallel. The full report lands in about 30 seconds.

Change the target repo

Edit `.mcp.json` and update the `GITHUB_REPO` value:

"env": {
"GITHUB_REPO": "owner/repo"
}

Works with any public GitHub repo — no token required.

**What's happening under the hood**


| File | What it does |
|---|---|
| `mcp-server/server.py` | Python MCP server — wraps 4 GitHub API endpoints as Claude tools 
| `.mcp.json` | Registers the MCP server with Claude Code
| `.claude/settings.json` | Permissions (auto-approves MCP tools and sets default mode for seamless demo)
| `.claude/commands/intel-report.md` | The slash command that orchestrates the parallel subagents 
