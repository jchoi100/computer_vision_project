import cv2
import numpy as np
import sys
from PIL import Image
from pytesseract import image_to_string

def preprocess(img_file):
	img = cv2.imread(sys.argv[1], 0)
	img = cv2.medianBlur(img, 5)
	th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 2)
	th = cv2.fastNlMeansDenoising(th, None, 10, 10, 7)
	return th

def main():
	if len(sys.argv) != 2:
		print("Wrong number of input arguments.")
		sys.exit()
	# img = cv2.imread(sys.argv[1], 0)
	# img = cv2.medianBlur(img, 5)
	# th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 2)
	# th = cv2.fastNlMeansDenoising(th, None, 10, 10, 7)
	th = preprocess(sys.argv[1])
	cv2.imwrite(sys.argv[1] + '_thresh.png', th)
	text = image_to_string(Image.open(sys.argv[1] + '_thresh.png'))
	# print(text)
	# print("=========================================")
	text_splitted = text.split(" ")
	print("Total of " + str(len(text_splitted)) + " words detected.")
	with open(sys.argv[1] + '_output_text.txt', 'w') as writer:
		try:
			for word in text_splitted:
				writer.write(word + " ")
		except IOError:
			raise Exception("Exception while writing text file for input image " + sys.argv[1] + ".")
	print("Output written successfully!")

if __name__ == "__main__":
	main()