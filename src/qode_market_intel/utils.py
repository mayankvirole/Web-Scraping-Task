import re
import emoji
from typing import List, Tuple

URL_RE = re.compile(r"https?://\S+")
MENTION_RE = re.compile(r"@([A-Za-z0-9_]{1,15})")
HASHTAG_RE = re.compile(r"#(\w+)")

def strip_urls(text: str) -> str:
    return URL_RE.sub("", text)

def extract_mentions(text: str) -> List[str]:
    return list(set(MENTION_RE.findall(text)))

def extract_hashtags(text: str) -> List[str]:
    return list(set(HASHTAG_RE.findall(text)))

def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def demojize_text(text: str) -> str:
    return emoji.demojize(text, language="en")

def basic_clean(text: str) -> Tuple[str, List[str], List[str]]:
    if not isinstance(text, str):
        return "", [], []
    mentions = extract_mentions(text)
    hashtags = extract_hashtags(text)
    t = strip_urls(text)
    t = demojize_text(t)
    t = normalize_whitespace(t)
    return t, mentions, hashtags
