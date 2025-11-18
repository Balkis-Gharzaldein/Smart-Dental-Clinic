import cv2
import numpy as np
from matplotlib import pyplot as plt

image = cv2.imread('C:/Users/HP/Downloads/Basic_panoramic_radiograph.jpg')

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Gaussian Blur
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Histogram Equalization
equalized_image = cv2.equalizeHist(blurred_image)

# Canny
edges = cv2.Canny(equalized_image, 100, 200)


kernel = np.array([[0, -1, 0], [-1, 5,-1],[0, -1, 0]])
sharpened_image = cv2.filter2D(equalized_image, -1, kernel)

plt.figure(figsize=(10, 8))
plt.subplot(2, 3, 1), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)), plt.title('Original Image')
plt.subplot(2, 3, 2), plt.imshow(gray_image, cmap='gray'), plt.title('Grayscale Image')
plt.subplot(2, 3, 3), plt.imshow(blurred_image, cmap='gray'), plt.title('Blurred Image')
plt.subplot(2, 3, 4), plt.imshow(equalized_image, cmap='gray'), plt.title('Equalized Image')
plt.subplot(2, 3, 5), plt.imshow(edges, cmap='gray'), plt.title('Edge Detection')
plt.subplot(2, 3, 6), plt.imshow(sharpened_image, cmap='gray'), plt.title('Sharpened Image')
plt.tight_layout()
plt.show()
