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

class sub_time:
    def __init__(self, index, start, end):
        self.index = index
        self.start = start
        self.end = end
    def __str__(self):
        return '{}: {} --> {}'.format(self.index, self.start, self.end)

class sub_parse:
    def __init__(self, input_file):
        self.input_file = open(input_file)

class srt_parse(sub_parse):
    def __init__(self, input_file):
        super().__init__(input_file)

    def extractor(self):
        return srt.parse(self.input_file)

    @staticmethod
    def to_seconds(time):
        return time.seconds + time.microseconds / 1e6

    @staticmethod
    def format(subtitle):
        start = srt_parse.to_seconds(subtitle.start)
        end = srt_parse.to_seconds(subtitle.end)
        return sub_time(subtitle.index, start, end)

    def obtain_times(self):
        result = []
        for s in self.extractor():
            result.append(self.format(s))
        return result

class ass_parse(sub_parse):
    pass

def obtain_times(subtitle_file):
    pass

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
    for s in parser.obtain_times():
        start = int(s.start * fps)
        end = int(s.end * fps)
        capture.set(cv.CAP_PROP_POS_FRAMES, int(s.start * fps))
        print(s.index, start, end)
        frames = [capture.read()[1] for K in range(start, end)]
        avg = average(frames)
        if s.index > 0:
            cv.imshow('foo', avg)
            cv.waitKey()


if __name__ == "__main__":
    main(sys.argv)
