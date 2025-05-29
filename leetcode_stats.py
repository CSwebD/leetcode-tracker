import requests

USERNAME = "cris_tian_7"
API_URL = f"https://leetcode-stats-api.herokuapp.com/{USERNAME}"

response = requests.get(API_URL)
data = response.json()

if "status" in data and data["status"] == "error":
    raise ValueError(f"❌ User '{USERNAME}' not found.")

easy = data.get("easySolved", 0)
medium = data.get("mediumSolved", 0)
hard = data.get("hardSolved", 0)
total = data.get("totalSolved", 0)

with open("README.md", "w") as f:
    f.write(f"# LeetCode Progress Tracker for {USERNAME}\n\n")
    f.write(f"- Easy: {easy} problems solved\n")
    f.write(f"- Medium: {medium} problems solved\n")
    f.write(f"- Hard: {hard} problems solved\n")
    f.write(f"\n✅ Total Solved: {total} problems\n")
