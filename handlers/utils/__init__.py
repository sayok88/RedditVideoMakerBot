import json
from datetime import datetime
from os.path import exists
from pathlib import Path

import praw
import tomlkit
from flask import current_app
from praw.models import MoreComments
from prawcore import ResponseException
from sqlalchemy import desc

from models import Story, db, Comment, VideoScript, ScriptText, VS_STATUSES
from utils.ai_methods import sort_by_similarity
from utils.console import print_substep
from utils.gui_utils import get_config
from utils.subreddit import get_subreddit_undone
from utils.voice import sanitize_text


def d_list(olist):
    return [o.t_data() for o in olist]


def get_reddit_config():
    if not hasattr(current_app, "config2"):
        print("reloaded config")
        config_load = tomlkit.loads(Path("config.toml").read_text())
        current_app.config2 = get_config(config_load)
    return current_app.config2


def get_reddit_obj():
    if not hasattr(current_app.config, "reddit_obj"):
        config = get_reddit_config()
        username = config["username"]
        passkey = config["password"]
        try:
            current_app.config["reddit_obj"] = praw.Reddit(
                client_id=config["client_id"],
                client_secret=config["client_secret"],
                user_agent="Accessing Reddit threads",
                username=username,
                passkey=passkey,
                check_for_async=False,
            )

        except ResponseException as e:
            if e.response.status_code == 401:
                print("Invalid credentials - please check them in config.toml")
        except:
            print("Something went wrong...")
    return current_app.config["reddit_obj"]


def get_sub_reddit():
    reddit = get_reddit_obj()
    config = get_reddit_config()
    sub = config["subreddit"]
    if not current_app.config.get("subreddit", {}).get(sub):
        subreddit_choice = sub
        if str(subreddit_choice).casefold().startswith("r/"):  # removes the r/ from the input
            subreddit_choice = subreddit_choice[2:]
        subreddit = reddit.subreddit(subreddit_choice)
        conf1 = current_app.config.get("subreddit", {})
        conf1[sub] = subreddit
        current_app.config["subreddit"] = conf1
    return current_app.config["subreddit"][sub]


def already_done(done_videos: list, submission) -> bool:
    """Checks to see if the given submission is in the list of videos

    Args:
        done_videos (list): Finished videos
        submission (Any): The submission

    Returns:
        Boolean: Whether the video was found in the list
    """

    for video in done_videos:
        if video["id"] == str(submission):
            return True
    return False


def get_subreddit_undone(submissions: list, subreddit, times_checked=0, similarity_scores=None):
    """_summary_

    Args:
        submissions (list): List of posts that are going to potentially be generated into a video
        subreddit (praw.Reddit.SubredditHelper): Chosen subreddit

    Returns:
        Any: The submission that has not been done
    """
    # Second try of getting a valid Submission
    config = get_reddit_config()
    if times_checked and config["ai_similarity_enabled"]:
        print("Sorting based on similarity for a different date filter and thread limit..")
        submissions = sort_by_similarity(
            submissions, keywords=config["ai_similarity_enabled"]
        )

    # recursively checks if the top submission in the list was already done.
    if not exists("./video_creation/data/videos.json"):
        with open("./video_creation/data/videos.json", "w+") as f:
            json.dump([], f)
    with open("./video_creation/data/videos.json", "r", encoding="utf-8") as done_vids_raw:
        done_videos = json.load(done_vids_raw)
    if not exists("./video_creation/data/already_fetched.json"):
        with open("./video_creation/data/already_fetched.json", "w+") as f:
            json.dump([], f)
    with open("./video_creation/data/already_fetched.json", "r", encoding="utf-8") as already_fetched:
        already_fetched = json.load(already_fetched)
    for i, submission in enumerate(submissions):
        does_exists = Story.query.filter(Story.thread_id == submission.id).count() > 0
        if already_done(done_videos, submission) or str(submission) in already_fetched or does_exists:
            continue
        if submission.over_18:
            try:
                if not config["allow_nsfw"]:
                    print_substep("NSFW Post Detected. Skipping...")
                    continue
            except AttributeError:
                print_substep("NSFW settings not defined. Skipping NSFW post...")
        if submission.stickied:
            print_substep("This post was pinned by moderators. Skipping...")
            continue
        if (
                submission.num_comments <= int(config["min_comments"])
                and not config["storymode"]
        ):
            print_substep(
                f'This post has under the specified minimum of comments ({config["min_comments"]}). Skipping...'
            )
            continue
        if not submission.selftext:
            print_substep("You are trying to use story mode on post with no post text")
            continue

        if len(submission.selftext.split(' ')) < 200:
            continue

        if similarity_scores is not None:
            return submission, similarity_scores[i].item()
    print("all submissions have been done going by top submission order")
    VALID_TIME_FILTERS = [
        "day",
        "hour",
        "month",
        "week",
        "year",
        "all",
    ]  # set doesn't have __getitem__
    index = times_checked + 1
    if index == len(VALID_TIME_FILTERS):
        print("All submissions have been done.")

    return get_subreddit_undone(
        subreddit.top(
            time_filter=VALID_TIME_FILTERS[index],
            limit=(50 if int(index) == 0 else index + 1 * 50),
        ),
        subreddit,
        times_checked=index,
    )  # all the videos in hot have already been done


def get_story(post_id=None, force_get_story=False):
    if post_id and not force_get_story:
        story = Story.query.filter(Story.thread_id == post_id).one_or_none()
        if story:
            content = {"title": story.title, "body": story.body, "is_nsfw": story.is_nsfw,
                       "thread_url": story.permalink(), "thread_id": story.thread_id
                       }
            return content
    reddit = get_reddit_obj()
    config = get_reddit_config()
    subreddit = get_sub_reddit()
    if post_id:  # would only be called if there are multiple queued posts
        submission = reddit.submission(id=post_id)

    elif config["ai_similarity_enabled"]:  # ai sorting based on comparison
        threads = subreddit.hot(limit=50)
        keywords = config["ai_similarity_keywords"].split(",")
        keywords = [keyword.strip() for keyword in keywords]
        # Reformat the keywords for printing
        keywords_print = ", ".join(keywords)
        print(f"Sorting threads by similarity to the given keywords: {keywords_print}")
        threads, similarity_scores = sort_by_similarity(threads, keywords)
        submission, similarity_score = get_subreddit_undone(
            threads, subreddit, similarity_scores=similarity_scores
        )
    else:
        threads = subreddit.hot(limit=25)
        submission = get_subreddit_undone(threads, subreddit)
    content = {}
    threadurl = f"https://new.reddit.com/{submission.permalink}"
    content["title"] = submission.title
    content["thread_id"] = submission.id
    content["is_nsfw"] = submission.over_18
    content["body"] = submission.selftext
    story = Story(**content)
    db.session.add(story)
    db.session.commit()
    content["thread_url"] = threadurl
    content["comments"] = []
    return content


def get_post_comment(post_id, limit=100, skip=0):
    reddit = get_reddit_obj()
    submission = reddit.submission(id=post_id)
    return get_comments(submission.comments, limit, skip)


def get_replies(comment_id, limit=100, skip=0):
    reddit = get_reddit_obj()
    comments = reddit.comment(id=comment_id)
    comments.refresh()
    return get_comments(comments.replies, limit, skip, get_all_replies=True)


def get_static_story(post_id):
    if post_id:
        story = Story.query.filter(Story.thread_id == post_id).one_or_none()
        if story:
            content = {"title": story.title, "body": story.body, "is_nsfw": story.is_nsfw,
                       "thread_url": story.permalink(), "thread_id": story.thread_id,
                       "comments": get_static_comments(post_id)}
            return content


def get_static_comments(post_id, comment_id=None):
    all_comments = []
    if comment_id:
        comments = Comment.query.filter(Comment.story_id == post_id, Comment.parent_id == comment_id)
    else:
        comments = Comment.query.filter(Comment.story_id == post_id, Comment.parent_id == None)
    for comment in comments:
        comment_body = {"body": comment.body, "permalink": comment.permalink, "id": comment.id,
                        "upvotes": comment.upvotes,
                        "downvotes": comment.downvotes, "stickied": comment.stickied, "story_id": comment.story_id,
                        "is_by_op": comment.is_by_op, 'replies': get_static_comments(post_id, comment.id)}
        all_comments.append(comment_body)
    return all_comments


def get_comments(comment_forest, limit=100, skip=0, get_all_replies=False):
    comments = []
    index = 0
    comment_forest = comment_forest[skip:]

    try:
        for top_level_comment in comment_forest:
            if isinstance(top_level_comment, MoreComments):
                continue
            index += 1
            if index > limit:
                break
            if top_level_comment.body in ["[removed]", "[deleted]"]:
                continue  # # see https://github.com/JasonLovesDoggo/RedditVideoMakerBot/issues/78
            if not top_level_comment.stickied:
                sanitised = sanitize_text(top_level_comment.body)
                if not sanitised or sanitised == " ":
                    continue

            if (
                    top_level_comment.author is not None
                    and sanitize_text(top_level_comment.body) is not None
            ):  # if errors occur with this change to if not.
                comment = {
                    "body": top_level_comment.body,
                    "permalink": top_level_comment.permalink,
                    "id": top_level_comment.id,
                    "upvotes": top_level_comment.ups,
                    "downvotes": top_level_comment.downs,
                    "stickied": top_level_comment.stickied,
                    "story_id": top_level_comment.link_id,
                    "is_by_op": top_level_comment.is_submitter
                }
                if comment["story_id"].startswith("t3_"):
                    comment["story_id"] = comment["story_id"][3:]
                if top_level_comment.parent_id.startswith("t1_"):
                    comment["parent_id"] = top_level_comment.parent_id[3:]

                try:
                    story = Comment(**comment)
                    db.session.merge(story)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(e)
                    pass
                comment["replies"] = get_comments(top_level_comment.replies, 100000, 0, True) if get_all_replies else []
                comments.append(
                    comment
                )
    except Exception as e:
        print(e)
    return comments


def get_stories(page=1):
    per_page = 10
    Story.query.all()
    offset = (page - 1) * per_page
    stories = db.session.query(Story).order_by(desc(Story.created_at)).offset(offset).limit(per_page).all()
    return {'stories': d_list(stories)}


def create_vid_script_api(thread_id, data):
    vs = VideoScript()
    db.session.add(vs)
    db.session.commit()
    print(vs.id)
    story = Story.query.filter(Story.thread_id == thread_id).one_or_none()
    if story is None:
        return None
    # vss = VideoScriptStories(video_id=vs.id, story_id=story.thread_id)
    # db.session.add(vss)
    # db.session.commit()
    i = 0
    for st in data:
        std = ScriptText(video_id=vs.id, text=st.get("text"), index=i, datasource=st.get("datasource"),
                         story_id=thread_id)
        i += 1
        db.session.add(std)
        db.session.commit()
    return vs.id


def get_scripts_api(page=0):
    per_page = 4
    offset = (page - 1) * per_page
    vss = VideoScript.query.filter(VideoScript.job_status != VS_STATUSES.completed).order_by(
        desc(VideoScript.created_at)).offset(offset).limit(per_page)
    scripts = []
    for video_script_story in vss:
        temp = {}
        # story = Story.query.filter(Story.thread_id == video_script_story.story_id).one_or_none()
        # if story is None:
        #     continue
        # temp["story"] = story.t_data()
        st = ScriptText.query.filter(ScriptText.index == 0, ScriptText.video_id == video_script_story.id).one_or_none()
        if st is None:
            continue
        temp["script"] = st.text
        temp["video_id"] = st.video_id
        temp["story_id"] = st.story_id
        scripts.append(temp)
    return scripts


def get_scripts_vid_api(video_id):
    vs = VideoScript.query.filter(VideoScript.id == video_id).one_or_none()
    script_texts = ScriptText.query.filter(ScriptText.video_id == video_id).order_by(
        ScriptText.index)
    script = []
    for st in script_texts:
        script.append(st.t_data())
    return dict(script=script, video=vs.t_data())


def get_voices():
    with open('./TTS/edgtts_voices.json', 'r') as f:
        return [x for x in json.load(f) if "English (United States)" in x['FriendlyName']]


def get_video_backgrounds():
    with open('./utils/background_videos.json', 'r') as f:
        return json.load(f)


def get_audio_backgrounds():
    with open('./utils/background_audios.json', 'r') as f:
        return json.load(f)


def update_script_text(data):
    for row in data:
        vs = ScriptText.query.filter(ScriptText.id == row['id']).first()
        if vs is not None:
            vs.text = row.get('text')
            vs.voice = row.get('voice')
            vs.updated_at = datetime.utcnow()
            db.session.add(vs)
            db.session.commit()


def update_video_script(data):
    print(data)
    vs = VideoScript.query.filter(VideoScript.id == data['id']).first()
    if vs is not None:
        vs.job_status = data.get('job_status')
        vs.background_video = data.get('background_video')
        vs.background_music_volume = data.get('background_music_volume')
        vs.background_music = data.get('background_music')
        vs.updated_at = datetime.utcnow()
        db.session.add(vs)
        db.session.commit()
