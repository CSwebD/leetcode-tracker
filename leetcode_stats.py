import requests
import json

USERNAME = "cris_tian_7"  # Your actual LeetCode username

query = """
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
    username
    submitStats: submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
      }
    }
  }
}
"""

variables = {"username": USERNAME}
headers = {"Content-Type": "application/json"}

response = requests.post(
    "https://leetcode.com/graphql",
    json={"query": query, "variables": variables},
    headers=headers
)

data = response.json()

if not data["data"]["matchedUser"]:
    raise ValueError(f"User '{USERNAME}' not found on LeetCode.")

stats = data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]

with open("README.md", "w") as f:
    f.write(f"# LeetCode Progress Tracker for {USERNAME}\n\n")
    total = 0
    for item in stats:
        f.write(f"- {item['difficulty'].capitalize()}: {item['count']} problems solved\n")
        total += item['count']
    f.write(f"\n✅ Total Solved: {total} problems\n")
