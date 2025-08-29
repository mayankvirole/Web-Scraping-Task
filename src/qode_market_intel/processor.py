import json
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
from loguru import logger
from .config import PROCESSED_DIR
from .utils import basic_clean

def _flatten(tweet: Dict[str, Any]) -> Dict[str, Any]:
    # flatten essential fields from snscrape tweet JSON
    user = tweet.get("user") or {}
    out = {
        "id": tweet.get("id"),
        "date": tweet.get("date"),
        "content_raw": tweet.get("content"),
        "username": user.get("username"),
        "displayname": user.get("displayname"),
        "likeCount": tweet.get("likeCount", 0),
        "retweetCount": tweet.get("retweetCount", 0),
        "replyCount": tweet.get("replyCount", 0),
        "quoteCount": tweet.get("quoteCount", 0),
        "lang": tweet.get("lang"),
        "url": tweet.get("url"),
    }
    return out

def clean_and_dedupe(raw_jsonl: Path) -> Path:
    Path(PROCESSED_DIR).mkdir(parents=True, exist_ok=True)
    records: List[Dict[str, Any]] = []
    with open(raw_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            try:
                t = json.loads(line)
                records.append(_flatten(t))
            except Exception:
                continue
    df = pd.DataFrame.from_records(records)
    if df.empty:
        logger.warning("No records parsed from raw. Exiting early.")
        out = Path(PROCESSED_DIR) / "tweets.parquet"
        df.to_parquet(out, index=False)
        return out

    # Clean text
    cleaned = df["content_raw"].apply(lambda x: basic_clean(x))
    df["content"], df["mentions"], df["hashtags"] = zip(*cleaned)

    # Engagement
    df["engagement"] = df[["likeCount", "retweetCount", "replyCount", "quoteCount"]].sum(axis=1)

    # Deduplicate by tweet id; keep max engagement if duplicates
    df.sort_values(["id", "engagement"], ascending=[True, False], inplace=True)
    df = df.drop_duplicates(subset=["id"], keep="first")

    # Ensure datetime
    df["date"] = pd.to_datetime(df["date"], utc=True, errors="coerce")

    out = Path(PROCESSED_DIR) / "tweets.parquet"
    df.to_parquet(out, index=False)
    logger.success(f"Saved cleaned & deduped tweets: {out} (count={len(df)})")
    return out
