import cv2
import numpy as np
import matplotlib.pyplot as plt

input_data = ['obama_letter1.png', 'obama_letter2.png', 'obama_letter3.png', 'obama_letter4.png', 'obama_letter5.png',\
				'gwb_letter1.png', 'gwb_letter2.png', 'bill_clinton_letter1.png', 'bill_clinton_letter2.png']

# for d in input_data:
img = cv2.imread('data/doc7.png', 0)
template = cv2.imread('data/jhu_logo.png', 0)
w, h = template.shape[::-1]

method = eval('cv2.TM_CCORR_NORMED')
res = cv2.matchTemplate(img, template, method)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
print img.shape
print max_loc
print max_val
top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)
cv2.rectangle(img, top_left, bottom_right, (0,0,255), 2)
plt.subplot(121),plt.imshow(res,cmap='gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(img,cmap='gray')
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
plt.show()
