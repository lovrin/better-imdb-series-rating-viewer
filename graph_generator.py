from PIL import Image, ImageDraw, ImageFont
import json
import sys
import math

COLORS = [
    (255, 0, 0),    # 0
    (255, 0, 0),    # 1
    (255, 0, 0),    # 2
    (255, 0, 0),    # 3
    (255, 69, 0),   # 4
    (255, 140, 0),  # 5
    (255, 215, 0),  # 6
    (231, 255, 0),  # 7
    (198, 255, 0),  # 8
    (140, 255, 0),  # 9
    (61, 255, 0)    # 10
]

block_w = 64

def lerp(a, b, t):
    return a * (1 - t) + b * t

def load_series(series_id):
    f = open(series_id + ".json", "r")
    return json.loads(f.read())

def get_color(rating):
    flr = math.floor(rating)
    c_a = COLORS[flr]
    c_b = COLORS[flr+1]
    t = rating-flr

    r = int(lerp(c_a[0], c_b[0], t))
    g = int(lerp(c_a[1], c_b[1], t))
    return (r, g, 0)
    
if __name__ == '__main__':
    series_id = sys.argv[1]
    data = load_series(series_id)

    ep_width = len(data["data"])
    ep_height = 0
    for it in data["data"]:
        if len(it) > ep_height:
            ep_height = len(it)

    img_w = block_w*ep_width
    img_h = block_w*ep_height

    image = Image.new('RGB', (img_w, img_h))
    
    image_draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial', size=25)

    pixels = image.load()
    for xx in range(0, ep_width):
        for yy in range(0, len(data["data"][xx])):
            rating = data["data"][xx][yy]
            color = get_color(rating)
            for y in range(0, block_w):
                for x in range(0, block_w):
                    pixels[xx*block_w+x, yy*block_w+y] = color    
            image_draw.text((xx*block_w+15, yy*block_w+20), str(rating), font=font, fill =(0, 0, 0))
    image.show()
