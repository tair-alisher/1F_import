import sys
import pypyodbc
from sources.serv import print_progress
import sources.connection_strings as con_strings

file = input('enter the name of the file: ')

filename = 'input\\%s' % file

try:
    with open(filename) as f:
        content = f.readlines()
except FileNotFoundError:
    print('no such file. aborted')
    sys.exit()

csv = open('sources\\sender_identifiers.py', 'w')
csv.write('get_sender_id_by_okpo = {')
csv.write('\n')

connection = pypyodbc.connect(con_strings.server)
cursor = connection.cursor()

content = [x.strip() for x in content]

total = len(content)-1
iteration = 0

for index, line in enumerate(content, 1):
    if index > len(content)-1:
        break

    SQLCommand = "SELECT Id as id FROM AspNetUsers WHERE OKPO = ?"

    iteration += 1
    row = content[index].split(',')

    try:
        okpo = row[4]
    except IndexError:
        print('\nend of file')
        break

    SQLCommand = "SELECT Id as id FROM AspNetUsers WHERE OKPO = ?"

    cursor.execute(SQLCommand, [okpo])
    result = cursor.fetchone()

    try:
        identifier = result['id']
    except TypeError:
        identifier = ''

    csv.write("    '{0}': '{1}',\n".format(okpo, identifier))

    print_progress(iteration, total)

connection.close()

csv.write('}\n')
csv.close()
