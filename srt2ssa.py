#!/bin/python
import srt
import sys
from datetime import timedelta

def timedelta_print(time, salida):
    seconds = time.seconds
    centiseconds = time.microseconds // 10000
    hours = seconds // 3600
    seconds = seconds % 3600
    minutes = seconds // 60
    seconds = seconds % 60
    print('{:01d}:{:02d}:{:02d}.{:02d}'.format(hours, minutes, seconds, centiseconds), file=salida, end=',')

def main():
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: ' + sys.argv[0] + ' input_file output_file\n')
        sys.exit(1)
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    with open(input_filename) as entrada:
        with open(output_filename, 'w') as salida:
            print('[Events]', file=salida)
            print('Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text', file=salida)
            subs = srt.parse(entrada)
            for s in subs:
                texto = s.content
                #italics and line breaks
                texto = texto.replace('<i>', '{\\i1}').replace('</i>', '{\\i}')
                texto = texto.replace('\n', '\\N')
#Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
                print('Dialogue: 0,', file=salida, end='')
                timedelta_print(s.start, salida)
                timedelta_print(s.end, salida)
                print('Default', '', '0,0,0', '', texto, file=salida, sep=',', end='\n')


if __name__ == "__main__":
    main()
