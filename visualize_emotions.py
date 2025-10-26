import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import argparse
import sys
import logEmotion

def parse_args():
    p = argparse.ArgumentParser(description="Dummy visualization of emotions over dates with optional date filter.")
    p.add_argument("--start", type=str, default=None, help="Start date (YYYY-MM-DD)")
    p.add_argument("--end", type=str, default=None, help="End date (YYYY-MM-DD)")
    p.add_argument("--days", type=int, default=20, help="Number of days for dummy data (default: 20)")
    return p.parse_args()

def loadStats(logger) -> pd.DataFrame:
    raw = logger.loadJSON()
    if not raw:
        return pd.DataFrame(columns=["date", "label", "score"])
    df = pd.DataFrame(raw)
    required = {"datetime", "emotion", "percentage"}
    missing = required - set(df.columns)
    if missing:
        print("missing fields in json")
        return pd.DataFrame(columns=["date", "label", "score"])

    df["date"] = pd.to_datetime(df["datetime"], errors="coerce").dt.normalize()
    df = df.rename(columns={"emotion": "label", "percentage": "score"})
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df = df.dropna(subset=["date", "label", "score"])
    df = df[["date", "label", "score"]]
    return df

def make_dataset(days: int = 20) -> pd.DataFrame:
    logger = logEmotion.LogEmotion("stats.json")
    rawData = logger.loadJSON()
    df = pd.DataFrame(rawData)
    validInput = {"datetime", "emotion", "percentage"}
    invalidInput = validInput - set(df.columns)
    if not invalidInput:
        df["date"] = pd.to_datetime(df["datetime"], errors="coerce", format="%Y-%m-%d").dt.normalize()
        df = df.rename(columns={"emotion": "label", "percentage": "score"})
        df["score"] = pd.to_numeric(df["score"], errors="coerce")
        df = df.dropna(subset=["date", "label", "score"])
        df = df[["date", "label", "score"]]
        return df
    else:
        print("error loading stats")

    #dummy set as fallback
def make_dummy(days: int = 20) -> pd.DataFrame:
    np.random.seed(42)
    dates = pd.date_range(datetime.today().date() - timedelta(days=days-1), periods=days, freq="D")

    emotions = ["happy", "sad", "neutral", "angry", "surprise"]
    data = []
    for d in dates:
        for e in emotions:
            count = np.random.poisson(lam=3)
            for _ in range(count):
                # simple intensity model: happy tends higher
                mu = 70 if e == "happy" else 50
                score = np.clip(np.random.normal(loc=mu, scale=15), 0, 100)
                data.append({"date": pd.to_datetime(d), "label": e, "score": float(score)})
    return pd.DataFrame(data)

def apply_date_filter(df: pd.DataFrame, start: str | None, end: str | None) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()  # date-only

    min_d = df["date"].min().date()
    max_d = df["date"].max().date()

    if start is None and end is None:
        print(f"[Info] No filter provided. Available range: {min_d} to {max_d}")
        return df

    # parse inputs
    try:
        start_d = pd.to_datetime(start).date() if start else min_d
        end_d = pd.to_datetime(end).date() if end else max_d
    except Exception:
        print("[Error] Failed to parse --start/--end. Use YYYY-MM-DD, e.g. --start 2025-10-01 --end 2025-10-20")
        sys.exit(2)

    if start_d > end_d:
        print(f"[Error] start({start_d}) is after end({end_d}).")
        sys.exit(2)

    mask = (df["date"] >= pd.to_datetime(start_d)) & (df["date"] <= pd.to_datetime(end_d))
    filtered = df.loc[mask]
    if filtered.empty:
        print(f"[Warn] No rows in selected interval {start_d} .. {end_d}. Available: {min_d} .. {max_d}")
    else:
        print(f"[Info] Using interval {start_d} .. {end_d} (available: {min_d} .. {max_d})")
    return filtered

def main():
    args = parse_args()

    # 1) retrieve data
    df = make_dataset()
    #df = make_dummy()
    if df.empty:
        print("[Error] Dummy generation failed.")
        sys.exit(1)

    # 2) Apply date filter
    df = apply_date_filter(df, args.start, args.end)
    if df.empty:
        sys.exit(0)

    # 3) Aggregations
    counts = df.groupby(["date", "label"]).size().unstack(fill_value=0)
    intensity = df.groupby(["date", "label"])["score"].mean().unstack()

    # 4) Visualizations
    # Plot 1: stacked area — frequency share
    ax = counts.div(counts.sum(axis=1), axis=0).plot.area(
        figsize=(10, 4), alpha=0.7, colormap="tab10"
    )
    ax.set_title("Emotion Share Over Time")
    ax.set_ylabel("Share of emotions")
    ax.set_xlabel("Date")
    plt.tight_layout()
    plt.show()

    # Plot 2: line chart — average intensity
    ax2 = intensity.plot(figsize=(10, 4), linewidth=2)
    ax2.set_title("Average Emotion Intensity Over Time")
    ax2.set_ylabel("Intensity (0–100)")
    ax2.set_xlabel("Date")
    plt.tight_layout()
    plt.show()

    # Plot 3: Pie chart: total emotion distribution
    total_counts = df["label"].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(
        total_counts,
        labels=total_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=plt.cm.tab10.colors
    )
    plt.title("Overall Emotion Distribution (Filtered Range)")
    plt.tight_layout()
    plt.show()


main()
