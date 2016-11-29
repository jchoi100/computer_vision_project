import cv2
import sys
from PIL import Image
from pytesseract import image_to_string
from g_translate import translate
import codecs

if len(sys.argv) < 2:
    print("Usage: Too few arguments! You need to specify at least the target image file.")
    sys.exit(0)
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
    th_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 2)
    th_img = cv2.fastNlMeansDenoising(th_img, None, 7, 21, 7)
    cv2.imwrite(IMG_PREFIX + '_thresh.png', th_img)

def extract_text():
    raw_text = image_to_string(Image.open(IMG_PREFIX + '_thresh.png'))
    split_text = raw_text.split(" ")
    print("Total of " + str(len(split_text)) + " words detected.")
    return raw_text, split_text

def write_original_output(text):
    with open(IMG_PREFIX + '_output_text.txt', 'w') as writer:
        try:
            for word in text:
                writer.write(word + " ")
        except IOError:
            raise Exception("Exception while writing text file for input image " + sys.argv[1] + ".")    
    print("Output successfully written in original input language.")

def write_translated_output(text, src):
    chopped_text = []
    for i in range(0, len(text), 1000):
        end_index = i + 1000 if i + 1000 < len(text) else len(text)
        chopped_text.append(text[i:end_index])
    for dest_lang in DEST:
        for c in chopped_text:
            translated = translate(c, dest_lang, src).decode('utf-8')
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
    raw_text, split_text = extract_text()    
    write_original_output(split_text)
    write_translated_output(raw_text, "auto")
    return farewell()

if __name__ == '__main__':
    main()
