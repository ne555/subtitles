"""
    A partir de los tiempos de los srt, extrae los fotogramas y los promedia
"""

import sys
import srt
import os

import cv2 as cv
import numpy as np

def usage(program):
    print(program, 'file.srt', 'file.video')

def average(frames):
    result = np.zeros(shape=frames[0].shape, dtype='float64')
    for f in frames:
        result += f.astype('float64')
    result /= len(frames)
    return result.astype('uint8')

def main(argv):
    if len(argv) != 3:
        usage(argv[0])
        return 1

    subtitle_name = argv[1]
    video_name = argv[2]
    (name, extension) = os.path.splitext(subtitle_name)

    if extension == '.srt':
        parser = srt_parse(subtitle_name)

    capture = cv.VideoCapture(video_name)
    fps = capture.get(cv.CAP_PROP_FPS)
    buffer_size = 2
    for s in parser.obtain_times():
        #obtain the frames in the range
        start = int(s.start * fps) + buffer_size
        end = int(s.end * fps) - buffer_size
        capture.set(cv.CAP_PROP_POS_FRAMES, start)
        print(s.index, start, end)
        frames = [capture.read()[1] for K in range(start, end)]

        if frames:
            avg = average(frames)
            output_filename = 'output/{}_{:03d}'.format(os.path.basename(name), s.index) + '.png'
            cv.imwrite(output_filename, avg)


if __name__ == "__main__":
    main(sys.argv)

class extractor:
    def __init__(self, filename, buffer_size):
        self.buffer_size = buffer_size
        self.capture = cv.VideoCapture(filename)
        self.fps = self.capture.get(cv.CAP_PROP_FPS)

    def get_average_frame(self, time):
        start = int(time.start * self.fps) + self.buffer_size
        end = int(time.end * self.fps) - self.buffer_size
        self.capture.set(cv.CAP_PROP_POS_FRAMES, start)
        frames = [self.capture.read()[1] for K in range(start, int((start+end)/2))]

        if frames:
            return average(frames)
