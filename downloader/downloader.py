#!/usr/bin/env python3

"""
- 1 time per day snapshot top 15 past 24h
- HN too
"""

import datetime
import json
import os
import shutil
import sys
from functools import reduce
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

import requests
from requests.auth import HTTPBasicAuth

USER_AGENT = "DailyBrief/0.1 by coursesuno"
REDDIT_COM = "https://reddit.com"
OUTPUT_FNAME = "reddit-posts.json"

subreddits = [
    "comics",
    "omaha",
    "omahatech",
    "spacexlounge",
    "spacex",
    "onebag",
    "ExperiencedDevs",
    "solotravel",
    "ultralight",
]

def main():
    download_reddit()
    download_nyt()

def get_nyt_url(date):
    return f"https://static01.nyt.com/images/{date.year}/{date.month:02}/{date.day:02}/nytfrontpage/scan.pdf"

def download_nyt():
    eprint("Fetching nyt front page")
    date = datetime.datetime.now(ZoneInfo("America/New_York"))
    url = get_nyt_url(date)

    r = requests.get(url, stream=True)
    if r.status_code == 200:
        write_nyt(r)
    else:
        yesterday = date - datetime.timedelta(days=1)
        new_url = get_nyt_url(yesterday)
        r2 = requests.get(new_url, stream=True)
        if r2.status_code == 200:
            write_nyt(r2)
        else:
            eprint("Failed to fetch nyt")

def write_nyt(r):
    fname = "nyt.pdf"
    path = os.path.join("..", "data", "img", fname)
    with open(path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

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
    url = f"https://www.reddit.com/r/{subreddit}/top/.json?count={count}&t=day&limit=10"
    r = get(url)
    return r.json()


def get_post(listing_post: dict):
    url = reduce(urljoin, [REDDIT_COM, listing_post["data"]["permalink"], ".json?limit=10000&depth=100"])
    r = get(url)
    return r.json()


def download_images(posts: list):
    for post in posts:
        post_data = post[0]['data']['children'][0]['data']
        url = post_data['url']
        thumb = post_data['thumbnail']

        if thumb in ['self', 'default']:
            continue

        if '.png' in url or '.jpg' in url or '.jpeg' in url:
            try:
                download_image(url)
            except Exception as e:
                eprint("Failed to download img", url)
                eprint(e)

        download_image(thumb)

def download_image(url: str):
    r = requests.get(url, stream=True)
    path = os.path.join("..", "data", "img", url.split("/")[-1])
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)



def download_reddit():
    out = {
        "time": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "subreddits": {},
    }

    for subreddit in subreddits:
        eprint(f"Fetching top posts from /r/{subreddit}")
        listing = get_listing(subreddit)
        posts = []
        for listing_post in listing["data"]["children"]:
            posts.append(get_post(listing_post))

        download_images(posts)

        out["subreddits"][subreddit] = posts

    output_path = os.path.join("..", "data", OUTPUT_FNAME)
    with open(output_path, "w+") as f:
        json.dump(out, f)


if __name__ == "__main__":
    main()
