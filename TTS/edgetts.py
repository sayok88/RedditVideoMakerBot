import json
import random
from time import sleep

import edge_tts

from TTS.edgetts_submaker.submaker import SubMaker
from utils import settings
from utils.console import print_substep

locales = ['en-GB',
           'en-NZ',
           'en-US',
           'en-AU',
           'en-IE',
           'en-CA']


class edgetts:
    def __init__(self):
        self.max_chars = 5000
        self.voices = []
        self.m_voice = ""
        self.f_voice = ""
        with open("TTS/edgtts_voices.json", 'r') as f:
            voices = json.load(f)
            voices = [a for a in voices if a["Locale"] in locales]
            male = [a for a in voices if a["Gender"] == "Male"]
            female = [a for a in voices if a["Gender"] == "Female"]
            self.m_voice = random.choice(male)["ShortName"]
            self.f_voice = random.choice(female)["ShortName"]

        print_substep(f"Female Voice {self.f_voice}")
        print_substep(f"Male Voice {self.m_voice}")

    def run(
            self,
            text: str,
            filepath: str,
            random_voice=False,
            tries=0,
            max_tries=10,
            gender=None
    ):
        try:
            use_hard_sub = settings.config["settings"]["sub"]["use_hard_sub"]
            if use_hard_sub:
                sub_maker = SubMaker()
                sub_path = filepath.replace('.mp3', '.vtt')

            communicate = None
            if gender is not None and gender in ('M', 'F'):
                communicate = edge_tts.Communicate(text, voice=self.m_voice if gender == 'M' else self.f_voice)

            elif settings.config["settings"]["tts"]["edge_tts_voice"]:
                communicate = edge_tts.Communicate(text, voice=settings.config["settings"]["tts"]["edge_tts_voice"])

            else:
                communicate = edge_tts.Communicate(text)

            with open(filepath, "wb") as file:
                for chunk in communicate.stream_sync():
                    if chunk["type"] == "audio":
                        file.write(chunk["data"])

                    elif use_hard_sub and chunk["type"] == "WordBoundary":
                        sub_maker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

            if use_hard_sub and 'title' not in sub_path:
                with open(sub_path, "w", encoding="utf-8") as file:
                    file.write(sub_maker.generate_subs())

        except TimeoutError as e:
            print(e)
            if tries == max_tries:
                raise Exception("timed out")
            sleep(1)
            return self.run(text, filepath, tries=tries + 1, gender=gender, max_tries=max_tries)

        except Exception as e:
            print(text, filepath)
            raise e
