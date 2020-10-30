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

def usage(program):
    print(program, 'fotograma.png')

def main(argv):
    if len(argv) != 2:
        usage(argv[0])
        return 1

    filename = argv[1]
    print(filename)
    grayscale = cv.imread(filename, cv.IMREAD_GRAYSCALE)

    watermark = (80, 50)
    grayscale[0:watermark[0], 0:watermark[1]] = 0

    umbral = 250
    threshold = cv.threshold(grayscale, umbral, 255, cv.THRESH_BINARY)[1]

    kernel = np.ones((3, 3), np.uint8)
    dilatado = cv.dilate(threshold, kernel)

    result = cv.bitwise_and(grayscale, grayscale, mask=dilatado)
    #cv.imshow('foo', grayscale)
    #cv.waitKey()
    #cv.imshow('foo', threshold)
    #cv.waitKey()
    #cv.imshow('foo', dilatado)
    #cv.waitKey()
    #cv.imshow('foo', result)
    #cv.waitKey()

    output_directory = 'ocr/masked/'
    filename = os.path.basename(filename)
    cv.imwrite(output_directory+filename, result)


if __name__ == "__main__":
    main(sys.argv)
