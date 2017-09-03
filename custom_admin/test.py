from PIL import Image
import sys

import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % (lang))
# Ex: Will use lang 'fra'

txt = tool.image_to_string(
    Image.open('test.jpg'),
    lang='eng',
    builder=pyocr.builders.TextBuilder()
)
word_boxes = tool.image_to_string(
    Image.open('test.jpg'),
    lang="eng",
	builder=pyocr.builders.WordBoxBuilder()
)

line_and_word_boxes = tool.image_to_string(
    Image.open('test.jpg'), lang="eng",
    builder=pyocr.builders.LineBoxBuilder()
)

# Digits - Only Tesseract (not 'libtesseract' yet !)
digits = tool.image_to_string(
    Image.open('test.jpg'),
    lang='eng',
    builder=pyocr.tesseract.DigitBuilder()
)

for line in txt.splitlines():
	if line == '< ACCOUNT DETAILS': print line + ' ok'
	
	
#	date = datetime.strptime('24 May 2016', '%d %b %Y')