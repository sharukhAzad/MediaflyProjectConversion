"""
AUTHOR

    Ron Yehoshua <ryehoshua@mediafly.com>    
"""

from PIL import Image

def process_image(filename):
    try:
        processed_filename = "processed-" + filename
        image = Image.open(filename)
        resized_image = image.resize((960, 540)) # resizing to 1280 x 720
        resized_image = resized_image.transpose(Image.FLIP_LEFT_RIGHT)
        resized_image = resized_image.transpose(Image.FLIP_TOP_BOTTOM)
        resized_image.save(processed_filename)
        return processed_filename 
    except:
        return None