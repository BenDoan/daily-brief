#!/usr/bin/env python3

"""
- 1 time per day snapshot top 15 past 24h
- HN too
"""

import datetime
import json
import sys
from functools import reduce
from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

USER_AGENT = "DailyBrief/0.1 by coursesuno"
REDDIT_COM = "https://reddit.com"
OUTPUT_FNAME = "posts.json"

subreddits = [
    "all",
    "spacexlounge",
]

def login():
    basic = HTTPBasicAuth(APP_ID, SECRET)
    headers = {"User-Agent": "DailyBrief/0.1 by coursesuno"}
    r = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=basic,
        data=dict(
            grant_type="https://oauth.reddit.com/grants/installed_client",
            device_id="DO_NOT_TRACK_THIS_DEVICE",
        ),
        headers=headers,
    )
    if r.status_code == 200:
        return r.json()["access_token"]
    else:
        return None


def get(*args, **kwargs):
    headers = {"User-Agent": USER_AGENT}
    return requests.get(*args, headers=headers, **kwargs)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def print_ratelimits(h: dict):
    print(f"Used: {h['x-ratelimit-used']}")
    print(f"Remaining: {h['x-ratelimit-remaining']}")
    print(f"Reset: {h['x-ratelimit-reset']}")


def get_listing(subreddit: str, count: int = 10):
    url = f"https://www.reddit.com/r/{subreddit}/top/.json?count={count}&t=day"
    r = get(url)
    return r.json()


def get_post(listing_post: dict):
    url = reduce(urljoin, [REDDIT_COM, listing_post["data"]["permalink"], ".json"])
    r = get(url)
    return r.json()


def main():
    out = {
        "time": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "subreddits": {},
    }

    for subreddit in subreddits:
        eprint(f"Fetching top posts from /r/{subreddit}")
        listing = get_listing(subreddit)
        for listing_post in listing["data"]["children"]:
            post = get_post(listing_post)
            out["subreddits"][subreddit] = post

    with open(OUTPUT_FNAME, "w+") as f:
        json.dump(out, f)


if __name__ == "__main__":
    main()
