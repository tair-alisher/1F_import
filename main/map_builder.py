def build_map_file(lines):
    from main.main import print_success_message

    write_data_to_file(lines)
    print_success_message('map file')


def write_data_to_file(data):
    from sources.serv import print_progress

    output = open('results\\map.py', 'w')
    output.write('hashMap = {\n')
    for index, line in enumerate(data):
        row = line.split(',')

        for position, key in enumerate(row):
            new_line = "    '%{0}%': {1},\n".format(key, position)
            output.write(new_line)

        print_progress(1, 1)

        break
    output.write('}\n')
    output.close()
