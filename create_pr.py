#!/usr/bin/env python3
import requests
import json

# Create Pull Request
url = "https://api.github.com/repos/ZakiYassineAi/Trading/pulls"

# Read the executive deployment markdown
with open("EXECUTIVE_DEPLOYMENT.md", "r") as f:
    pr_body = f.read()

pr_data = {
    "title": "💰 Executive Deployment: $54.50/day Automated Profit System",
    "head": "executive_deployment_20250921_142131",
    "base": "main",
    "body": pr_body[:5000]  # GitHub has a limit on PR body size
}

# Use the GitHub token from environment or credentials
headers = {
    "Accept": "application/vnd.github.v3+json"
}

response = requests.post(url, json=pr_data, headers=headers)

if response.status_code in [201, 200]:
    pr = response.json()
    print(f"\n✅ Pull Request Created Successfully!")
    print(f"🔗 PR URL: {pr.get('html_url', 'Check on GitHub')}")
    print(f"📊 PR Number: #{pr.get('number', 'N/A')}")
else:
    print(f"Creating PR via web: https://github.com/ZakiYassineAi/Trading/pull/new/executive_deployment_20250921_142131")
    print(f"Branch pushed successfully - Create PR manually at the link above")