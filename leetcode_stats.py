
import requests
import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

USERNAME = "cris_tian_7"
ASSET_PATH = "assets"

def fetch_submission_calendar():
    query = """
    query userSubmissionCalendar($username: String!) {
      userCalendar(userSlug: $username) {
        submissionCalendar
      }
    }
    """
    variables = {"username": USERNAME}
    response = requests.post("https://leetcode.com/graphql", json={"query": query, "variables": variables})
    data = response.json()
    calendar_str = data["data"]["userCalendar"]["submissionCalendar"]
    return json.loads(calendar_str)

def fetch_submission_stats():
    query = """
    query getUserStats($username: String!) {
      matchedUser(username: $username) {
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """
    variables = {"username": USERNAME}
    response = requests.post("https://leetcode.com/graphql", json={"query": query, "variables": variables})
    data = response.json()
    return data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]

def generate_heatmap(submissions):
    df = pd.DataFrame([
        {"date": datetime.datetime.utcfromtimestamp(int(ts)).strftime('%Y-%m-%d'), "count": cnt}
        for ts, cnt in submissions.items()
    ])
    if df.empty:
        print("⚠️ No submission data found for heatmap.")
        return
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    weekly = df["count"].resample("W").sum()

    plt.figure(figsize=(10, 1.5))
    sns.heatmap(weekly.values.reshape(1, -1), cmap="Greens", cbar=False)
    plt.axis("off")
    plt.title("LeetCode Weekly Submission Heatmap", fontsize=10)
    plt.tight_layout()
    os.makedirs(ASSET_PATH, exist_ok=True)
    plt.savefig(f"{ASSET_PATH}/leetcode-heatmap.svg", format="svg", bbox_inches="tight")
    plt.close()

def generate_bar_chart(stats):
    difficulties = [item["difficulty"] for item in stats]
    counts = [item["count"] for item in stats]

    plt.figure(figsize=(6, 3))
    bars = plt.bar(difficulties, counts, color=["green", "orange", "red"])
    plt.title("LeetCode Problems Solved (Easy, Medium, Hard)")
    plt.ylabel("Count")
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom', ha='center')
    plt.tight_layout()
    plt.savefig(f"{ASSET_PATH}/leetcode-submissions.svg", format="svg")
    plt.close()

if __name__ == "__main__":
    print("📥 Fetching submission calendar...")
    calendar = fetch_submission_calendar()
    print("📥 Fetching submission stats...")
    stats = fetch_submission_stats()
    print("📊 Generating heatmap...")
    generate_heatmap(calendar)
    print("📊 Generating bar chart...")
    generate_bar_chart(stats)
    print("✅ LeetCode stats updated.")
