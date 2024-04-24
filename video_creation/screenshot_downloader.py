import json
import re
from pathlib import Path
from typing import Dict, Final

import translators
from rich.progress import track

from utils import settings
from utils.console import print_step, print_substep
from utils.imagenarator import imagemaker
from utils.playwright import clear_cookie_by_name
from utils.videos import save_data

__all__ = ["download_screenshots_of_reddit_posts"]


def get_screenshots_of_reddit_posts(reddit_object: dict, screenshot_num: int):
    """Downloads screenshots of reddit posts as seen on the web. Downloads to assets/temp/png

    Args:
        reddit_object (Dict): Reddit object received from reddit/subreddit.py
        screenshot_num (int): Number of screenshots to download
    """
    # settings values
    W: Final[int] = int(settings.config["settings"]["resolution_w"])
    H: Final[int] = int(settings.config["settings"]["resolution_h"])
    lang: Final[str] = settings.config["reddit"]["thread"]["post_lang"]
    storymode: Final[bool] = settings.config["settings"]["storymode"]

    print_step("Downloading screenshots of reddit posts...")
    reddit_id = re.sub(r"[^\w\s-]", "", reddit_object["thread_id"])
    # ! Make sure the reddit screenshots folder exists
    Path(f"assets/temp/{reddit_id}/png").mkdir(parents=True, exist_ok=True)

    # set the theme and disable non-essential cookies
    if settings.config["settings"]["theme"] == "dark":
        bgcolor = (33, 33, 36, 255)
        txtcolor = (240, 240, 240)
        transparent = False
    elif settings.config["settings"]["theme"] == "transparent":
        if storymode:
            # Transparent theme
            bgcolor = (0, 0, 0, 0)
            txtcolor = (255, 255, 255)
            transparent = True
        else:
            # Switch to dark theme
            bgcolor = (33, 33, 36, 255)
            txtcolor = (240, 240, 240)
            transparent = False
    else:
        bgcolor = (255, 255, 255, 255)
        txtcolor = (0, 0, 0)
        transparent = False
    if storymode and settings.config["settings"]["storymodemethod"] == 1:
        # for idx,item in enumerate(reddit_object["thread_post"]):
        print_substep("Generating images...")
        return imagemaker(
            theme=bgcolor,
            reddit_obj=reddit_object,
            txtclr=txtcolor,
            transparent=transparent,
        )

