import pynvim
import os
import re

@pynvim.plugin
class Subtitle:
    def __init__(self, vim):
        self.vim = vim

    @pynvim.command('SubPlay', range='', nargs='*', sync=False)
    def play_subtitle(self, args, range):
        filename = self.vim.current.buffer.name
        dirname = os.path.dirname(filename)
        filename = os.path.basename(filename)
        extension = os.path.splitext(filename)[1]

        if extension=='.srt':
            player = SrtPlayer(self.vim)
        elif extension=='.ass':
            player = AssPlayer(self.vim)
        else:
            raise Exception('No known subtitle file type')

        video = re.sub(r'-.*'+extension, '.mkv', filename)
        player.play_subtitle(range, dirname+'/video/'+video)
        #en el mismo directorio
        #video = os.path.splitext(filename)[0] + '.mkv'
        #player.play_subtitle(range, dirname+'/'+video)


class SubPlayer:
    def __init__(self, vim):
        self.vim = vim
        self.command = 'mpv --vo=null --start={start} --end={end} {videofile}'

    def play_subtitle(self, range, videofile):
        raise NotImplementedError('play_subtitle() needs to be overrided')


class SrtPlayer(SubPlayer):
    def __init__(self, vim):
        super().__init__(vim)

    def play_subtitle(self, range, videofile):
        line = self.vim.current.line

        if self.is_timestamp(line):
            self.play(line.split(), videofile)
        else: #search for a timestamp
            #go up until a blank line or start of file
            line_number = range[0]
            line = self.vim.current.buffer[line_number-1]
            while line_number>0 and line:
                line_number -= 1
                line = self.vim.current.buffer[line_number-1]
            #blank, id, timestamp, text
            #so go 2 lines below
            line_number += 2
            line = self.vim.current.buffer[line_number-1]
            if self.is_timestamp(line):
                self.play(line.split(), videofile)
            else:
                raise Exception('No timestamp found: '+line)


    def play(self, time, videofile):
        start = time[0].replace(',', '.')
        end = time[2].replace(',', '.')
        cmd = self.command.format(start=start, end=end, videofile=videofile)
        print(cmd)
        os.system(cmd)

    def is_timestamp(self, line):
        time = line.split()
        return len(time)==3 and time[1]=='-->'

class AssPlayer(SubPlayer):
    def __init__(self, vim):
        super().__init__(vim)

    def play_subtitle(self, range, videofile):
        #Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
        line = self.vim.current.line

        time = line.split(sep=',')
        start = time[1]
        end = time[2]

        cmd = self.command.format(start=start, end=end, videofile=videofile)
        print(cmd)
        os.system(cmd)
