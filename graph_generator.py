from PIL import Image, ImageDraw, ImageFont
import json
import sys
import math

# COLORS = [
#     (255, 0, 0),    # 0
#     (255, 0, 0),    # 1
#     (255, 0, 0),    # 2
#     (255, 0, 0),    # 3
#     (255, 69, 0),   # 4
#     (255, 34, 0),  # 5
#     (255, 106, 0),  # 6
#     (255, 221, 0),  # 7
#     (212, 255, 0),  # 8
#     (100, 255, 0),  # 9
#     (0, 255, 0)    # 10
# ]

# COLORS = [
#     (255, 0, 0),   # 0: Red
#     (220, 20, 60), # 1: Crimson
#     (255, 69, 0),  # 2: Red-Orange
#     (255, 140, 0), # 3: Dark Orange
#     (255, 165, 0), # 4: Orange
#     (255, 188, 0), # 5: Yellow-Orange
#     (255, 215, 0), # 6: Orange-Yellow
#     (255, 255, 0), # 7: Yellow
#     (0, 128, 0),   # 8: Green
#     (0, 255, 255), # 9: Cyan
#     (0, 0, 255)    # 10: Blue
# ]

COLORS = [
    (220, 220, 255),  # 0 Pale Blue
    (186, 186, 255),  # 1 Pale Purple
    (152, 152, 255),  # 2 Pale Lavender
    (118, 118, 255),  # 3 Pale Violet
    (84, 84, 255),    # 4 Pale Indigo
    (50, 50, 255),    # 5 Pale Blue
    (30, 30, 255),    # 6 Bright Blue
    (0, 192, 255),    # 7 Bright Cyan
    (0, 255, 192),    # 8 Bright Teal
    (0, 255, 128),    # 9 Bright Green
    (0, 255, 128)     # 10 Bright Green
]


font_ttf_path = "/System/Library/Fonts/Monaco.ttf"

size_factor = 1
block_w = 64 * size_factor


def lerp(a, b, t):
    return a * (1 - t) + b * t


def load_series(series_id):
    f = open(series_id + ".json", "r")
    return json.loads(f.read())


def get_color(rating):
    flr = math.floor(rating)
    c_a = COLORS[flr]
    c_b = COLORS[flr + 1]
    t = rating - flr

    r = int(lerp(c_a[0], c_b[0], t))
    g = int(lerp(c_a[1], c_b[1], t))
    # return (r, g, 0)
    return (c_a[0], c_a[1], c_a[2])


if __name__ == "__main__":
    series_id = sys.argv[1]
    data = load_series(series_id)

    num_seasons = 0
    max_episodes = 0
    for seasondata in data["data"]:
        num_episodes = len(seasondata)
        if num_episodes > 0:
            num_seasons += 1
            max_episodes = max(max_episodes, num_episodes)

    ep_width = len(data["data"])
    ep_height = 0
    for it in data["data"]:
        if len(it) > ep_height:
            ep_height = len(it)

    # give it room for the first row of season number
    ep_height += 1

    img_w = block_w * ep_width
    img_h = block_w * ep_height

    image = Image.new(mode="RGBA", size=(img_w, img_h), color=(0, 0, 0, 0))

    image_draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_ttf_path, size=25 * size_factor)

    pixels = image.load()

    # episode num column
    for num_episode in range(0, max_episodes):
        image_draw.text(
            (0, block_w + num_episode * block_w + (16 * size_factor)),
            str(num_episode + 1),
            font=font,
            fill=(0, 0, 0),
        )

    for xx in range(0, ep_width - 2):
        # first row: season number
        image_draw.text(
            (ep_width * 2 + xx * block_w + (10 * size_factor), 0),
            str(xx + 1),
            font=font,
            fill=(0, 0, 0),
        )
        # rating cells
        for yy in range(0, len(data["data"][xx])):
            rating = data["data"][xx][yy]
            color = get_color(rating)
            for y in range(0, block_w):
                for x in range(0, block_w):
                    pixels[
                        ep_width * 2 + xx * block_w + x, block_w + yy * block_w + y
                    ] = color
            image_draw.text(
                (
                    ep_width * 2 + xx * block_w + (10 * size_factor),
                    block_w + yy * block_w + (16 * size_factor),
                ),
                str(rating),
                font=font,
                fill=(0, 0, 0),
            )
    image.show()
