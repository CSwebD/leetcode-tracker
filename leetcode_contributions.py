
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
         if "data" not in data or data["data"]["userCalendar"] is None:
         print("❌ LeetCode API error or user not found.")
         print("Raw response:", json.dumps(data, indent=2))
         exit(1)

    calendar_str = data["data"]["userCalendar"]["submissionCalendar"]

    return json.loads(calendar_str)

def generate_heatmap(submissions):
    df = pd.DataFrame([
        {"date": datetime.datetime.utcfromtimestamp(int(ts)).strftime('%Y-%m-%d'), "count": cnt}
        for ts, cnt in submissions.items()
    ])
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    weekly = df["count"].resample("W").sum()

    plt.figure(figsize=(10, 1.5))
    sns.heatmap(weekly.values.reshape(1, -1), cmap="Greens", cbar=False)
    plt.axis("off")
    plt.tight_layout()
    os.makedirs(ASSET_PATH, exist_ok=True)
    plt.savefig(f"{ASSET_PATH}/leetcode-contributions.svg", format="svg", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    calendar = fetch_submission_calendar()
    generate_heatmap(calendar)
