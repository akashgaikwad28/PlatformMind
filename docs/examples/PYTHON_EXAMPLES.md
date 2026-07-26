---
Last Updated: 2026-07-26
Related Source Files: N/A
Applies To Version: 1.0.0
Maintainer: PlatformMind Team
Generated From: Repository Audit
---

# Python Examples

## Purpose
How to trigger PlatformMind programmatically.

## Basic Execution Script
```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/execute",
            json={
                "instruction": "Merge PR #42 if it passes CI",
                "context": {"repository": "owner/repo"}
            },
            timeout=30.0
        )
        data = response.json()
        print(f"Status: {data['data']['status']}")

if __name__ == "__main__":
    asyncio.run(main())
```
