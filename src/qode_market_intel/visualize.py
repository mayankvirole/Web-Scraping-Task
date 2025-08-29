from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from loguru import logger
from .config import PLOTS_DIR

def _ensure_dirs():
    Path(PLOTS_DIR).mkdir(parents=True, exist_ok=True)

def plot_aggregate(aggregates_parquet: Path) -> Path:
    _ensure_dirs()
    df = pd.read_parquet(aggregates_parquet)
    if df.empty:
        logger.warning("Empty aggregates; skipping plot.")
        return Path(PLOTS_DIR) / "aggregate.png"

    # Downsample if very long (every k-th point)
    k = max(1, len(df) // 500)
    df = df.iloc[::k].copy()

    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["signal_mean"], label="Signal mean")
    plt.fill_between(df.index, df["ci_low"], df["ci_high"], alpha=0.2, label="95% CI")
    plt.xlabel("Time")
    plt.ylabel("Composite signal")
    plt.title("Composite Trading Signal (mean ± 95% CI)")
    plt.legend()
    out_path = Path(PLOTS_DIR) / "signal_aggregate.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=120)
    plt.close()
    logger.info(f"Saved plot: {out_path}")
    return out_path
