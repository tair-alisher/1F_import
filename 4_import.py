import pyodbc

from sources.serv import print_progress

from results.data import data
from results.data import static

import sources.connection_strings as con_strings

import sources.db as db

connection = pyodbc.connect(con_strings.clone)
cursor = connection.cursor()

log = open('logs\\log.txt', 'w')

iteration = 0
total = len(data)

missed = 0

for row in data:
    try:
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
        UserInfo_ID = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

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
            static['Form_ID'],
            UserInfo_ID,
            static['PeriodType'],
            data[row]['DepartmentType'],
            static['Datetime'])
        MessagesStatuses_ID = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

        # ---------------- RespondentDatas table ---------------- #
        respondent_datas_insert_query = """
        INSERT INTO RespondentDatas(
            MessageStatusID,
            SoateCode)
        VALUES(?, ?)
        """
        cursor.execute(
            respondent_datas_insert_query,
            MessagesStatuses_ID,
            data[row]['SOATE'])

        # ---------------- Messages table section 1 ---------------- #
        last_messages_table_id = cursor.execute("Select IDENT_CURRENT('Messages')").fetchone()[0]
        last_messages_table_id += 1
        Message_XML = db.xml(title=data[row]['section_1'])[0]['content'].replace('%ID%', str(last_messages_table_id))
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
            Message_XML,
            static['Section_ID_1'],
            MessagesStatuses_ID,
            static['DSDMoniker_1'])
        Message_1 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

        # ---------------- Messages table section 2 ---------------- #
        last_messages_table_id += 1
        Message_XML = db.xml(title=data[row]['section_2'])[0]['content'].replace('%ID%', str(last_messages_table_id))
        cursor.execute(
            messages_insert_query,
            Message_XML,
            static['Section_ID_2'],
            MessagesStatuses_ID,
            static['DSDMoniker_2'])
        Message_2 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

        # ---------------- Messages table section 3 ---------------- #
        last_messages_table_id += 1
        Message_XML = db.xml(title=data[row]['section_3'])[0]['content'].replace('%ID%', str(last_messages_table_id))
        cursor.execute(
            messages_insert_query,
            Message_XML,
            static['Section_ID_3'],
            MessagesStatuses_ID,
            static['DSDMoniker_3']
        )
        Message_3 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

        # ---------------- Messages table section 4 ---------------- #
        last_messages_table_id += 1
        Message_XML = db.xml(title=data[row]['section_4'])[0]['content'].replace('%ID%', str(last_messages_table_id))
        cursor.execute(
            messages_insert_query,
            Message_XML,
            static['Section_ID_4'],
            MessagesStatuses_ID,
            static['DSDMoniker_4'])
        Message_4 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

        # ---------------- Messages table section 5 ---------------- #
        last_messages_table_id += 1
        Message_XML = db.xml(title=data[row]['section_5'])[0]['content'].replace('%ID%', str(last_messages_table_id))
        cursor.execute(
            messages_insert_query,
            Message_XML,
            static['Section_ID_5'],
            MessagesStatuses_ID,
            static['DSDMoniker_5'])
        Message_5 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

        # ---------------- Messages table section 6 ---------------- #
        last_messages_table_id += 1
        Message_XML = db.xml(title=data[row]['section_6'])[0]['content'].replace('%ID%', str(last_messages_table_id))
        cursor.execute(
            messages_insert_query,
            Message_XML,
            static['Section_ID_6'],
            MessagesStatuses_ID,
            static['DSDMoniker_6'])
        Message_6 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

        # ---------------- logs ---------------- #
        log_data = """
        OKPO: {0}
        UserInfoId: {1}
        MessagesStatuses_ID: {2}
        Message_1: {3}
        Message_2: {4}
        Message_3: {5}
        Message_4: {6}
        Message_5: {7}
        Message_6: {8}


        """

        log.write(
            log_data.format(
                data[row]['OKPO'],
                UserInfo_ID,
                MessagesStatuses_ID,
                Message_1,
                Message_2,
                Message_3,
                Message_4,
                Message_5,
                Message_6
            )
        )
    except pyodbc.Error as err:
        print('\n')
        print(err)
        missed += 1
        connection.rollback()

    connection.commit()
    iteration += 1
    print_progress(iteration, total)

log.close()

connection.close()

print("\nmissed: %d" % missed)
