# python 3.6.3
# https://dbfconv.com/ dbf to csv converter online

import main.main as main
from main.map_builder import build_map_file
from main.sender_id_getter import build_sender_ids_file
from main.xml_builder import build_xml_data
from main.data_uploader import data_import

main.create_dir_if_not_exists('results')

filename = input('enter the name of the file: ')
file = 'input\\{0}'.format(filename)
lines = main.get_clean_lines(file)

build_map_file(lines)
build_sender_ids_file(lines)
build_xml_data(lines)
data_import()
