import cv2
import numpy as np
import sys
from PIL import Image
from pytesseract import image_to_string
from g_translate import translate
import codecs

img_name = (sys.argv[1]).split(".")[0]
dest = [sys.argv[i] for i in range(2, len(sys.argv))]
languages = {"en": "English", "fr": "French", "es": "Spanish", "ko": "Korean", \
             "ja": "Japanese", "zh-CN": "Chinese (traditional)", "ar": "Arabic", \
             "de": "German", "hi": "Hindi", "ru": "Russian", "el": "Greek"}

def threshold_image():
    img = cv2.imread(sys.argv[1], 0)
    img = cv2.medianBlur(img, 5)
    th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 2)
    th = cv2.fastNlMeansDenoising(th, None, 10, 10, 7)
    cv2.imwrite(img_name + '_thresh.png', th)

def extract_text():
    raw_text = image_to_string(Image.open(img_name + '_thresh.png'))
    text = raw_text.split(" ")
    print("Total of " + str(len(text)) + " words detected.")
    return raw_text, text

def write_original_output(text):
    with open(img_name + '_output_text.txt', 'w') as writer:
        try:
            for word in text:
                writer.write(word + " ")
        except IOError:
            raise Exception("Exception while writing text file for input image " + sys.argv[1] + ".")    
    print("Output successfully written in original input language.")

def write_translated_output(raw_text, src):
    for i in range(len(dest)):
        translated = translate(raw_text, dest[i], "auto").decode('utf-8')
        try:
            codecs.open(img_name + '_output_text_' + dest[i] + '.txt', 'w', 'utf-8').write(translated)
        except:
            raise Exception("Exception while writing text file for language " + languages[dest[i]] + ".")
        print("Output successfully written in language " + languages[dest[i]] + ".")

def main():
    threshold_image()
    raw_text, text = extract_text()    
    write_original_output(text)
    write_translated_output(raw_text, "auto")
    return 0

if __name__ == '__main__':
    main()
