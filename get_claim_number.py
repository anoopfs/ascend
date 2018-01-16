from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
from PIL import Image as Image
import pyocr
import pyocr.builders
import pytesseract
import string


def get_claim_number():
    def remove_non_printable(s):
        return filter(lambda x: x in string.printable, s)

    def is_sendback_letter(page_text):
        if 'Re' in page_text and 'Dear' in page_text and fuzz.ratio('United Healthcare\nMedicare Solutions\nP.O. Box 31362 Salt Lake City, Utah 84131-0362', page_text[:100]) >= 75:
            return True
        return False

    path = 'C:\\Users\\anoopshar\\Desktop\\002_00000034.tif'

    image = Image.open(path)
    image = image.convert('RGB')
    image = image.convert('1')

    tools = pyocr.get_available_tools()[0]
    # page_text = remove_non_printable(tools.image_to_string(image, builder=pyocr.builders.TextBuilder()))
    page_text = remove_non_printable(pytesseract.image_to_string(image))
    if is_sendback_letter(page_text):
        claim_line = [line for line in page_text.split('\n') if 'claim' in line.lower() and ':' in line][0]
        return claim_line
    return 'NA'
        # claim_number = re.search(':(.*)-', claim_line).group(1)
        # print claim_number
