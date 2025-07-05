#!/usr/bin/env python3

"""
Download all ClassDojo photos and videos in your timeline.
by kecebongsoft
How it works:
1. Fetch list of items in the timeline, if there are multiple pages,
   it will fetch for all pages.
2. Collect list of URLs for the attachment for each item
3. Download the files into local temporary directory, and also save
   the timeline activity as a json file.
How to use:
1. Modify the session cookie in this script, check your session cookie
   by opening classdojo in browser and copy the following cookies:
   dojo_log_session_id, dojo_login.sid, and dojo_home_login.sid
2. Run this script and wait for it to finish.
If error happens:
1. I ran this script in windows, make sure your path is correct if you
   are on linux
2. Make sure "classdojo_output" directory exists in the same folder as
   this script
3. Make sure you have a correct session cookies set in this script.
4. Make sure you can open the FEED_URL listed in this script from
   within your browser (assuming you can open ClassDojo website)
"""

import json
import os
import tempfile

import requests
from dotenv import load_dotenv

load_dotenv()

FEED_URL = "https://home.classdojo.com/api/storyFeed?includePrivate=true"

# make sure that classdojo_output dir exists, if not create it

DESTINATION = tempfile.mkdtemp(
    dir="classdojo_output"
)  # make sure this directory exists in the same place as this script.

SESSION_COOKIES = {
    "dojo_log_session_id": os.getenv("dojo_log_session_id"), #noqa SIM112
    "dojo_login.sid": os.getenv("dojo_login.sid"), #noqa SIM112
    "dojo_home_login.sid": os.getenv("dojo_home_login.sid"), #noqa SIM112
}

NOT_BEFORE = os.getenv("NOT_BEFORE", "0000-00-00")

def get_items(feed_url):
    print(f"Fetching items: {feed_url} ...")
    resp = requests.get(feed_url, cookies=SESSION_COOKIES)
    data = resp.json()
    prev = data.get("_links", {}).get("prev", {}).get("href")

    return data["_items"], prev


def get_contents(feed_url):
    items, prev = get_items(feed_url)

    while prev and feed_url != prev:
        prev_urls, prev = get_items(prev)
        items.extend(prev_urls)

    # Save the JSON data for later/inspection.
    with open(os.path.join(DESTINATION, "data.json"), "w") as fd:
        fd.write(json.dumps(items, indent=4))

    contents = []
    total = 0
    for item in items:
        data = item["contents"]
        group = item["headerSubtext"]
        # sanitize group name - replace spaces with underscores
        group = group.replace(" ", "_")
        entry = {
            "description": data.get("body"),
            "base_name": None,
            "day": None,
            "attachments": [],
            "group": group,
        }
        attachments = data.get("attachments", {})
        if not attachments:
            continue

        for attachment in attachments:
            parts = attachment["path"].split("/")
            day = parts[-3]
            if parts[3] == "api" or day < NOT_BEFORE:
                continue
            total += 1
            if not entry["base_name"]:
                entry["base_name"] = parts[-4]
                entry["day"] = day
            entry["attachments"].append(
                {"name": "_".join(parts[-2:]), "url": attachment["path"]}
            )

        if entry["base_name"]:
            contents.append(entry)

    return contents, total


def download_contents(contents, total):
    index = 0
    highest_day = contents[0]["day"]
    for entry in contents:
        description_name = "{}_{}_{}_description.txt".format(
            entry["day"], entry["group"], entry["base_name"]
        )
        with open(os.path.join(DESTINATION, description_name), "w") as fd:
            fd.write(entry["description"])
        for item in entry["attachments"]:
            index += 1
            day = entry["day"]
            if day > highest_day:
                highest_day = day
            url = item["url"]
            filename = os.path.join(
                DESTINATION,
                "{}_{}_{}_{}".format(
                    entry["day"], entry["group"], entry["base_name"], item["name"]
                ),
            )
            if os.path.exists(filename):
                continue
            print("Downloading {}/{} on {}: {}".format(index, total, day, item["name"]))
            with open(filename, "wb") as fd:
                resp = requests.get(url, cookies=SESSION_COOKIES)
                fd.write(resp.content)
    print(f"Last day of data download: {highest_day}")
    print("Done!")


if __name__ == "__main__":
    print("Starting")
    contents, total = get_contents(FEED_URL)
    download_contents(contents, total)
