import os
import random
import re
import textwrap
from copy import deepcopy
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from TTS.engine_wrapper import process_text
from utils.imagenarator import textsize

color = (37, 52, 89)


def change_col(img):
    img = img.convert("RGB")
    pixdata = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y] == (0, 0, 0):
                pixdata[x, y] = color
    return img


def create_lower_header(c_count, l_count, s_count, o_file=None):
    width = 20
    bgcolor = (255, 255, 255, 255)
    size = (1920, 1080)
    imgs = ['fonts/comment-solid.png', 'fonts/heart-solid.png', 'fonts/share-solid.png']
    counts = [c_count, l_count, s_count]
    image = Image.new("RGBA", size, bgcolor)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(os.path.join("fonts", "Roboto-Regular.ttf"), 100)

    for pair in zip(imgs, counts):
        count = pair[1]
        comment = Image.open(pair[0]).convert("RGBA")
        comment = comment.resize((100, 100))
        comment_mask = deepcopy(comment)
        comment = change_col(comment)
        image.paste(comment, (width, 10,), comment_mask)
        width += 100 + 20

        draw.text((width, 0), count, font=font,
                  fill=color)
        c_text_width = int(font.getlength(count))
        width += c_text_width + 20
    image = image.crop((0, 0, width, 120))
    if o_file:
        image.save(f"assets/{o_file}.png")
    return image


def draw_multiple_line_text_1(
        image, text, font, text_color, padding, wrap=40, transparent=False, header=None, sub_header=None,
        comment_box=None
) -> None:
    """
    Draw multiline text over given image
    """
    header_font = ImageFont.truetype(os.path.join("fonts", "Roboto-Regular.ttf"), 150)
    sub_header_font = ImageFont.truetype(os.path.join("fonts", "Apple Color Emoji.ttc"),
                                         96)  # 20, 32, 40, 48, 64, 96, 160
    draw = ImageDraw.Draw(image)
    Fontperm = textsize(text, font)  # font.getsize(text)
    image_width, image_height = image.size
    lines = textwrap.wrap(text, width=wrap)
    height = 20
    if header:
        draw.text((padding, height), header, font=header_font, fill=text_color)
        height += 150

    if sub_header:
        draw.text((padding, height), sub_header, font=sub_header_font, embedded_color=True)
        height += 120

    y = height
    for line in lines:
        line_width, line_height = textsize(line, font)  # font.getsize(line)
        draw.text((20, y), line, font=font, fill=text_color)
        y += line_height + padding
    height = y
    if comment_box:
        image.paste(comment_box, (20, height,))


def get_counts(reddit_obj):
    # add code for c_count, l_count, s_count from reddit_obj
    return [str(random.randrange(100, 998, 1)) for _ in range(0, 3)]


def create_title_png(reddit_obj):
    title = process_text(reddit_obj["thread_title"], False)
    text = title
    reddit_id = re.sub(r"[^\w\s-]", "", reddit_obj["thread_id"])
    Path(f"assets/temp/{reddit_id}/png").mkdir(parents=True, exist_ok=True)
    bgcolor = (255, 255, 255, 255)
    size = (1920, 1080)
    image = Image.new("RGBA", size, bgcolor)
    # text = process_text(text, False)
    header = "True Crazy Stories"
    header2 = "😊😇😎😱🤯"
    font = ImageFont.truetype(os.path.join("fonts", "Roboto-Regular.ttf"), 100)
    draw_multiple_line_text_1(image, text, font, "black", 20, header=header, sub_header=header2,
                              comment_box=create_lower_header(*get_counts(reddit_obj)))
    # create_lower_header("6", "1293", "90", "ijkl")
    image.save(f"assets/temp/{reddit_id}/png/title.png")


if __name__ == '__main__':
    text = "AITA for wanting to finish my beer before leaving the restaurant my wife and I were at?"
    bgcolor = (255, 255, 255, 255)
    size = (1920, 1080)
    image = Image.new("RGBA", size, bgcolor)
    # text = process_text(text, False)
    header = "True Crazy Stories"
    header2 = "😊😇😎😱🤯"
    font = ImageFont.truetype(os.path.join("fonts", "Roboto-Regular.ttf"), 100)
    draw_multiple_line_text_1(image, text, font, "black", 20, header=header, sub_header=header2,
                              comment_box=create_lower_header("6", "1293", "90", "ijkl"))
    # create_lower_header("6", "1293", "90", "ijkl")
    image.save("dsds.png")
