import os
from pathlib import Path

import sources.db as db
import sources.constants as constants

from sources.receiver_identifiers import get_receiver_by_code


def build_xml_data(lines):
    from results.map import hashMap
    from sources.serv import print_progress
    from main.main import print_success_message
    from results.sender_identifiers import get_sender_id_by_okpo

    header = {"%REC%": '', "%SENDER%": '', "%TIME%": constants.period}

    output = open('results\\data.py', 'w')

    static_data = form_static_data()

    output.write(static_data)
    output.write('\n\ndata = {')

    total = len(lines) - 1
    iteration = 0

    invalid_soates_log = open('logs\\invalid_soates.txt', 'w')

    for index, line in enumerate(lines, 1):
        if index > len(lines) - 1:
            break

        row = lines[index].split(',')

        try:
            soate = row[5]
        except IndexError:
            break

        try:
            code = soate[3:8]  # код области берем из СОАТЕ: 417 [02 000] ...
            header['%REC%'] = get_receiver_by_code[code]['id']
        except KeyError:
            invalid_soates_log.write('{0}\n'.format(soate))
            iteration += 1
            continue

        try:
            okpo = row[4]
        except IndexError:
            break

        header['%SENDER%'] = get_sender_id_by_okpo[okpo]

        sections = form_sections_id_and_template_dictionary(okpo)
        sections = replace_xml_header_keys_with_values(sections, header)
        sections = replace_xml_body_keys_with_values(sections, hashMap, row)

        add_data_to_xml_table(sections)

        data = form_dynamic_data(sections, okpo, iteration, soate, header['%SENDER%'], code)
        output.write(data)

        iteration += 1
        print_progress(iteration, total)

    db.xml.commit()

    invalid_soates_log.close()
    output.write('}\n')
    output.close()
    message = 'data file'
    if len(lines) > 500:
        message = '\ndata file'
    print_success_message(message)


def form_static_data():
    from datetime import datetime
    static_data = """static = {
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
        str(datetime.now())[:-3],
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
    return static_data


def form_sections_id_and_template_dictionary(okpo):
    sections = {}
    for filename in os.listdir('templates'):
        key = "{0}_{1}".format(okpo, filename.replace('.xml', ''))
        sections[key] = Path('templates\\{0}'.format(filename)).read_text()
    return sections


def replace_xml_header_keys_with_values(sections, header):
    for key, value in header.items():
        for section, xml_content in sections.items():
            sections[section] = xml_content.replace(key, value)
    return sections


def replace_xml_body_keys_with_values(sections, hash_map, row):
    for key, value in hash_map.items():
        val = '' if row[value] == '0' or row[value] == '0.0' else row[value]
        for section, xml_content in sections.items():
            if key in xml_content:
                sections[section] = xml_content.replace(key, val)
    return sections


def add_data_to_xml_table(sections):
    for section, xml_content in sections.items():
        if db.xml(title=section):
            record = db.xml(title=section)
            db.xml.update(record, content=xml_content)
        else:
            db.xml.insert(title=section, content=xml_content)


def form_dynamic_data(sections, okpo, iteration, soate, sender, code):
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
        sender,
        get_receiver_by_code[code]['type']
    )

    for section in sections.keys():
        data += form_section_template_title(section, okpo)
    data += "    },\n"

    return data


def form_section_template_title(section, okpo):
    key = section.replace("{0}_".format(okpo), "")
    template_title = "        '{0}': '{1}',\n".format(key, section)
    return template_title
