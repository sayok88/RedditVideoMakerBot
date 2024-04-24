import json
import random

import edge_tts
from utils import settings
from utils.console import print_substep


class edgetts:
    def __init__(self):
        self.max_chars = 5000
        self.voices = []
        self.m_voice = ""
        self.f_voice = ""
        with open("TTS/edgtts_voices.json", 'r') as f:
            voices = json.load(f)
            male = [a for a in voices if "en-" in a["Locale"] and a["Gender"] == "Male"]
            female = [a for a in voices if "en-" in a["Locale"] and a["Gender"] == "Female"]
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
            if gender is not None and gender in ('M', 'F'):
                edge_tts.Communicate(text, voice=self.m_voice if gender == 'M' else self.f_voice).save_sync(
                    filepath)
            elif settings.config["settings"]["tts"]["edge_tts_voice"]:
                edge_tts.Communicate(text, voice=settings.config["settings"]["tts"]["edge_tts_voice"]).save_sync(
                    filepath)
            else:
                edge_tts.Communicate(text).save_sync(filepath)
        except TimeoutError as e:
            if tries == max_tries:
                raise e
            return self.run(text, filepath, tries=tries + 1, gender=gender)

        except BaseException as e:
            print(text, filepath)
            raise e
