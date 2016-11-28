import cv2
import numpy as np
import sys
from PIL import Image
from pytesseract import image_to_string
from g_translate import translate
import codecs

IMG_PREFIX = (sys.argv[1]).split(".")[0]
DEST = [sys.argv[i] for i in range(2, len(sys.argv))]
LANGUAGES = {"en": "English", "fr": "French", "es": "Spanish", "ko": "Korean", \
             "ja": "Japanese", "zh-CN": "Chinese (traditional)", "ar": "Arabic", \
             "de": "German", "hi": "Hindi", "ru": "Russian", "el": "Greek"}

def greetings():
    print("=============== Welcome to James' text recognition and translation software! ===============")

def threshold_image():
    img = cv2.imread(sys.argv[1], 0)
    img = cv2.medianBlur(img, 5)
    th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 2)
    th = cv2.fastNlMeansDenoising(th, None, 10, 10, 7)
    cv2.imwrite(IMG_PREFIX + '_thresh.png', th)

def extract_text():
    raw_text = image_to_string(Image.open(IMG_PREFIX + '_thresh.png'))
    no_new_line_text = ""
    for char in raw_text:
        if char is not "\n":
            no_new_line_text += char
    text = raw_text.split(" ")
    print("Total of " + str(len(text)) + " words detected.")
    return raw_text, text, no_new_line_text

def write_original_output(text):
    with open(IMG_PREFIX + '_output_text.txt', 'w') as writer:
        try:
            for word in text:
                writer.write(word + " ")
        except IOError:
            raise Exception("Exception while writing text file for input image " + sys.argv[1] + ".")    
    print("Output successfully written in original input language.")

def write_translated_output(raw_text, src):
    for dest_lang in DEST:
        translated = translate(raw_text, dest_lang, src).decode('utf-8')
        try:
            codecs.open(IMG_PREFIX + '_output_text_' + dest_lang + '.txt', 'a', 'utf-8').write(translated)
        except:
            raise Exception("Exception while writing text file for language " + LANGUAGES[dest_lang] + ".")
        print("Output successfully written in " + LANGUAGES[dest_lang] + ".")

def farewell():
    print("======================================== Good Bye! =========================================")
    return 0

def main():
    greetings()
    threshold_image()
    raw_text, text, no_new_line_text = extract_text()    
    write_original_output(text)
    # print(len(no_new_line_text))
    # doc4 works if we split the text at 1850.
    # doc4 works for length 1850.
    # doc4 doesn't work for 1900.
    # doc4 has length 1983.
    chopped_text = []
    begin_index = 0
    for i in range(0, len(no_new_line_text), 1000):
        end_index = begin_index + 1000 if begin_index + 1000 < len(no_new_line_text) else len(no_new_line_text)
        chopped_text.append(no_new_line_text[begin_index:end_index])
        begin_index += 1000
    for c in chopped_text:
        write_translated_output(c, "auto")
    return farewell()

if __name__ == '__main__':
    main()
