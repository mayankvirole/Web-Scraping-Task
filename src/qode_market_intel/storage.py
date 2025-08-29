from pathlib import Path
import pandas as pd
from loguru import logger

def read_parquet(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path)

def write_parquet(df: pd.DataFrame, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    logger.info(f"Wrote parquet: {path} (rows={len(df)})")
    return path
