from pathlib import Path
from loguru import logger
import collector
import processor
import analysis
import visualize
from .config import MIN_TWEETS

def main():
    Path("logs").mkdir(exist_ok=True)
    if not Path("cookies.json").exists():
        logger.error("cookies.json not found! Please export Twitter cookies first.")
        return
    
    logger.add("logs/pipeline.log", rotation="5 MB", retention=10)
    raw = collector.collect_last_24h(min_tweets=MIN_TWEETS)
    cleaned = processor.clean_and_dedupe(raw)
    sig_path, agg_path = analysis.build_signals(cleaned)
    plot_path = visualize.plot_aggregate(agg_path)
    logger.success(
        f"Pipeline complete.\nRaw: {raw}\nCleaned: {cleaned}\nSignals: {sig_path}\nAggregates: {agg_path}\nPlot: {plot_path}"
    )

if __name__ == "__main__":
    main()
