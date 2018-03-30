def build_sender_ids_file(lines):
    import pypyodbc
    from main.main import print_success_message
    import sources.connection_strings as con_strings

    connection = pypyodbc.connect(con_strings.server)
    cursor = connection.cursor()

    write_ids_to_file(cursor, lines)

    connection.close()
    print_success_message('\nsender_identifiers file')


def write_ids_to_file(cursor, lines):
    from sources.serv import print_progress

    csv = open('results\\sender_identifiers.py', 'w')
    csv.write('get_sender_id_by_okpo = {\n')

    total = len(lines) - 1
    iteration = 0

    for index, line in enumerate(lines, 1):
        if index > len(lines) - 1:
            break

        row = lines[index].split(',')

        try:
            okpo = row[4]
        except IndexError:
            break

        select_query = """
        SELECT Id as id
        FROM AspNetUsers
        WHERE OKPO = ?
        """

        cursor.execute(select_query, [okpo])

        identifier = get_identifier_or_empty_string(cursor.fetchone())

        csv.write("    '{0}': '{1}',\n".format(okpo, identifier))

        iteration += 1
        print_progress(iteration, total)

    csv.write('}\n')
    csv.close()


def get_identifier_or_empty_string(row):
    try:
        sender_id = row['id']
    except TypeError:
        sender_id = ''
    return sender_id
