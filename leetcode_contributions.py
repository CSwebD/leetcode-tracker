import requests
import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

USERNAME = "cris_tian_7"
ASSET_PATH = "assets"
YEAR = datetime.datetime.now().year

def fetch_submission_calendar():
    query = """
    query userSubmissionCalendar($userSlug: String!, $year: Int!, $queryType: ProgressCalendarQueryTypeEnum!) {
      userProgressCalendarV2(userSlug: $userSlug, year: $year, queryType: $queryType) {
        submissions {
          date
          count
        }
      }
    }
    """
    variables = {
        "userSlug": USERNAME,
        "year": YEAR,
        "queryType": "SUBMISSION"
    }
    response = requests.post("https://leetcode.com/graphql", json={"query": query, "variables": variables})
    data = response.json()

    if "data" not in data or data["data"] is None or data["data"].get("userProgressCalendarV2") is None:
        print("❌ LeetCode API error or user not found.")
        print("Raw response:", json.dumps(data, indent=2))
        exit(1)

    submissions = data["data"]["userProgressCalendarV2"]["submissions"]
    return submissions

def generate_heatmap(submissions):
    df = pd.DataFrame([
        {"date": sub["date"], "count": sub["count"]}
        for sub in submissions
    ])
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    df = df.resample("D").sum().fillna(0)
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
