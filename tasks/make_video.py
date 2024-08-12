import datetime
import math
from time import sleep

from altlib.utils.imagenarator_v2 import create_title_png
from altlib.video_creation.audio_creation import create_audio
from altlib.video_creation.background import download_background_video, download_background_audio, chop_background, \
    get_background_config
from altlib.video_creation.final_video import make_final_video
from altlib.video_creation.voices import save_text_to_mp3
from models import VideoScript, VS_STATUSES, ScriptText
from utils.posttextparser import posttextparser


def create_video(app, db):
    while True:
        sleep(1)
        print("Waiting for new jobs")
        ready_jobs = db.session.query(VideoScript).filter(VideoScript.job_status == VS_STATUSES.ready)
        for job in ready_jobs:
            script = db.session.query(ScriptText).filter(ScriptText.video_id == job.id)
            data = [s.t_data() for s in script]
            for d in data[1:]:
                d["text"] = posttextparser(d["text"])
            print(data)
            length, file_numbers, data = save_text_to_mp3(data, "edgetts")

            print(data)
            create_title_png(data)
            bg_config = {
                "video": get_background_config("video", job.background_video),
                "audio": get_background_config("audio", job.background_music),
                "background_audio_volume": job.background_music_volume,
            }
            download_background_video(bg_config["video"])
            download_background_audio(bg_config["audio"])
            length = create_audio(data)
            chop_background(bg_config, length, data)
            length = math.ceil(length)
            make_final_video(length, data, bg_config)
            job.job_status = VS_STATUSES.completed
            db.session.add(job)
            db.session.commit()

        break