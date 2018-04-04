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


def print_success_message(message, seconds):
    print("%s %d seconds" % (message.ljust(110, '.'), seconds))


def create_dir_if_not_exists(dir_name):
    from pathlib import Path

    if not Path(dir_name).exists():
        Path(dir_name).mkdir()


def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\rprogress:%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()
