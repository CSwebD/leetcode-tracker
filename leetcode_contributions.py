
import requests
import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
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
    response = requests.post(
        "https://leetcode.com/graphql",
        json={"query": query, "variables": {"username": USERNAME}},
        headers={"Content-Type": "application/json"}
    )

    try:
        response.raise_for_status()
        data = response.json()
        if "data" in data and data["data"]["userCalendar"]:
            calendar_str = data["data"]["userCalendar"]["submissionCalendar"]
            return json.loads(calendar_str)
        else:
            print("❌ Unexpected response format:")
            print(json.dumps(data, indent=2))
            raise Exception("Missing expected keys in response.")
    except Exception as e:
        print("🚨 Failed to fetch submission calendar.")
        print(f"Error: {str(e)}")
        raise


def generate_contribution_heatmap(submissions):
    df = pd.DataFrame([
        {
            "date": datetime.datetime.utcfromtimestamp(int(ts)).date(),
            "count": count
        }
        for ts, count in submissions.items()
    ])

    # Ensure all days are covered
    start_date = datetime.date.today() - datetime.timedelta(days=365)
    all_days = pd.date_range(start=start_date, end=datetime.date.today())
    df_all = pd.DataFrame({"date": all_days})
    df_all["count"] = 0
    df_all.set_index("date", inplace=True)

    for row in df.itertuples():
        df_all.at[row.date, "count"] = row.count

    df_all.reset_index(inplace=True)
    df_all["dow"] = df_all["date"].dt.weekday
    df_all["week"] = df_all["date"].apply(lambda d: d.isocalendar()[1])
    df_all["year"] = df_all["date"].dt.year

    # Pivot to create heatmap shape
    pivot = pd.pivot_table(df_all, values='count',
                           index=df_all["date"].dt.weekday,
                           columns=pd.to_datetime(df_all["date"]).dt.isocalendar().week,
                           fill_value=0)

    # Plot
    fig, ax = plt.subplots(figsize=(14, 2))
    cmap = plt.get_cmap("Greens")
    norm = mcolors.Normalize(vmin=0, vmax=max(df_all["count"].max(), 1))
    heatmap = ax.imshow(pivot, aspect='auto', cmap=cmap, norm=norm)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("LeetCode Submission Heatmap (Past Year)", fontsize=10, pad=10)
    plt.tight_layout()

    os.makedirs(ASSET_PATH, exist_ok=True)
    plt.savefig(f"{ASSET_PATH}/leetcode-contributions.svg", format="svg", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    submission_data = fetch_submission_calendar()
    generate_contribution_heatmap(submission_data)
