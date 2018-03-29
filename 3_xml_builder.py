# python 3.6.3
# https://dbfconv.com/ dbf to csv converter online

import os
import sys
import datetime
from pathlib import Path

from sources.sender_identifiers import get_sender_id_by_okpo
from sources.receiver_identifiers import get_receiver_by_code
from sources.serv import print_progress
import sources.constants as constants
import sources.db as db

from results.map import hashMap


file = input('enter the name of the file: ')

filename = "input\\%s" % file  # csv полученное из dbf

try:
    with open(filename) as f:
        content = f.readlines()
except FileNotFoundError:
    print('no such file. aborted.')
    sys.exit()

header = {
    "%REC%": '', "%SENDER%": '', "%TIME%": constants.period
}

if not Path('results').exists():
    Path('results').mkdir()

output = open('results\\data.py', 'w')

output.write("""
static = {
    'Form_ID': '%s',
    'PeriodType': '%s',
    'Datetime': '%s',
    'Section_ID_1': '%s',
    'Section_ID_2': '%s',
    'Section_ID_3': '%s',
    'Section_ID_4': '%s',
    'Section_ID_5': '%s',
    'Section_ID_6': '%s',
    'DSDMoniker_1': '%s',
    'DSDMoniker_2': '%s',
    'DSDMoniker_3': '%s',
    'DSDMoniker_4': '%s',
    'DSDMoniker_5': '%s',
    'DSDMoniker_6': '%s',
}
""" % (
    constants.form_id,
    constants.period,
    str(datetime.datetime.now())[:-3],
    constants.section_id_1,
    constants.section_id_2,
    constants.section_id_3,
    constants.section_id_4,
    constants.section_id_5,
    constants.section_id_6,
    constants.dsd_moniker_1,
    constants.dsd_moniker_2,
    constants.dsd_moniker_3,
    constants.dsd_moniker_4,
    constants.dsd_moniker_5,
    constants.dsd_moniker_6
    )
)

output.write('\n\ndata = {')

content = [x.strip() for x in content]

total = len(content) - 1
iteration = 0
missed = 0
wrong_soate = 0
ok = 0

broken = open('logs\\wrong_soates.txt', 'w')

for index, line in enumerate(content, 1):
    if index > len(content)-1:
        print('\nend of file. index: {0}, all rows: {1}'.format(index, len(content)))
        break

    row = content[index].split(',')
    try:
        soate = row[5]
        code = soate[3:8]  # код области берем из СОАТЕ: 417 [02 000] ...
        header['%REC%'] = get_receiver_by_code[code]['id']
    except IndexError:
        print('\nend of file. wrong row index for soate')
        break
    except KeyError:
        wrong_soate += 1
        broken.write(str(row[5]))
        broken.write('\n')
        iteration += 1
        continue

    try:
        okpo = row[4]
    except IndexError:
        print('\nend of file. okpo was not found')
        break
    ok += 1
    header['%SENDER%'] = get_sender_id_by_okpo[okpo]

    sections = {}

    for filename in os.listdir('templates'):
        key = "{0}_{1}".format(okpo, filename.replace('.xml', ''))
        sections[key] = Path('templates\\{0}'.format(filename)).read_text()

    for key, value in header.items():
        for section, xml_content in sections.items():
            sections[section] = xml_content.replace(key, value)

    for key, value in hashMap.items():
        val = '' if row[value] == '0' or row[value] == '0.0' else row[value]
        for section, xml_content in sections.items():
            if key in xml_content:
                sections[section] = xml_content.replace(key, val)

    for section, xml_content in sections.items():
        if db.xml(title=section):
            record = db.xml(title=section)
            db.xml.update(record, content=xml_content)
        else:
            db.xml.insert(title=section, content=xml_content)

    data = """
    %d: {
        'OKPO': '%s',
        'SOATE': '%s',
        'User_ID': '%s',
        'UserInfo_ID': '',
        'DepartmentType': '%s',
        'MessagesStatuses_ID': '',
    """ % (
        iteration,
        okpo,
        soate,
        header['%SENDER%'],
        get_receiver_by_code[code]['type']
    )
    data += "    "
    for section in sections.keys():
        key = section.replace("{0}_".format(okpo), "")

        data += """'%s': '%s',
        """ % (key, section)

    data += "},\n"

    output.write(data)

    iteration += 1
    print_progress(iteration, total)
db.xml.commit()

broken.close()
output.write('}\n')
output.close()
print('\nmissed: %d' % missed)
print('wrong soate: %d' % wrong_soate)
print('ok: %d' % ok)
