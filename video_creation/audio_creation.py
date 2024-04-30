import re

from rich.progress import track

from utils import settings
from utils.console import print_step
from vtt import merge_vtt_audio


def create_audio(number_of_clips,post_numbers, reddit_obj):
    print_step("Joining audio  files 🎵")
    # Gather all audio clips
    audio_clips = list()
    reddit_id = re.sub(r"[^\w\s-]", "", reddit_obj["thread_id"])
    if number_of_clips == 0 and settings.config["settings"]["storymode"] == "false":
        print(
            "No audio clips to gather. Please use a different TTS or post."
        )  # This is to fix the TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'
        exit()
    if settings.config["settings"]["storymode"]:
        if settings.config["settings"]["storymodemethod"] == 0:
            audio_clips = [f"assets/temp/{reddit_id}/mp3/title.mp3"]
            audio_clips.insert(1, f"assets/temp/{reddit_id}/mp3/postaudio.mp3")
        elif settings.config["settings"]["storymodemethod"] == 1:
            audio_clips = [
                f"assets/temp/{reddit_id}/mp3/postaudio-{i}.mp3"
                for i in track(range(post_numbers), "Collecting the audio files...")
            ]
            if len(reddit_obj["comments"]) > 0:
                audio_clips = audio_clips + [f"silence0500.mp3"]
                audio_clips = audio_clips + [f"assets/temp/{reddit_id}/mp3/comments.mp3"]
                audio_clips = audio_clips + [f"silence0500.mp3"]
                audio_clips = audio_clips + [
                    f"assets/temp/{reddit_id}/mp3/{i}.mp3" for i in range(number_of_clips)
                ]
            audio_clips.insert(0, f"assets/temp/{reddit_id}/mp3/title.mp3")

    else:
        audio_clips = [
            f"assets/temp/{reddit_id}/mp3/{i}.mp3" for i in range(number_of_clips)
        ]
        audio_clips.insert(0, f"assets/temp/{reddit_id}/mp3/title.mp3")

    return merge_vtt_audio(audio_clips, f"assets/temp/{reddit_id}/audio")

