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
        cursor.execute("INSERT INTO UsersInfo(OKPO, User_ID) VALUES (?, ?)", data[row]['OKPO'], data[row]['User_ID'])
        UserInfo_ID = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

        cursor.execute(
            "INSERT INTO MessagesStatuses(Form_ID, UsersInfo_ID, PeriodType, DepartmentType, DateTime) VALUES (?, ?, ?, ?, ?)",
            static['Form_ID'], UserInfo_ID, static['PeriodType'], data[row]['DepartmentType'], static['Datetime']
        )
        MessagesStatuses_ID = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

        cursor.execute(
            "INSERT INTO RespondentDatas(MessageStatusID, SoateCode) values(?, ?)",
            MessagesStatuses_ID, data[row]['SOATE']
        )

        Message_XML = db.xml(title=data[row]['section_1'])[0]['content']
        cursor.execute(
            "INSERT INTO Messages(Message_XML, Section_ID, MessagesStatuses_ID, DSDMoniker) VALUES (?, ?, ?, ?)",
            Message_XML, static['Section_ID_1'], MessagesStatuses_ID, static['DSDMoniker_1']
        )
        Message_1 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

        Message_XML = db.xml(title=data[row]['section_2'])[0]['content']
        cursor.execute(
            "INSERT INTO Messages(Message_XML, Section_ID, MessagesStatuses_ID, DSDMoniker) VALUES (?, ?, ?, ?)",
            Message_XML, static['Section_ID_2'], MessagesStatuses_ID, static['DSDMoniker_2']
        )
        Message_2 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

        Message_XML = db.xml(title=data[row]['section_3'])[0]['content']
        cursor.execute(
            "INSERT INTO Messages(Message_XML, Section_ID, MessagesStatuses_ID, DSDMoniker) VALUES (?, ?, ?, ?)",
            Message_XML, static['Section_ID_3'], MessagesStatuses_ID, static['DSDMoniker_3']
        )
        Message_3 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

        Message_XML = db.xml(title=data[row]['section_4'])[0]['content']
        cursor.execute(
            "INSERT INTO Messages(Message_XML, Section_ID, MessagesStatuses_ID, DSDMoniker) VALUES (?, ?, ?, ?)",
            Message_XML, static['Section_ID_4'], MessagesStatuses_ID, static['DSDMoniker_4']
        )
        Message_4 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

        Message_XML = db.xml(title=data[row]['section_5'])[0]['content']
        cursor.execute(
            "INSERT INTO Messages(Message_XML, Section_ID, MessagesStatuses_ID, DSDMoniker) VALUES (?, ?, ?, ?)",
            Message_XML, static['Section_ID_5'], MessagesStatuses_ID, static['DSDMoniker_5']
        )
        Message_5 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

        Message_XML = db.xml(title=data[row]['section_6'])[0]['content']
        cursor.execute(
            "INSERT INTO Messages(Message_XML, Section_ID, MessagesStatuses_ID, DSDMoniker) VALUES (?, ?, ?, ?)",
            Message_XML, static['Section_ID_6'], MessagesStatuses_ID, static['DSDMoniker_6']
        )
        Message_6 = cursor.execute("SELECT @@IDENTITY AS id").fetchone()[0]

        log.write('OKPO: {0}\nUserInfoId: {1}\nMessagesStatuses_ID: {2}\nMessage_1: {3}\nMessage_2: {4}\nMessage_3: {5}\nMessage_4: {6}\nMessage_5: {7}\nMessage_6: {8}\n\n'.format(
            data[row]['OKPO'], UserInfo_ID, MessagesStatuses_ID, Message_1, Message_2, Message_3, Message_4, Message_5, Message_6))
    except pyodbc.Error:
        missed += 1
        connection.rollback()

    connection.commit()
    iteration += 1
    print_progress(iteration, total)

log.close()

connection.close()

print("\n%d" % missed)
