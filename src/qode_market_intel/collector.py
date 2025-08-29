import json
import math
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict, Any
from loguru import logger
from .config import HASHTAGS, LOOKBACK_HOURS, RAW_DIR, SLICE_MINUTES, BASE_BACKOFF_SECS, MAX_BACKOFF_SECS

def _build_query(hashtag: str, since: datetime, until: datetime) -> str:
    # Twitter/X advanced search via snscrape
    # Eg: since:2025-08-28 until:2025-08-29 (#nifty50) lang:en
    # Keep multiple languages; do not force lang filter.
    return f'#{hashtag} since:{since.date()} until:{until.date()}'
    
def _run_snscrape(query: str) -> List[Dict[str, Any]]:
    """Run snscrape and return list of tweet dicts (JSON from --jsonl)."""
    cmd = ["snscrape", "--jsonl", "twitter-search", query]
    logger.debug(f"Running: {' '.join(cmd)}")
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"snscrape failed: {out.stderr[:500]}")
    tweets = []
    for line in out.stdout.splitlines():
        try:
            tweets.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return tweets

def collect_last_24h(min_tweets: int = 2000) -> Path:
    Path(RAW_DIR).mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=LOOKBACK_HOURS)
    logger.info(f"Collecting tweets {LOOKBACK_HOURS}h window: {start.isoformat()} -> {now.isoformat()}")

    slice_td = timedelta(minutes=SLICE_MINUTES)
    slice_points = []
    t = start
    while t < now:
        u = min(t + slice_td, now)
        slice_points.append((t, u))
        t = u

    all_tweets: List[Dict[str, Any]] = []
    backoff = BASE_BACKOFF_SECS

    for tag in HASHTAGS:
        for s, u in slice_points:
            q = _build_query(tag, s, u)
            try:
                chunk = _run_snscrape(q)
                all_tweets.extend(chunk)
                logger.info(f"Fetched {len(chunk)} tweets for #{tag} in slice {s} -> {u}")
                backoff = BASE_BACKOFF_SECS  # reset backoff
            except Exception as e:
                logger.warning(f"Error fetching #{tag} slice {s}->{u}: {e}. Backing off {backoff}s")
                import time as _t
                _t.sleep(backoff)
                backoff = min(backoff * 2, MAX_BACKOFF_SECS)

    # Save raw as JSONL
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = Path(RAW_DIR) / f"tweets_{ts}.jsonl"
    with raw_path.open("w", encoding="utf-8") as f:
        for t in all_tweets:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")
    logger.success(f"Saved raw tweets: {raw_path} (count={len(all_tweets)})")
    return raw_path
