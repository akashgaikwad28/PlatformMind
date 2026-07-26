---
Last Updated: 2026-07-26
Related Source Files: `src/platformmind/infrastructure/github/`
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Troubleshooting Authentication & Rate Limits

## Purpose
Resolve HTTP 401, 403, and 429 errors from external providers.

## GitHub Bad Credentials
```
github.GithubException.BadCredentialsException: 401
```
**Cause:** `GITHUB_TOKEN` is invalid, expired, or lacks correct scopes.
**Resolution:** Generate a new PAT with `repo` scopes.

## GitHub Rate Limit Exceeded
```
github.GithubException.RateLimitExceededException: 403
```
**Cause:** Exceeded 5,000 requests per hour (authenticated) or secondary rate limits triggered by burst traffic.
**Resolution:** Wait for the reset window. PlatformMind logs the exact reset time. If hitting secondary limits, slow down the `ExecutionOrchestrator` concurrency.

## Groq Authentication Error
```
groq.AuthenticationError
```
**Cause:** Invalid `GROQ_API_KEY`.
**Resolution:** Check the `.env` file.
