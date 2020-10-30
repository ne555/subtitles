"""
    according to the times on the srt
    obtain the text through ocr
"""

import video_sub_avg as video
import sub_parser as sub
import extract_text
import srt

def to_seconds_micro(time):
    seconds = int(time)
    micro = int((time - seconds)*1e6)
    return (seconds, micro)

def create_subtitle(index, times, text):
    return srt.Subtitle(index, to_seconds_micro(times.start), to_seconds_micro(times.end), text)

def main(argv):
    if len(argv) != 3:
        usage(argv[0])
        return 1

    subtitle_name = argv[1]
    video_name = argv[2]
    (name, extension) = os.path.splitext(subtitle_name)

    if extension == '.srt':
        parser = sub.srt_parse(subtitle_name)

    video = video.extractor(video_name, buffer_size=2)

    result = []
    index = 1
    for s in parser.obtain_times():
        frame = video.get_average_frame(s)
        text = extract_text.extract(frame)
        result.append(create_subtitle(index, s, text))
        index += 1

    print(srt.compose(result))

if __name__ == "__main__":
    main(sys.argv)
