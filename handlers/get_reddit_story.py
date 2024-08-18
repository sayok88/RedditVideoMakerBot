from flask import render_template, request, jsonify
from flask import Blueprint

from handlers.utils import get_story, get_post_comment, get_replies, get_static_story, get_stories, \
    create_vid_script_api, get_scripts_api, get_scripts_vid_api, get_video_backgrounds, get_audio_backgrounds, \
    get_voices, update_video_script, update_script_text, create_multi_thread_vid_script_api

bp = Blueprint('handlers', __name__)


@bp.route("/story", methods=["GET"])
def story():
    # print(get_reddit_config())
    return get_story(force_get_story=True)


@bp.route("/get_story/<string:story_id>", methods=["GET"])
def get_story_title(story_id):
    return get_story(story_id)


@bp.route("/get_static_story/<string:story_id>", methods=["GET"])
def get_story_title1(story_id):
    return get_static_story(story_id)


@bp.route("/get_story/<string:story_id>/comments", methods=["GET"])
def get_reddit_comments(story_id):
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 100, type=int)
    return get_post_comment(story_id, skip=skip, limit=limit)


@bp.route("/comment/<string:comment_id>/replies", methods=["GET"])
def get_replies1(comment_id):
    return get_replies(comment_id, skip=0, limit=100000)


@bp.route("/stories", methods=["GET"])
def get_stories_api():
    page = request.args.get('page', 0, type=int)
    return get_stories(page)


@bp.route("/create_vid_script", methods=["POST"])
def create_vid_script():
    data = request.get_json()
    id = create_vid_script_api(data.get("thread_id"), data.get("selected_comments"))
    print(data)
    response = jsonify({'vid_id': id})
    return response


@bp.route("/create_multi_thread_script", methods=["POST"])
def create_multi_thread_script():
    data = request.get_json()
    id = create_multi_thread_vid_script_api(data)
    print(data)
    response = jsonify({'vid_id': id})
    return response


@bp.route("/get_scripts", methods=["GET"])
def get_scripts():
    page = request.args.get('page', 0, type=int)
    return {'response': get_scripts_api(page)}


@bp.route("/get_scripts/<int:video_id>", methods=["GET"])
def get_scripts_vid(video_id):
    return {'response': get_scripts_vid_api(video_id)}


@bp.route("/video_config_all", methods=["GET"])
def video_config_all():
    return {'videos': get_video_backgrounds(), 'audios': get_audio_backgrounds(),
            'voices': get_voices(), 'video_orientations': {'v': 'Vertical', 'h': 'Horizontal', 'b': 'Both'}}


@bp.route("/update_script/<int:video_id>", methods=["PUT"])
def update_script(video_id):
    data = request.get_json()
    update_script_text(data['script_data'])
    update_video_script(data['video_data'])
    return {}
