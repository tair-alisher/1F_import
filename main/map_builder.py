import sys

def build_map_file(lines):
    write_data_to_file(lines)
    print('map file was build')


def write_data_to_file(data):
    output = open('results\\map.py', 'w')
    output.write('hashMap = {\n')
    for index, line in enumerate(data, 0):
        row = line.split(',')

        for position, key in enumerate(row):
            new_line = "    '%{0}%': {1},\n".format(key, position)
            output.write(new_line)
        break
    output.write('}')
    output.close()
