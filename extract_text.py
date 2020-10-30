"""
    Enmascara el texto presente
    Pseudocode:
        * remove watermark (upper left)
        * grayscale
        * threshold >250
        * dilate
        * multiply
"""

import sys
import os

import cv2 as cv
import numpy as np
import pytesseract as tess

def preprocess(image):
    grayscale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    watermark = (80, 50)
    grayscale[0:watermark[0], 0:watermark[1]] = 0

    umbral = 250
    threshold = cv.threshold(grayscale, umbral, 255, cv.THRESH_BINARY)[1]

    kernel = np.ones((3, 3), np.uint8)
    dilatado = cv.dilate(threshold, kernel)

    result = cv.bitwise_and(grayscale, grayscale, mask=dilatado)
    return result

def extract(image):
    image = preprocess(image)
    return tess.image_to_string(image)
