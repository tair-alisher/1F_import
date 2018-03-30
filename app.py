from main.main import get_clean_lines
from main.map_builder import build_map_file

filename = input('enter the name of the file: ')
file = 'input\\{0}'.format(filename)
lines = get_clean_lines(file)

build_map_file(lines)
