import json
from twikit import Client
from gnews import GNews

# -----------------------------
# 1️⃣ Initialize Twikit client
# -----------------------------
client = Client('en-US')

# Load existing cookies if available
try:
    client.load_cookies('cookies.json')
except FileNotFoundError:
    print("No cookies found. You need to login manually first.")
    client.login('username', 'password', 'verification_code_if_needed')
    client.save_cookies('cookies.json')
    exit("Please login first to generate cookies.json.")

# -----------------------------
# 2️⃣ Get stock hashtag from user
# -----------------------------
ticker = input("Enter stock ticker (e.g., TSLA, AAPL, RELIANCE): ").upper()
hashtag = f"#{ticker}"

# -----------------------------
# 3️⃣ Fetch tweets
# -----------------------------
print(f"\nFetching latest tweets for {hashtag}...\n")
tweets = client.search_tweet(hashtag, product='Latest', count=20)

if not tweets:
    print("No tweets found.")
else:
    for i, tweet in enumerate(tweets, start=1):
        print(f"{i}. {tweet.user.name} (@{tweet.user.username}):")
        print(tweet.text)
        print("-" * 60)

# -----------------------------
# 4️⃣ Fetch news headlines
# -----------------------------
print(f"\nFetching latest news for {ticker}...\n")
google_news = GNews(language='en', country='US', period='7d', max_results=5)
news_items = google_news.get_news(f"{ticker} stock")

if not news_items:
    print("No news found.")
else:
    for i, news in enumerate(news_items, start=1):
        print(f"{i}. {news['title']}")
        print(news['url'])
        print("-" * 60)

print("\nDone.")
