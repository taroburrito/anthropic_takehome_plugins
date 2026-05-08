Generate a GitHub intelligence report for anthropics/anthropic-sdk-python.

Investigate the following three dimensions IN PARALLEL by spawning a separate subagent for each:

**Subagent 1 — Commit Velocity & Health**
Use get_repo_overview and get_recent_commits. Analyze: how active is development, what areas of the codebase are changing most, are there any patterns in commit cadence?

**Subagent 2 — Issue Landscape**
Use get_open_issues. Analyze: how many open issues, what labels dominate, which issues have the most engagement, are there recurring themes?

**Subagent 3 — PR Bottlenecks**
Use get_open_pull_requests. Analyze: how many open PRs, which have been waiting longest, are there PRs with no reviewers assigned, what does the review load look like? Include a ranked list of the top 10 PR submitters by number of open PRs.

Once all three subagents return, synthesize their findings into a concise engineering intelligence report with:
- A one-paragraph executive summary
- Key findings from each dimension
- Top 2-3 recommended actions for the engineering team
