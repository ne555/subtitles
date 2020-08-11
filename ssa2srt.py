#!/bin/python
import asstosrt as ssa
import sys

def main():
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: ' + sys.argv[0] + ' input_file output_file\n')
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    with open(input_filename) as entrada:
        texto = ssa.convert(entrada, no_effect=True)
        with open(output_filename, 'w') as salida:
            texto.replace('\r\n', '\r')
            print(texto, file=salida, end='')


if __name__ == "__main__":
    main()
