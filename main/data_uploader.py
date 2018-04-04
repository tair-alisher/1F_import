import pyodbc
import sources.db as db
import importlib as imp


def data_import():
    import time
    from main.main import print_progress
    from main.main import print_success_message
    import sources.connection_strings as con_strings
    import results.data as res_data

    start = time.time()

    res_data = imp.reload(res_data)
    connection = pyodbc.connect(con_strings.clone)
    cursor = connection.cursor()

    log = open('logs\\log.txt', 'w')

    iteration = 0
    total = len(res_data.data)
    db.Database.open_db()

    for row in res_data.data:
        try:
            data_upload(cursor, res_data.data, row, log)
        except pyodbc.Error as err:
            log.write('\n\n' + str(err))
            connection.rollback()

        connection.commit()
        iteration += 1
        print_progress(iteration, total)

    log.close()

    connection.close()
    print_success_message('import', time.time() - start)


def data_upload(cursor, data, row, log):
    import results.data as res_data

    res_data = imp.reload(res_data)
    # ---------------- UsersInfo table ---------------- #
    users_info_insert_query = """
                INSERT INTO UsersInfo(
                    OKPO,
                    User_ID)
                VALUES (?, ?)
                """
    cursor.execute(
        users_info_insert_query,
        data[row]['OKPO'],
        data[row]['User_ID'])
    user_info_id = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

    # ---------------- MessagesStatuses table ---------------- #
    messages_statuses_insert_query = """
                INSERT INTO MessagesStatuses(
                    Form_ID,
                    UsersInfo_ID,
                    PeriodType,
                    DepartmentType,
                    DateTime)
                VALUES (?, ?, ?, ?, ?)
                """
    cursor.execute(
        messages_statuses_insert_query,
        res_data.static['Form_ID'],
        user_info_id,
        res_data.static['PeriodType'],
        data[row]['DepartmentType'],
        res_data.static['Datetime'])
    messages_statuses_id = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

    # ---------------- RespondentDatas table ---------------- #
    respondent_datas_insert_query = """
                INSERT INTO RespondentDatas(
                    MessageStatusID,
                    SoateCode)
                VALUES(?, ?)
                """
    cursor.execute(
        respondent_datas_insert_query,
        messages_statuses_id,
        data[row]['SOATE'])

    # ---------------- Messages table section 1 ---------------- #
    last_messages_table_id = cursor.execute("Select IDENT_CURRENT('Messages')").fetchone()[0]
    last_messages_table_id += 1
    message_xml = db.Database.xml(title=data[row]['section_1'])[0]['content'].replace('%ID%', str(last_messages_table_id))
    messages_insert_query = """
                INSERT INTO Messages(
                    Message_XML,
                    Section_ID,
                    MessagesStatuses_ID,
                    DSDMoniker)
                VALUES (?, ?, ?, ?)
                """
    cursor.execute(
        messages_insert_query,
        message_xml,
        res_data.static['Section_ID_1'],
        messages_statuses_id,
        res_data.static['DSDMoniker_1'])
    message_1 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

    # ---------------- Messages table section 2 ---------------- #
    last_messages_table_id += 1
    message_xml = db.Database.xml(title=data[row]['section_2'])[0]['content'].replace('%ID%', str(last_messages_table_id))
    cursor.execute(
        messages_insert_query,
        message_xml,
        res_data.static['Section_ID_2'],
        messages_statuses_id,
        res_data.static['DSDMoniker_2'])
    message_2 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

    # ---------------- Messages table section 3 ---------------- #
    last_messages_table_id += 1
    message_xml = db.Database.xml(title=data[row]['section_3'])[0]['content'].replace('%ID%', str(last_messages_table_id))
    cursor.execute(
        messages_insert_query,
        message_xml,
        res_data.static['Section_ID_3'],
        messages_statuses_id,
        res_data.static['DSDMoniker_3']
    )
    message_3 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

    # ---------------- Messages table section 4 ---------------- #
    last_messages_table_id += 1
    message_xml = db.Database.xml(title=data[row]['section_4'])[0]['content'].replace('%ID%', str(last_messages_table_id))
    cursor.execute(
        messages_insert_query,
        message_xml,
        res_data.static['Section_ID_4'],
        messages_statuses_id,
        res_data.static['DSDMoniker_4'])
    message_4 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

    # ---------------- Messages table section 5 ---------------- #
    last_messages_table_id += 1
    message_xml = db.Database.xml(title=data[row]['section_5'])[0]['content'].replace('%ID%', str(last_messages_table_id))
    cursor.execute(
        messages_insert_query,
        message_xml,
        res_data.static['Section_ID_5'],
        messages_statuses_id,
        res_data.static['DSDMoniker_5'])
    message_5 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

    # ---------------- Messages table section 6 ---------------- #
    last_messages_table_id += 1
    message_xml = db.Database.xml(title=data[row]['section_6'])[0]['content'].replace('%ID%', str(last_messages_table_id))
    cursor.execute(
        messages_insert_query,
        message_xml,
        res_data.static['Section_ID_6'],
        messages_statuses_id,
        res_data.static['DSDMoniker_6'])
    message_6 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

    # ---------------- logs ---------------- #
    data = form_log_data(data[row]['OKPO'], user_info_id, messages_statuses_id, message_1,
                         message_2, message_3, message_4, message_5, message_6)
    log.write(data)


def form_log_data(
        okpo, user_info_id, messages_statuses_id, message_1,
        message_2, message_3, message_4, message_5, message_6
):
    log_data = """OKPO: {0}
    UserInfoId: {1}
    messages_statuses_id: {2}
    message_1: {3}
    message_2: {4}
    message_3: {5}
    message_4: {6}
    message_5: {7}
    message_6: {8}
    """.format(
        okpo,
        user_info_id,
        messages_statuses_id,
        message_1,
        message_2,
        message_3,
        message_4,
        message_5,
        message_6
    )

    log_data += '\n\n'
    return log_data
