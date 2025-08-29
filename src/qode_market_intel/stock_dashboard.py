from twikit import Client

# Initialize client
client = Client('en-US')

# Load cookies (must exist from prior login & save)
client.load_cookies('cookies.json')

# -----------------------------
# Get stock ticker from user
# -----------------------------
ticker = input("Enter stock ticker (e.g., TSLA, AAPL, RELIANCE): ").upper()
hashtag = f"#{ticker}"

print(f"\nFetching latest tweets for {hashtag}...\n")

# -----------------------------
# Fetch latest tweets
# -----------------------------
tweets = client.search_tweet(hashtag, product='Latest', count=20)

if not tweets:
    print("No tweets found.")
else:
    for i, tweet in enumerate(tweets, start=1):
        print(f"{i}. {tweet.user.name} (@{tweet.user.username})")
        print(tweet.text)
        print("-" * 60)
