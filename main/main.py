import sys


def get_clean_lines(file):
    data = remove_white_spaces(read_input_file(file))
    return data


def read_input_file(input_file):
    try:
        with open(input_file) as f:
            result = f.readlines()
    except FileNotFoundError:
        print('main.read_input_file function. no such file. aborted.')
        sys.exit()
    return result


def remove_white_spaces(lines):
    clean_lines = [x.strip() for x in lines]
    return clean_lines


def print_success_message(message):
    print(message.ljust(110, '.') + 'ok')


def create_dir_if_not_exists(dir_name):
    from pathlib import Path

    if not Path(dir_name).exists():
        Path(dir_name).mkdir()
