from datetime import datetime
from wsgiref.util import is_hop_by_hop

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()


class Story(db.Model):
    __tablename__ = 'stories'
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    thread_id = db.Column(db.Text, primary_key=True)
    modified = db.Column(db.Boolean, nullable=False, default=False)
    is_nsfw = db.Column(db.Boolean, nullable=False, default=False)
    update_story = db.Column(db.Text, db.ForeignKey('stories.thread_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def permalink(self):
        return f"https://new.reddit.com/{self.thread_id}"

    def t_data(self):
        return {
            'title': self.title,
            'body': self.body,
            'is_nsfw': self.is_nsfw,
            'update_story': self.update_story,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'thread_id': self.thread_id,
            'permalink': self.permalink(),
            'modified': self.modified,
        }


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Text, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.thread_id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    permalink = db.Column(db.Text, nullable=False)
    downvotes = db.Column(db.Integer, nullable=False, default=0)
    upvotes = db.Column(db.Integer, nullable=False, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    stickied = db.Column(db.Boolean, nullable=False, default=False)
    edited = db.Column(db.Boolean, nullable=False, default=False)
    is_by_op = db.Column(db.Boolean, nullable=True, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def t_data(self):
        return {
            'id': self.id,
            'body': self.body,
            'permalink': self.permalink,
            'stickied': self.stickied,
            'edited': self.edited,
            'is_by_op': self.is_by_op,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'parent_id': self.parent_id,
            'story_id': self.story_id,
            'downvotes': self.downvotes,
            'upvotes': self.upvotes,

        }


class VS_STATUSES:
    ready = "Ready"
    wip = "WIP"
    completed = "Completed"


class VideoScript(db.Model):
    __tablename__ = 'video_scripts'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    background_video = db.Column(db.Text, nullable=True)
    background_music = db.Column(db.Text, nullable=True)
    background_music_volume = db.Column(db.Float, nullable=True)
    job_status = db.Column(db.Text, nullable=True, default=VS_STATUSES.wip)
    back_ground_col = db.Column(db.Text, nullable=True, default="000000")
    border_col = db.Column(db.Text, nullable=True, default="0000ff")
    v_or_h_or_b = db.Column(db.Text, nullable=True, default="v")

    @property
    def text_color(self):
        return self.back_ground_col if self.back_ground_col is not None else '000000'

    def convert_to_ffmeg_color(self, color):
        color = color.replace('#', '')
        if len(color) == 6:
            r = color[0:2]
            g = color[2:4]
            b = color[4:6]
            return f"&H00{b}{g}{r}"
        return f"&H00000000"

    @property
    def text_border_color(self):
        return self.border_col if self.border_col is not None else '0000ff'

    def t_data(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'background_video': self.background_video,
            'background_music': self.background_music,
            'background_music_volume': self.background_music_volume,
            'job_status': self.job_status,
            'back_ground_col': '#' + self.text_color,
            'border_col': "#" + self.text_border_color,
            'v_or_h_or_b': self.v_or_h_or_b,
        }


# class VideoScriptStories(db.Model):
#     __tablename__ = 'video_scriptstories'
#     video_id = db.Column(db.Integer, db.ForeignKey('video_scripts.id'), primary_key=True)
#     story_id = db.Column(db.Text, db.ForeignKey('stories.thread_id'), primary_key=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
#     __table_args__ = (UniqueConstraint("video_id", "story_id", name="two_columns"),)


class ScriptText(db.Model):
    __tablename__ = 'script_text'
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Text, db.ForeignKey('stories.thread_id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video_scripts.id'))
    index = db.Column(db.Integer, nullable=False, default=0)
    text = db.Column(db.Text, nullable=False)
    voice = db.Column(db.Text, nullable=True)
    datasource = db.Column(db.Text, nullable=False)  # Urls for post/comments or filler data
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def t_data(self):
        return {
            'id': self.id,
            'story_id': self.story_id,
            'video_id': self.video_id,
            'index': self.index,
            'text': self.text,
            'voice': self.voice,
            'datasource': self.datasource,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
