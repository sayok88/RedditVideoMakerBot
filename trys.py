import multiprocessing

import ffmpeg
from tqdm import tqdm

from video_creation.final_video import ProgressFfmpeg

if __name__ == '__main__':
    pbar = tqdm(total=100, desc="Progress: ", bar_format="{l_bar}{bar}", unit=" %")


    def on_update_example(progress) -> None:
        status = round(progress * 100, 2)
        old_percentage = pbar.n
        pbar.update(status - old_percentage)


    reddit_id = "1cbdhug"
    post_numbers = 18
    screenshot_width = int((1080 * 45) // 100)
    video = ffmpeg.input('assets/temp/1cbdhug/background_noaudio.mp4')
    audio = ffmpeg.input('assets/temp/1cbdhug/audio.mp3')
    audio_clips_durations = []
    current_length = 0
    number_of_clips = 13
    audio_clips_durations.append(
        float(ffmpeg.probe(f"assets/temp/{reddit_id}/mp3/title.mp3")["format"]["duration"])
    )
    for i in range(post_numbers):
        audio_clips_durations.append(float(
            ffmpeg.probe(f"assets/temp/{reddit_id}/mp3/postaudio-{i}.mp3")["format"]["duration"]
        ))

    for i in range(number_of_clips):
        audio_clips_durations.append(float(
            ffmpeg.probe(f"assets/temp/{reddit_id}/mp3/{i}.mp3")["format"]["duration"]
        ))
    over_lay = ffmpeg.input(f"assets/temp/{reddit_id}/png/title.png")["v"].filter(
        "scale", screenshot_width, -1
    )
    video = video.overlay(
        over_lay,
        enable=f"between(t,{0},{audio_clips_durations[0]})",
        x="(main_w-overlay_w)/2",
        y="(main_h-overlay_h)/2",
    )
    current_length += audio_clips_durations[0]
    for i in range(0, number_of_clips + post_numbers - 1):
        over_lay = ffmpeg.input(f"assets/temp/{reddit_id}/png/img{i}.png")["v"].filter(
            "scale", screenshot_width, -1
        )

        video = video.overlay(
            over_lay,
            enable=f"between(t,{current_length},{current_length + audio_clips_durations[i]})",
            x="(main_w-overlay_w)/2",
            y="(main_h-overlay_h)/2",
        )
        current_length += audio_clips_durations[i]
    with ProgressFfmpeg(311, on_update_example) as progress:
        ffmpeg.output(
            video,
            audio,
            'tryyyy.mp4',
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
