import sys

file = input('enter the name of the file: ')

filename = "input\\%s" % file  # csv полученное из dbf

try:
    with open(filename) as f:
        content = f.readlines()
except FileNotFoundError:
    print('no such file. aborted')
    sys.exit()

content = [x.strip() for x in content]

output = open('results\\map.py', 'w')

output.write('hashMap = {\n')

for index, line in enumerate(content, 0):
    row = line.split(',')

    for position, key in enumerate(row):
        new_line = "    '%{0}%': {1},\n".format(key, position)
        output.write(new_line)

    break

output.write('}')
output.close()
