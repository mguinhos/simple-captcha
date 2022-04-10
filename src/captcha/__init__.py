from os import walk, path
from random import choice, randint
from PIL import Image, ImageDraw, ImageFont, ImageFilter

dirname = path.dirname(__file__)

def get_all_fonts():
    for root, _dirs, filenames in walk(path.join(dirname, 'fonts')):
        for filename in filenames:
            if filename.endswith('.ttf'):
                yield filename.split(path.sep)[-1], ImageFont.truetype(path.join(root, filename), 48)
    
    return

def get_all_phrases():
    for root, _dirs, filenames in walk(path.join(dirname, 'phrases')):
        for filename in filenames:
            if filename.endswith('.lst'):
                yield filename.split(path.sep)[-1], open(path.join(root, filename), encoding='utf-8').readlines()
    
    return

fonts = dict(get_all_fonts())
phrases = dict(get_all_phrases())

def new(language: str) -> tuple[str, Image.Image]:
    image = Image.new('RGBA', (1024, 256), 0x0000ee)
    idraw = ImageDraw.ImageDraw(image)
    
    image_cx = 512
    image_cy = 128
    
    phrase = choice(phrases[f'{language}.lst'])
    font = fonts[choice(tuple(fonts))]

    phrase_bbox = idraw.textbbox((0, 0), phrase, font=font)

    phrase_cx = (phrase_bbox[2] - phrase_bbox[0]) // 2
    phrase_cy = (phrase_bbox[3] - phrase_bbox[1]) // 2

    for _ in range(500):
        x, y = randint(-100, 100) * 24, randint(-100, 100) * 24
        idraw.text((x + (image_cx - phrase_cx), y + (image_cy - (phrase_cy + 24))), phrase, font=font)
    
    image = image.filter(ImageFilter.BoxBlur(5))
    idraw = ImageDraw.ImageDraw(image)

    idraw.text((image_cx - phrase_cx, image_cy - (phrase_cy + 24)), phrase, font=font)

    return phrase, image