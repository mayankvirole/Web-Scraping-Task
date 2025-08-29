# Market Intelligence Pipeline (No Paid APIs)

Data collection & analysis system for real-time Indian market intelligence from Twitter/X **without paid APIs**.

## Features
- Collect tweets for hashtags: `#nifty50`, `#sensex`, `#intraday`, `#banknifty` (last 24h)
- No paid APIs: uses `snscrape` (public web scraping)
- Robust logging, retries & rate-limit backoff
- Clean & normalize text (Unicode-safe, Indian languages ready)
- Parquet storage + deduplication
- Text→Signal using TF‑IDF + VADER sentiment + engagement features
- Composite trading signal with confidence intervals
- Memory‑efficient plotting (downsampling)
- Designed to scale 10x via streaming & chunking

## Quickstart

```bash
# 1) Create & activate a virtual env (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps (includes snscrape)
pip install -r requirements.txt

# 3) (One-time) Download VADER lexicon
python -m nltk.downloader vader_lexicon

# 4) Run the end-to-end pipeline (collect -> process -> analyze -> visualize)
python -m qode_market_intel.run_pipeline
```

Outputs go to `data/`:
- `data/raw/tweets_*.jsonl` – raw scrape (JSON Lines)
- `data/processed/tweets.parquet` – cleaned + deduped dataset
- `data/processed/signals.parquet` – per-tweet features & signals
- `data/processed/aggregates.parquet` – aggregated signals with CIs
- `plots/` – lightweight PNGs

## Configuration
Edit `src/qode_market_intel/config.py` to change hashtags, windows, limits, etc.

## Notes / Caveats
- Scraping public sites can break if HTML changes; `snscrape` is widely used but not guaranteed.
- Respect terms of service, robots, and local laws. For internal evaluation only.
- If `snscrape` is rate-limited, the collector uses exponential backoff and chunked queries.

## Project Structure
```
market-intel-pipeline/
├─ src/qode_market_intel/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ utils.py
│  ├─ collector.py
│  ├─ processor.py
│  ├─ storage.py
│  ├─ analysis.py
│  ├─ visualize.py
│  └─ run_pipeline.py
├─ data/
├─ logs/
├─ plots/
├─ requirements.txt
└─ README.md
```
