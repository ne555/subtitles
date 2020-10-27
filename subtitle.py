import pynvim
import os
import fnmatch
import subprocess
import re

def find_file(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

@pynvim.plugin
class Subtitle:
    def __init__(self, vim):
        self.vim = vim

    @pynvim.command('SubPlay', range='', nargs='*', sync=False)
    def play_subtitle(self, args, range):
        filename = self.vim.current.buffer.name
        dirname = os.path.dirname(filename)
        filename = os.path.basename(filename)
        (name, extension) = os.path.splitext(filename)

        #factory
        if extension=='.srt':
            player = SrtPlayer(self.vim, args)
        elif extension=='.ass':
            player = AssPlayer(self.vim, args)
        else:
            raise Exception('No known subtitle file type')

        #get video filename
        candidates = find_file(re.sub(r'-.*$', '', name)+'.*', dirname+'/video/')
        valid_extensions = ['.mkv', '.avi', '.mp4', '.webm', '.wmv']
        for c in candidates:
            if os.path.splitext(c)[1] in valid_extensions:
                video = c
                break

        player.play_subtitle(range, video)


class SubPlayer:
    def __init__(self, vim, args):
        self.vim = vim
        if 'video' in args:
            video = ''
        else:
            video = '--vo=null'

        if 'keep-going' in args:
            keep = ''
        else:
            keep = '--end={end}'

        self.command = 'mpv {video} --start={{start}} {keep} {{videofile}}'.format(video=video, keep=keep)

    def play_subtitle(self, range, videofile):
        start = self.parse_range(range[0])[0]
        end = self.parse_range(range[1])[1]
        cmd = self.command.format(start=start, end=end, videofile=videofile)
        subprocess.Popen(cmd.split())


class SrtPlayer(SubPlayer):
    def __init__(self, vim, args):
        super().__init__(vim, args)

    def search_timestamp(self, line_number):
        line = self.vim.current.buffer[line_number-1]
        if self.is_timestamp(line):
            return line_number
        else: #search for a timestamp
            #go up until a blank line or start of file
            while line_number>0 and line:
                line_number -= 1
                line = self.vim.current.buffer[line_number-1]
            #so go 2 lines below
            return line_number + 2

    def parse_range(self, line_number):
        time = self.search_timestamp(line_number)
        return self.parse(self.vim.current.buffer[time-1])

    def parse(self, time):
        time = time.split()
        start = time[0].replace(',', '.')
        end = time[2].replace(',', '.')
        return start, end

    def is_timestamp(self, line):
        time = line.split()
        return len(time)==3 and time[1]=='-->'

class AssPlayer(SubPlayer):
    def __init__(self, vim, args):
        super().__init__(vim, args)

    def parse_range(self, line_number):
        #Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
        line = self.vim.current.buffer[line_number-1]
        time = line.split(sep=',')
        start = time[1]
        end = time[2]
        return start, end
