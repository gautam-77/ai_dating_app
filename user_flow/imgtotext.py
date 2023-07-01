import pytesseract
from PIL import Image


def imagetotext(image):
    images = Image.open(f'./{image}')
    text = pytesseract.image_to_string(images)
    return text