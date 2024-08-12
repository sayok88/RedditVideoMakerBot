import re

from rich.progress import track

from utils.console import print_step
from vtt import merge_vtt_audio


def create_audio(reddit_obj):
    print_step("Joining audio  files 🎵")
    # Gather all audio clips
    reddit_id = re.sub(r"[^\w\s-]", "", reddit_obj[0]["story_id"])
    audio_clips = [f"assets/temp/{reddit_id}/mp3/title.mp3"]
    audio_clips = audio_clips + [f"silence0500.mp3"]
    for idx, c in enumerate(reddit_obj[1:]):
        for idy, d in enumerate(c["text"]):
            audio_clips = audio_clips + [f"assets/temp/{reddit_id}/mp3/postaudio-{idx}-{idy}.mp3"]
        audio_clips = audio_clips + [f"silence0500.mp3"]

    return merge_vtt_audio(audio_clips, f"assets/temp/{reddit_id}/audio")
