from pathlib import Path
from typing import Tuple
import numpy as np
import pandas as pd
from loguru import logger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from .config import (MAX_FEATURES, MIN_DF, NGRAM_RANGE, PROCESSED_DIR, RESAMPLE_RULE, CONFIDENCE_Z)

def _tfidf_vectors(texts: pd.Series) -> Tuple[TfidfVectorizer, np.ndarray]:
    vect = TfidfVectorizer(max_features=MAX_FEATURES, min_df=MIN_DF, ngram_range=NGRAM_RANGE)
    X = vect.fit_transform(texts.fillna(""))
    return vect, X

def _sentiment_scores(texts: pd.Series) -> pd.Series:
    sid = SentimentIntensityAnalyzer()
    # compound ∈ [-1, 1]
    return texts.fillna("").apply(lambda t: sid.polarity_scores(t)["compound"])

def build_signals(tweets_parquet: Path) -> Tuple[Path, Path]:
    df = pd.read_parquet(tweets_parquet)
    if df.empty:
        logger.warning("Empty tweets dataset; skipping analysis.")
        sig_out = Path(PROCESSED_DIR) / "signals.parquet"
        agg_out = Path(PROCESSED_DIR) / "aggregates.parquet"
        pd.DataFrame().to_parquet(sig_out)
        pd.DataFrame().to_parquet(agg_out)
        return sig_out, agg_out

    # TF-IDF (sparse matrix not saved by default to keep memory light)
    _, X = _tfidf_vectors(df["content"])

    # Sentiment
    df["sentiment"] = _sentiment_scores(df["content"])

    # Normalize engagement to [0,1]
    scaler = MinMaxScaler()
    df["engagement_norm"] = scaler.fit_transform(df[["engagement"]])

    # Composite signal: simple weighted sum (tuneable)
    # weight more on sentiment, some on engagement
    df["signal"] = 0.7 * df["sentiment"] + 0.3 * df["engagement_norm"]

    # Save per-tweet signals
    sig_out = Path(PROCESSED_DIR) / "signals.parquet"
    df.to_parquet(sig_out, index=False)
    logger.success(f"Saved per-tweet signals: {sig_out}")

    # Aggregate over time with confidence intervals
    ts = df.set_index(pd.to_datetime(df["date"], utc=True, errors="coerce")).sort_index()
    grouped = ts.resample(RESAMPLE_RULE).agg(
        signal_mean=("signal", "mean"),
        signal_std=("signal", "std"),
        n=("signal", "count"),
    )
    grouped["se"] = grouped["signal_std"] / np.sqrt(grouped["n"].clip(lower=1))
    grouped["ci_low"] = grouped["signal_mean"] - CONFIDENCE_Z * grouped["se"]
    grouped["ci_high"] = grouped["signal_mean"] + CONFIDENCE_Z * grouped["se"]
    agg_out = Path(PROCESSED_DIR) / "aggregates.parquet"
    grouped.to_parquet(agg_out)
    logger.success(f"Saved aggregated signals: {agg_out}")
    return sig_out, agg_out
