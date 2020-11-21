"""
    according to the times on the srt
    obtain the text through ocr
"""

import sys
import os
import video_sub_avg as video
import sub_parser as sub
import extract_text
import srt

import datetime
from tqdm import tqdm

def to_seconds_micro(time):
    seconds = int(time)
    micro = int((time - seconds)*1e6)

    return datetime.timedelta(seconds=seconds, microseconds=micro)

def create_subtitle(index, times, text):
    return srt.Subtitle(index, to_seconds_micro(times.start), to_seconds_micro(times.end), text)

def usage(program):
    print(program, 'file.srt', 'file.video')

def main(argv):
    if len(argv) != 3:
        usage(argv[0])
        return 1

    subtitle_name = argv[1]
    video_name = argv[2]
    (name, extension) = os.path.splitext(subtitle_name)
    output_file = name+'_ocr'+extension
    print(output_file)

    if extension == '.srt':
        parser = sub.srt_parse(subtitle_name)

    videofile = video.extractor(video_name, buffer_size=2)

    result = []
    index = 1
    text = '...'
    for s in tqdm(parser.obtain_times()):
        frame = videofile.get_average_frame(s)
        if len(frame):
            text = extract_text.extract(frame, index)
        result.append(create_subtitle(index, s, text))
        index += 1

    with open(output_file, 'w') as salida:
        for s in result:
            print(s.to_srt(), file=salida, end='')

if __name__ == "__main__":
    main(sys.argv)
