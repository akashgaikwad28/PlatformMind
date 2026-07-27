---
Last Updated: 2026-07-26
Related Source Files: "`src/platformmind/infrastructure/github/`"
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# GitHub Integration

## Purpose
Details how PlatformMind talks to GitHub.

## Responsibilities
Managing authentication, rate limits, and wrapping the GitHub REST API.

## Location in Codebase
- `src/platformmind/infrastructure/github/`

## Related Modules
- [Infrastructure Layer](../infrastructure/README.md)
- [Adding a GitHub Tool](../development/ADDING_GITHUB_TOOL.md)

## Dependencies
`PyGithub`, `httpx`.

## Internal Workflow
The `GitHubClient` implements `PlatformClient`. It handles token injection and retry-after headers. Tools (e.g. `CreateIssueTool`) inherit from `BaseTool` and use the `GitHubClient` to make specific requests.

## Input
Tool specific inputs (e.g. repo name, title, body).

## Output
`ToolResult`.

## Error Handling
HTTP errors are caught and transformed into `ToolResult(success=False, error=...)`.

## Performance Notes
API calls are I/O bound.

## Extension Points
Add new tools by inheriting from `BaseTool`.

## Current Limitations
- No GraphQL API support.

## Future Improvements
- Add GraphQL support for more efficient data fetching.
