import os
import re
from pathlib import Path
from typing import Tuple

import numpy as np
import translators
from moviepy.audio.AudioClip import AudioClip
from moviepy.audio.fx.volumex import volumex
from moviepy.editor import AudioFileClip
from rich.progress import track

from reddit.morw import get_gender
from utils.console import print_step, print_substep
from utils.voice import sanitize_text
from vtt import merge_vtt_audio

DEFAULT_MAX_LENGTH: int = (
    300  # Video length variable, edit this on your own risk. It should work, but it's not supported
)


class TTSEngine:
    """Calls the given TTS engine to reduce code duplication and allow multiple TTS engines.

    Args:
        tts_module            : The TTS module. Your module should handle the TTS itself and saving to the given path under the run method.
        script_list         : The reddit object that contains the posts to read.
        path (Optional)       : The unix style path to save the mp3 files to. This must not have leading or trailing slashes.
        max_length (Optional) : The maximum length of the mp3 files in total.

    Notes:
        tts_module must take the arguments text and filepath.
    """

    def __init__(
            self,
            tts_module,
            script_list: list,
            path: str = "assets/temp/",
            max_length: int = DEFAULT_MAX_LENGTH,
            last_clip_length: int = 0,
    ):
        self.tts_module = tts_module()
        self.script_list = script_list
        print(self.script_list[1])
        self.redditid = re.sub(r"[^\w\s-]", "", script_list[0]["story_id"])
        self.path = path + self.redditid + "/mp3"
        self.max_length = max_length
        self.length = 0
        self.last_clip_length = last_clip_length

    def add_periods(
            self,
    ):  # adds periods to the end of paragraphs (where people often forget to put them) so tts doesn't blend sentences
        for comment in self.script_list:
            # remove links
            regex_urls = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
            if type(comment["text"]) == str:
                comment["text"] = [comment["text"]]
            comment["text"] = [re.sub(regex_urls, " ", c) for c in comment["text"]]
            comment["text"] = [c.replace("\n", ". ") for c in comment["text"]]
            comment["text"] = [re.sub(r"\bAI\b", "A.I", c) for c in comment["text"]]
            comment["text"] = [re.sub(r"\bAGI\b", "A.G.I", c) for c in comment["text"]]
            if comment["text"][-1] != ".":
                comment["text"] += "."
            comment["text"] = [c.replace(". . .", ".") for c in comment["text"]]
            comment["text"] = [c.replace(".. . ", ".") for c in comment["text"]]
            comment["text"] = [c.replace(". . ", ".") for c in comment["text"]]
            comment["text"] = [re.sub(r'\."\.', '".', c) for c in comment["text"]]
            comment["text"] = [c for c in comment["text"] if c != "." or len(c) > 1]

    def run(self) -> Tuple[int, int, list]:
        Path(self.path).mkdir(parents=True, exist_ok=True)
        print_step("Saving Text to MP3 files...")

        self.add_periods()
        # gender = self.script_list.get("voice_gender")
        self.call_tts("title", process_text(self.script_list[0]["text"][0]), voice=self.script_list[0]["voice"])
        post_idx = 0
        for idx, script in track(enumerate(self.script_list[1:]), "...doing"):
            for idy, text in enumerate(script["text"]):
                self.call_tts(f"postaudio-{idx}-{idy}", process_text(text), voice=script["voice"])
                post_idx += idy

        return self.length, post_idx, self.script_list

    def split_post(self, text: str, idx, gender=None):
        split_files = []
        split_text = [
            x.group().strip()
            for x in re.finditer(
                r" *(((.|\n){0," + str(self.tts_module.max_chars) + "})(\.|.$))", text
            )
        ]
        self.create_silence_mp3()

        idy = None
        for idy, text_cut in enumerate(split_text):
            newtext = process_text(text_cut)
            # print(f"{idx}-{idy}: {newtext}\n")

            if not newtext or newtext.isspace():
                print("newtext was blank because sanitized split text resulted in none")
                continue
            else:
                self.call_tts(f"{idx}-{idy}.part", newtext, gender=gender)

                split_files.append(str(f"{self.path}/{idx}-{idy}.part.mp3"))

                # os.system(
                #     "ffmpeg -f concat -y -hide_banner -loglevel panic -safe 0 "
                #     + "-i "
                #     + f"{self.path}/list.txt "
                #     + "-c copy "
                #     + f"{self.path}/{idx}.mp3"
                # )
        merge_vtt_audio(split_files, f"{self.path}/{idx}")
        try:
            for i in range(0, len(split_files)):
                os.unlink(split_files[i])
                try:
                    os.unlink(split_files[i].replace('mp3', 'vtt'))
                except:
                    pass
        except FileNotFoundError as e:
            print("File not found: " + e.filename)
        except OSError:
            print("OSError")

    def call_tts(self, filename: str, text: str, voice=None):
        self.tts_module.run(
            text,
            filepath=f"{self.path}/{filename}.mp3",
            voice=voice
        )
        # try:
        #     self.length += MP3(f"{self.path}/{filename}.mp3").info.length
        # except (MutagenError, HeaderNotFoundError):
        #     self.length += sox.file_info.duration(f"{self.path}/{filename}.mp3")
        try:
            clip = AudioFileClip(f"{self.path}/{filename}.mp3")
            self.last_clip_length = clip.duration
            self.length += clip.duration
            clip.close()
        except Exception as e:
            print("Text" + text + str(len(text)))
            print(e)
            # self.length = 0

    def create_silence_mp3(self):
        silence_duration = 0.3
        silence = AudioClip(
            make_frame=lambda t: np.sin(440 * 2 * np.pi * t),
            duration=silence_duration,
            fps=44100,
        )
        silence = volumex(silence, 0)
        silence.write_audiofile(f"{self.path}/silence.mp3", fps=44100, verbose=False, logger=None)


def process_text(text: str, clean: bool = True):
    new_text = sanitize_text(text) if clean else text
    # if lang:
    #     print_substep("Translating Text...")
    #     translated_text = translators.translate_text(text, translator="google")
    #     new_text = sanitize_text(translated_text)
    return new_text
