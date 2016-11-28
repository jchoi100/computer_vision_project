import cv2
import numpy as np
import sys
from PIL import Image
from pytesseract import image_to_string


def main():
	if len(sys.argv) != 2:
		print("Wrong number of input arguments.")
		sys.exit()
	img = cv2.imread(sys.argv[1], 0)
	img = cv2.medianBlur(img, 5)
	th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	img_name = (sys.argv[1]).split('.')[0]
	cv2.imwrite(img_name + '_thresh.png', th)
	print(img_name + '_thresh.png')
	text = image_to_string(Image.open(img_name + '_thresh.png'))
	print(text)
	text_splitted = text.split(" ")
	with open(sys.argv[1] + '_output_text.txt', 'w') as writer:
		try:
			for word in text_splitted:
				writer.write(word + " ")
		except IOError:
			raise Exception("Exception while writing text file for input image " + sys.argv[1] + ".")
	print("Output written successfully!")

if __name__ == "__main__":
	main()