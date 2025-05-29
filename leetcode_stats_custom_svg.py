import requests
import os

USERNAME = "cris_tian_7"
API_URL = f"https://leetcode-stats-api.herokuapp.com/{USERNAME}"
ASSET_PATH = "assets"
SVG_FILE = f"{ASSET_PATH}/leetcode-summary.svg"

# Create assets folder if it doesn't exist
os.makedirs(ASSET_PATH, exist_ok=True)

response = requests.get(API_URL)
data = response.json()

if "status" in data and data["status"] == "error":
    raise ValueError(f"❌ User '{USERNAME}' not found.")

# Stats
easy = data.get("easySolved", 0)
medium = data.get("mediumSolved", 0)
hard = data.get("hardSolved", 0)
total = data.get("totalSolved", 0)

# SVG content
svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="500" height="150">
  <style>
    .title {{ font: bold 18px sans-serif; fill: #2f80ed; }}
    .stat {{ font: 14px sans-serif; fill: #333; }}
    .box {{ rx: 10; ry: 10; fill: #f3f4f6; stroke: #ccc; stroke-width: 1; }}
  </style>
  <rect class="box" x="5" y="5" width="490" height="140" />
  <text x="20" y="35" class="title">LeetCode Stats for {USERNAME}</text>
  <text x="20" y="65" class="stat">✔️ Easy: {easy} problems</text>
  <text x="20" y="90" class="stat">🚀 Medium: {medium} problems</text>
  <text x="20" y="115" class="stat">🔥 Hard: {hard} problems</text>
  <text x="350" y="90" class="title">✅ Total: {total}</text>
</svg>
"""

# Write to SVG file
with open(SVG_FILE, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"✅ Generated SVG at: {SVG_FILE}")
