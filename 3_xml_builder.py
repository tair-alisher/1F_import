# python 3.6.3
# https://dbfconv.com/ dbf to csv converter online

import os
import sys
from pathlib import Path
from sources.sender_identifiers import get_sender_id_by_okpo
from sources.receiver_identifiers import get_receiver_by_code
from sources.serv import print_progress
import sources.db as db
from results.map import hashMap

import datetime

import sources.constants as constants

file = input('enter the name of the file: ')

filename = "input\\%s" % file  # csv полученное из dbf

try:
    with open(filename) as f:
        content = f.readlines()
except FileNotFoundError:
    print('no such file. aborted.')
    sys.exit()

content = [x.strip() for x in content]

if not Path('results').exists():
    Path('results').mkdir()

header = {
    "%ID%": 'HeaderDataId_RecordId', "%REC%": '', "%SENDER%": '', "%TIME%": constants.period
}

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

total = len(content)
iteration = 0
missed = 0

for index, line in enumerate(content, 1):
    if index == 21:
        break
    if index > len(content) - 1:
        break
    row = content[index].split(',')

    try:
        soate = row[5]
        code = soate[3:8]  # код области берем из СОАТЕ: 417 [02 000] ...
    except IndexError:
        print('wrong index in row for soate')
        break

    try:
        header['%REC%'] = get_receiver_by_code[code]['id']
    except KeyError:
        missed += 1
        continue

    okpo = row[4]
    header['%SENDER%'] = get_sender_id_by_okpo[okpo]

    sections = {}

    for filename in os.listdir('templates'):
        key = "{0}_{1}".format(okpo, filename.replace('.xml', ''))
        sections[key] = Path('templates\\{0}'.format(filename)).read_text()

    for key, value in header.items():
        for section, content in sections.items():
            sections[section] = content.replace(key, value)

    for key, value in hashMap.items():
        val = '' if row[value] == '0' or row[value] == '0.0' else row[value]
        for section, content in sections.items():
            if key in content:
                sections[section] = content.replace(key, val)

    for section, content in sections.items():
        if db.xml(title=section):
            record = db.xml(title=section)
            db.xml.update(record, content=content)
        else:
            db.xml.insert(title=section, content=content)
        db.xml.commit()

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

output.write('}\n')
output.close()
print("\nmissed: %d" % missed)
