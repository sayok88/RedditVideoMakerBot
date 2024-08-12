from typing import Tuple

from rich.console import Console

from altlib.TTS.GTTS import GTTS
from altlib.TTS.TikTok import TikTok
from altlib.TTS.aws_polly import AWSPolly
from altlib.TTS.edgetts import edgetts
from altlib.TTS.elevenlabs import elevenlabs
from altlib.TTS.engine_wrapper import TTSEngine
from altlib.TTS.pyttsx import pyttsx
from altlib.TTS.streamlabs_polly import StreamlabsPolly
from utils import settings
from utils.console import print_table, print_step

console = Console()

TTSProviders = {
    "GoogleTranslate": GTTS,
    "AWSPolly": AWSPolly,
    "StreamlabsPolly": StreamlabsPolly,
    "TikTok": TikTok,
    "pyttsx": pyttsx,
    "ElevenLabs": elevenlabs,
    "edgetts": edgetts
}


def save_text_to_mp3(scripts, voice) -> Tuple[int, int, list]:
    """Saves text to MP3 files.

    Args:
        reddit_obj (): Reddit object received from reddit API in reddit/subreddit.py

    Returns:
        tuple[int,int]: (total length of the audio, the number of comments audio was generated for)
    """

    if str(voice).casefold() in map(lambda _: _.casefold(), TTSProviders):
        text_to_mp3 = TTSEngine(get_case_insensitive_key_value(TTSProviders, voice), scripts)
        return text_to_mp3.run()


def get_case_insensitive_key_value(input_dict, key):
    return next(
        (value for dict_key, value in input_dict.items() if dict_key.lower() == key.lower()),
        None,
    )
