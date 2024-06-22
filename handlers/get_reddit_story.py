from flask import render_template
from flask import Blueprint

from handlers.utils import get_reddit_config

bp = Blueprint('handlers', __name__)


@bp.route("/story", methods=["GET"])
def story():
    print(get_reddit_config())
    return render_template("templates/story.html", file="videos.json")

@bp.route("/get_story_title", methods=["GET"])
def get_story_title():
    pass