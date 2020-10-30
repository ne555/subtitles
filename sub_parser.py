"""
    extract times and text from subtitle files
"""

import srt

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
