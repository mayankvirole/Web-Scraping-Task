from loguru import logger
from pathlib import Path
from . import collector, processor, analysis, visualize
from .config import MIN_TWEETS

def main():
    logger.add("logs/pipeline.log", rotation="5 MB", retention="10 files")
    raw = collector.collect_last_24h(min_tweets=MIN_TWEETS)
    cleaned = processor.clean_and_dedupe(raw)
    sig_path, agg_path = analysis.build_signals(cleaned)
    plot_path = visualize.plot_aggregate(agg_path)
    logger.success(f"Pipeline complete.\nRaw: {raw}\nCleaned: {cleaned}\nSignals: {sig_path}\nAggregates: {agg_path}\nPlot: {plot_path}")

if __name__ == "__main__":
    main()
