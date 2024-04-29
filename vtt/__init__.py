import os
from typing import List

import ffmpeg
import webvtt
from webvtt import WebVTT, Caption


def merge_vtt_audio(mp3_file_list: List, o_file: str) -> int:
    """
    pass list of mp3_file_list ordered in way you want them merged,
    if function finds vtt file with same name e.g. foo.mp3 and foo.vtt,
    it will pick up the sub with proper offset to create merged vtt
    Args:
        mp3_file_list:
        o_file:

    Returns:
            duration
    """
    duration = 0.0
    vtt = WebVTT()
    for f in mp3_file_list:

        lead = f.split('.')[0]
        vtt_file = f'{lead}.vtt'

        if os.path.exists(vtt_file):
            for x in webvtt.read(vtt_file):
                if duration:
                    x.start = x._to_timestamp(x.start_in_seconds + duration)
                    x.end = x._to_timestamp(x.end_in_seconds + duration)
                vtt.captions.append(Caption(
                    x.start, x.end, x.lines
                ))
        duration += float(ffmpeg.probe(f)["format"]["duration"])
    audio_concat = ffmpeg.concat(*[ffmpeg.input(m) for m in mp3_file_list], a=1, v=0)
    e = ffmpeg.output(
        audio_concat, f"{o_file}.mp3", **{"b:a": "192k"}
    ).overwrite_output().run(quiet=True)
    vtt.save(f"{o_file}.vtt")
    return duration


def collect_files_test():
    """This is for test do not use this(put mp3 and vtt files to test, would result in random order of
    merge, create your function to collect audio and sub to use this)"""
    import glob
    return glob.glob("*.mp3")


if __name__ == '__main__':
    merge_vtt_audio(collect_files_test(), 'merged')
