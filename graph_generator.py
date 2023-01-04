from PIL import Image
import json
import sys

block_w = 64

def load_series(series_id):
    f = open(series_id + ".json", "r")
    return json.loads(f.read())

def get_color(rating):
    if rating < 5:
        return (255, 0, 0)
    if rating < 6:
        return (252, 136, 3)
    if rating < 7:
        return (252, 186, 3)
    if rating < 8:
        return (244, 252, 3)
    if rating < 9:
        return (173, 252, 3)
    return (65, 252, 3)
    
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

    pixels = image.load()
    for xx in range(0, ep_width):
        for yy in range(0, len(data["data"][xx])):
            color = get_color(data["data"][xx][yy])
            for y in range(0, block_w):
                for x in range(0, block_w):
                    pixels[xx*block_w+x, yy*block_w+y] = color
    
    image.show()
