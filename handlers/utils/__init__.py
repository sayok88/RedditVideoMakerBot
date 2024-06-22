from pathlib import Path

import praw
import tomlkit
from flask import current_app
from prawcore import ResponseException

from utils.gui_utils import get_config


def get_reddit_config():
    if not hasattr(current_app, "config2"):
        print("reloaded config")
        config_load = tomlkit.loads(Path("config.toml").read_text())
        current_app.config2 = get_config(config_load)
    return current_app.config2


def get_reddit_obj():
    if not hasattr(current_app.config, "reddit_obj"):
        config = get_reddit_config()
        username = config["reddit"]["creds"]["username"]
        passkey = config["reddit"]["creds"]["password"]
        try:
            current_app.config["reddit_obj"] = praw.Reddit(
                client_id=config["reddit"]["creds"]["client_id"],
                client_secret=config["reddit"]["creds"]["client_secret"],
                user_agent="Accessing Reddit threads",
                username=username,
                passkey=passkey,
                check_for_async=False,
            )

        except ResponseException as e:
            if e.response.status_code == 401:
                print("Invalid credentials - please check them in config.toml")
        except:
            print("Something went wrong...")
    return current_app.config["reddit_obj"]


def get_sub_reddit():
    reddit = get_reddit_obj()
    config = get_reddit_config()
    sub = config["reddit"]["thread"]["subreddit"]
    if not current_app.config.get("subreddit", {}).get(sub):
        subreddit_choice = sub
        if str(subreddit_choice).casefold().startswith("r/"):  # removes the r/ from the input
            subreddit_choice = subreddit_choice[2:]
        subreddit = reddit.subreddit(subreddit_choice)
        conf1 = current_app.config.get("subreddit", {})
        conf1[sub] = subreddit
        current_app.config["subreddit"] = conf1
    return current_app.config["subreddit"][sub]

