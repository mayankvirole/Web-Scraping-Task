from datetime import timedelta

# Hashtags to target (without the '#')
HASHTAGS = ["nifty50", "sensex", "intraday", "banknifty"]

# Time window for collection
LOOKBACK_HOURS = 24

# Minimum target tweets
MIN_TWEETS = 2000

# Hard cap to avoid over-fetching on big days
MAX_TWEETS = 20000

# Output paths
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
PLOTS_DIR = "plots"

# Concurrency & rate limiting
MAX_WORKERS = 4
BASE_BACKOFF_SECS = 2
MAX_BACKOFF_SECS = 60

# Chunking: fetch per-hashtag in slices to spread load
SLICE_MINUTES = 120  # query in 2-hour windows

# Vectorization
MAX_FEATURES = 20000  # TF-IDF max features
MIN_DF = 2
NGRAM_RANGE = (1, 2)

# Aggregation
RESAMPLE_RULE = "30min"  # aggregate signals to 30-min bins
CONFIDENCE_Z = 1.96  # ~95% CI
