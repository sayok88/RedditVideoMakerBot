import multiprocessing
import os
import re
import tempfile
import threading
import time
from os.path import exists  # Needs to be imported specifically
from typing import Final
from typing import Tuple, Dict

import ffmpeg
import translators
from PIL import Image
from rich.console import Console
from rich.progress import track

from utils.cleanup import cleanup
from utils.console import print_step, print_substep
from utils.thumbnail import create_thumbnail
from utils.videos import save_data
from vtt import merge_vtt_audio

console = Console()


class ProgressFfmpeg(threading.Thread):
    def __init__(self, vid_duration_seconds, progress_update_callback):
        threading.Thread.__init__(self, name="ProgressFfmpeg")
        self.stop_event = threading.Event()
        self.output_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
        self.vid_duration_seconds = vid_duration_seconds
        self.progress_update_callback = progress_update_callback

    def run(self):
        while not self.stop_event.is_set():
            latest_progress = self.get_latest_ms_progress()
            if latest_progress is not None:
                completed_percent = latest_progress / self.vid_duration_seconds
                self.progress_update_callback(completed_percent)
            time.sleep(1)

    def get_latest_ms_progress(self):
        lines = self.output_file.readlines()

        if lines:
            for line in lines:
                if "out_time_ms" in line:
                    out_time_ms_str = line.split("=")[1].strip()
                    if out_time_ms_str.isnumeric():
                        return float(out_time_ms_str) / 1000000.0
                    else:
                        # Handle the case when "N/A" is encountered
                        return None
        return None

    def stop(self):
        self.stop_event.set()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop()


def name_normalize(name: str) -> str:
    name = re.sub(r'[?\\"%*:|<>]', "", name)
    name = re.sub(r"( [w,W]\s?\/\s?[o,O,0])", r" without", name)
    name = re.sub(r"( [w,W]\s?\/)", r" with", name)
    name = re.sub(r"(\d+)\s?\/\s?(\d+)", r"\1 of \2", name)
    name = re.sub(r"(\w+)\s?\/\s?(\w+)", r"\1 or \2", name)
    name = re.sub(r"\/", r"", name)

    lang = "en"
    if lang:
        print_substep("Translating filename...")
        translated_name = translators.translate_text(name, translator="google", to_language=lang)
        return translated_name
    else:
        return name


def prepare_background(reddit_id: str, W: int, H: int, name: str = "") -> str:
    output_path = f"assets/temp/{reddit_id}/background_noaudio{name}.mp4"
    # return output_path
    output = (
        ffmpeg.input(f"assets/temp/{reddit_id}/background.mp4")
        .filter("crop", f"ih*({W}/{H})", "ih")
        .output(
            output_path,
            an=None,
            **{
                "c:v": "h264",
                "b:v": "20M",
                "b:a": "192k",
                "threads": multiprocessing.cpu_count(),
            },
        )
        .overwrite_output()
    )
    try:
        output.run(quiet=True)
    except ffmpeg.Error as e:
        print(e.stderr.decode("utf8"))
        exit(1)
    return output_path


def merge_background_audio(audio: ffmpeg, reddit_id: str, volume):
    """Gather an audio and merge with assets/backgrounds/background.mp3
    Args:
        audio (ffmpeg): The TTS final audio but without background.
        reddit_id (str): The ID of subreddit
    """
    background_audio_volume = volume
    if background_audio_volume == 0:
        return audio  # Return the original audio
    else:
        # sets volume to config
        bg_audio = ffmpeg.input(f"assets/temp/{reddit_id}/background.mp3").filter(
            "volume",
            background_audio_volume,
        )
        # Merges audio and background_audio
        merged_audio = ffmpeg.filter([audio, bg_audio], "amix", duration="longest")
        return merged_audio  # Return merged audio


def make_final_video(
        length: int,
        reddit_obj: list,
        background_config: Dict[str, Tuple],
):
    """Gathers audio clips, gathers all screenshots, stitches them together and saves the final video to assets/temp
    Args:
        number_of_clips (int): Index to end at when going through the screenshots'
        length (int): Length of the video
        reddit_obj (dict): The reddit object that contains the posts to read.
        background_config (Tuple[str, str, str, Any]): The background config to use.
    """
    # settings values
    # W: Final[int] = 1080
    # H: Final[int] = 1920
    use_hard_sub = True

    # opacity = settings.config["settings"]["opacity"]

    reddit_id = re.sub(r"[^\w\s-]", "", reddit_obj[0]["story_id"])

    allowOnlyTTSFolder: bool = (
            False
            and background_config["background_audio_volume"] != 0
    )

    print_step("Creating the final video 🎥")
    print_step("Creating background_clip 🎥")
    audio = ffmpeg.input(f"assets/temp/{reddit_id}/audio.mp3")
    final_audio = merge_background_audio(audio, reddit_id, volume=background_config["background_audio_volume"])
    for ori in background_config["video_orientations"]:
        print(ori)
        background_clip = ffmpeg.input(prepare_background(reddit_id, W=ori["width"], H=ori["height"], name=ori["name"]))

        console.log(f"[bold green] Video Will Be: {length} Seconds Long")

        screenshot_width = int((ori["width"] * 45) // 100)
        fsize = 20
        if ori["name"] == "landscape":
            fsize = 30
        style = f"FontName=Rubik SemiBold,FontSize={fsize},PrimaryColour={background_config['text_color']},OutlineColour={background_config['border_color']},BackColour=&H80000000,Bold=1,Italic=0,Alignment=10"
        background_clip = background_clip.filter('subtitles', f"assets/temp/{reddit_id}/audio.vtt", force_style=style)
        over_lay = ffmpeg.input(f"assets/temp/{reddit_id}/png/title.png")["v"].filter(
            "scale", screenshot_width, -1
        )
        title_dur = float(ffmpeg.probe(f"assets/temp/{reddit_id}/mp3/title.mp3")["format"]["duration"])
        background_clip = background_clip.overlay(
            over_lay,
            enable=f"between(t,0,{title_dur})",
            x="(main_w-overlay_w)/2",
            y="(main_h-overlay_h)/2",
        )
        title = re.sub(r"[^\w\s-]", "", reddit_obj[0]["text"][0])
        idx = re.sub(r"[^\w\s-]", "", reddit_obj[0]["story_id"])
        # title_thumb = reddit_obj["thread_title"]

        filename = f"{name_normalize(title)[:240]}{ori['name']}"
        subreddit = "FLASK"

        if not exists(f"./results/{subreddit}"):
            print_substep("The 'results' folder could not be found so it was automatically created.")
            os.makedirs(f"./results/{subreddit}")

        if not exists(f"./results/{subreddit}/OnlyTTS") and allowOnlyTTSFolder:
            print_substep("The 'OnlyTTS' folder could not be found so it was automatically created.")
            os.makedirs(f"./results/{subreddit}/OnlyTTS")

        # create a thumbnail for the video

        print_step("Rendering the video 🎥")
        from tqdm import tqdm

        pbar = tqdm(total=100, desc="Progress: ", bar_format="{l_bar}{bar}", unit=" %")

        def on_update_example(progress) -> None:
            status = round(progress * 100, 2)
            old_percentage = pbar.n
            pbar.update(status - old_percentage)

        defaultPath = f"results/{subreddit}"
        with ProgressFfmpeg(length, on_update_example) as progress:
            path = defaultPath + f"/{filename}"
            path = (
                    path[:251] + ".mp4"
            )  # Prevent a error by limiting the path length, do not change this.
            try:
                ffmpeg.output(
                    background_clip,
                    final_audio,
                    path,
                    f="mp4",
                    **{
                        "c:v": "h264",
                        "b:v": "20M",
                        "b:a": "192k",
                        "threads": multiprocessing.cpu_count(),
                    },
                ).overwrite_output().global_args("-progress", progress.output_file.name).run(
                    quiet=True,
                    overwrite_output=True,
                    capture_stdout=False,
                    capture_stderr=False,
                )
            except ffmpeg.Error as e:
                print(e.stderr.decode("utf8"))
                exit(1)
        old_percentage = pbar.n
        pbar.update(100 - old_percentage)
        if allowOnlyTTSFolder:
            path = defaultPath + f"/OnlyTTS/{filename}"
            path = (
                    path[:251] + ".mp4"
            )  # Prevent a error by limiting the path length, do not change this.
            print_step("Rendering the Only TTS Video 🎥")
            with ProgressFfmpeg(length, on_update_example) as progress:
                try:
                    ffmpeg.output(
                        background_clip,
                        audio,
                        path,
                        f="mp4",
                        **{
                            "c:v": "h264",
                            "b:v": "20M",
                            "b:a": "192k",
                            "threads": multiprocessing.cpu_count(),
                        },
                    ).overwrite_output().global_args("-progress", progress.output_file.name).run(
                        quiet=True,
                        overwrite_output=True,
                        capture_stdout=False,
                        capture_stderr=False,
                    )

                except ffmpeg.Error as e:
                    print(e.stderr.decode("utf8"))
                    exit(1)

            old_percentage = pbar.n
            pbar.update(100 - old_percentage)
        pbar.close()
        save_data(subreddit, filename + ".mp4", title, idx, background_config["video"][2])
    print_step("Removing temporary files 🗑")
    cleanups = cleanup(reddit_id)
    print_substep(f"Removed {cleanups} temporary files 🗑")
    print_step("Done! 🎉 The video is in the results folder 📁")
