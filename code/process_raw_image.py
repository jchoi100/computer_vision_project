import cv2
import numpy as np

"""
Code adapted from docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
"""

img = cv2.imread('doc2.png', 0)
img = cv2.medianBlur(img, 5)

th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

cv2.imwrite('doc2_thresh.png', th)
