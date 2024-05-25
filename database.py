from  mysql.connector import connect
import json
from datetime import datetime, timedelta
import re
import time
class DB_connect():
    def __init__(self):
        with open(".database_config.json", "r") as jf:
            json_setting = json.loads(jf.read())
            self.db_host = json_setting["host"]
            self.db_name = json_setting["database"]
            self.db_user = json_setting["user"]
            self.db_password = json_setting["password"]
            # self.db_port = json_setting["port"]

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def add_note(self,db_name = None, db_user_id = 0, db_message = None): # db_time has to be unix
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                db_time = datetime.now()
                if (db_user_id != 0 and db_message!=None and db_time!=0):
                    cursor.execute("SELECT name FROM notes WHERE user_id = %s", (db_user_id, ))
                    namelist = [list(el)[0] for el in cursor.fetchall()]
                    note_name = ""
                    if (db_name==None):
                        note_name = str(db_time)
                    elif (db_name in namelist):
                        note_name = (db_name + ' ' + db_time.strftime("%d/%m/%Y %H:%M:%S"))
                    else:
                        note_name = db_name

                    cursor.execute("INSERT INTO notes(name, user_id, message, date_time) VALUES (%s, %s, %s, %s)",(str(note_name), db_user_id, db_message, db_time))
                    conn.commit()
                    print("заметка добавлена")
                else:
                    print("WILL BE ERROR")
    def add_user(self, db_user_id = 0, db_username = None, db_first_name = None, db_last_name = None):
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                cursor.execute("SELECT tg_id FROM users WHERE tg_id = %s", (db_user_id, ))
                user = cursor.fetchall()
                if(user):
                    return None
                if (db_user_id != 0 and isinstance(db_user_id, int) and db_user_id != None):
                    cursor.execute("INSERT INTO users(tg_id, username, first_name, last_name) VALUES (%s, %s, %s, %s)", (db_user_id, str(db_username), str(db_first_name), str(db_last_name)))
                    conn.commit()
                    cursor.execute("INSERT INTO states(user_id) VALUES (%s)", (db_user_id, ))
                    conn.commit()
                    print("пользователь добавлен")
                else:
                    print("WILL BE ERROR")
    def add_file(self, db_file_id = 0, db_file_name = None): # db_time has to be unix
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                if (db_file_id != 0):
                    db_time = datetime.now()
                    note_name = ""
                    if (db_file_name == None):
                        note_name = str(db_time)
                    else:
                        note_name = db_file_name

                    cursor.execute("INSERT INTO files(file_id, name, date_time) VALUES (%s, %s, %s)", (db_file_id, str(note_name), db_time))
                    conn.commit()
                    print("файл добавлен")


    # def get_note_text(self, db_name = None, db_user_id  = 0): #хз как вернуть message
    #     with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
    #         with conn.cursor(buffered=True) as cursor:
    #             if ((db_name != None) and (db_user_id!= 0) ):
    #                 cursor.execute("SELECT message FROM notes WHERE user_id = %s AND name = %s ORDER BY date_time LIMIT 1", (db_user_id, str(db_name)))
    #                 message = cursor.fetchall()[0][0]
    #                 return message

    def get_file_id(self, db_name = None):#хз как вернуть file_id
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                if (db_name != None):
                    cursor.execute("SELECT file_id FROM files WHERE name = %s", (str(db_name),))
                    file_id = cursor.fetchall()[0][0]
                    return file_id

    def set_state(self, db_user_id = 0, state = None):
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                if (db_user_id != 0 and state != None and ("ing" in state), (str(state))):
                    cursor.execute("UPDATE states SET state = %s WHERE user_id = %s",(str(state), db_user_id))
                    conn.commit()
                    print("статус установлен")
    def get_state(self, db_id_user = 0):
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                if (db_id_user != 0):
                    cursor.execute("SELECT state FROM states WHERE user_id = %s", (db_id_user, ))
                    return cursor.fetchall()[0][0]
    def set_notification(self,db_name = None, db_user_id = 0, db_notice_date = datetime.now(), db_is_reg = False): #datetime notice_date
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                if(db_name!=None and db_notice_date > datetime.now()):
                    cursor.execute("SELECT id FROM notes WHERE user_id = %s AND name = %s", (db_user_id, str(db_name))) # get note_id by name
                    db_id = cursor.fetchall()[0][0] #note_id
                    db_time_now = datetime.now()
                    time_delta = db_notice_date - datetime.now()
                    db_time_unix = int(time_delta.total_seconds())
                    cursor.execute("INSERT INTO schedule(note_id, time_to_wait, is_regular, notice_time, time_added) VALUES (%s, %s, %s, %s, %s)", (db_id, db_time_unix, db_is_reg, db_notice_date, db_time_now))
                    conn.commit()
                    print("напоминание установлено")
    def delete_notification(self, db_name = None, db_user_id = 0, db_notice_date = datetime.now()):
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                if(db_notice_date == datetime.now()):
                    cursor.execute("SELECT id from notes WHERE user_id = %s AND name = %s", (db_user_id, str(db_name)))
                    db_id = cursor.fetchall()
                    for i in range (len(db_id)-1):
                        cursor.execute("DELETE * FROM schedule WHERE note_id = %s",(db_id, ))
                        conn.commit()
                elif(db_name!=None and db_user_id != 0):
                    cursor.execute("SELECT id from notes WHERE user_id = %s AND name = %s", (db_user_id, str(db_name)))
                    db_id = cursor.fetchall()[0][0]
                    cursor.execute("DELETE FROM schedule WHERE note_id = %s AND notice_time = %s", (db_id, db_notice_date))
                    conn.commit()
                    print("напоминание удалено")
    def delete_note(self, db_name = None, db_user_id = 0):
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                if(db_name!=None and db_user_id != 0):
                    cursor.execute("DELETE FROM notes WHERE name = %s AND user_id = %s", (str(db_name), db_user_id))
                    conn.commit()
                    print("заметка удалена")

    def get_note_text(self, db_to_find = None, db_user_id = 0):
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                if(db_to_find!=None and db_user_id != 0):
                    messages = []
                    db_to_find = db_to_find.replace(',', '').replace('.', '')
                    words = re.sub(r"[,\.-]", "", db_to_find).split(" ")

                    query_string = "(" + "|".join(words) + ")"

                    cursor.execute("SELECT name, message FROM notes WHERE name REGEXP %s", (query_string,))

                    info = cursor.fetchall()
                    for i in range (len(info)):
                        messages.append((info[i][0], info[i][1]))
                    return messages
                else:
                    print("WILL BE ERROR")

    def get_schedule_for_today(self, db_user_id = 0):
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                if(db_user_id != 0):
                    db_date_today = datetime.now().date()
                    schedule = {}
                    cursor.execute("SELECT schedule.notice_time, notes.message FROM (schedule LEFT JOIN notes ON schedule.note_id = notes.id) WHERE DATE(schedule.notice_time) = %s AND notes.user_id = %s ORDER BY schedule.notice_time",(db_date_today, db_user_id))
                    info = cursor.fetchall()
                    print(info)
                    for i in range (len(info) - 1):
                        schedule[info[i][0].strftime("%H:%M:%S")] = info[i][1]
                    return schedule
                else:
                    print("WILL BE ERROR")

    def get_schedule_for_tomorrow(self, db_user_id = 0):
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                if(db_user_id != 0):
                    db_date_tomorrow = (datetime.now().date() + timedelta(days=1))
                    schedule = {}
                    cursor.execute("SELECT schedule.notice_time, notes.message FROM (schedule LEFT JOIN notes ON schedule.note_id = notes.id) WHERE DATE(schedule.notice_time) = %s AND notes.user_id = %s ORDER BY schedule.notice_time",(db_date_tomorrow, db_user_id))
                    info = cursor.fetchall()
                    print(info)
                    for i in range (len(info) - 1):
                        schedule[info[i][0].strftime("%H:%M:%S")] = info[i][1]
                    return schedule
                else:
                    print("WILL BE ERROR")

    def check_notification(self):
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                db_time = datetime.now()
                cursor.execute("SELECT notes.user_id, notes.message, schedule. is_regular, notes.name, schedule.notice_time FROM schedule LEFT JOIN notes ON schedule.note_id = notes.id WHERE DATE(schedule.notice_time) < NOW()")
                passed = []
                info = cursor.fetchall()
                regularity = []
                for i in range(len(info)):
                    passed.append((info[i][0], info[i][1]))
                    regularity.append((info[i][2], info[i][3], info[i][4]))
                for i in range (len(info) - 1):
                    if (regularity[i][0] == 0):
                        self.delete_notification(regularity[i][1], passed[i][0], regularity[i][2])
                    else:
                        cursor.execute("SELECT id FROM notes WHERE user_id = %s AND name = %s",(passed[i][0], str(regularity[i][1])))  # get note_id by name
                        db_id = cursor.fetchall()[0][0]  # note_id
                        regularity[i][2] += timedelta(days=1)
                        delta = regularity[i][2] - datetime.now()
                        db_time_unix = int(delta.total_seconds())
                        cursor.execute("UPDATE schedule SET time_to_wait = %s, notice_time = %s WHERE note_id = %s", (db_time_unix, regularity[i][2], db_id))
                        conn.commit()
                        print("Новое напоминание установлено")

                return passed
    def is_regular(self, db_user_id = 0):
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                if(db_user_id != 0):
                    cursor.execute("SELECT schedule.is_regular FROM (schedule LEFT JOIN notes ON schedule.note_id = notes.id) WHERE notes.user_id = %s", (db_user_id, ))
                    reg = cursor.fetchall()[0]
                    return reg

    def get_list(self, db_user_id = 0):
        with connect(host=self.db_host, database=self.db_name, user=self.db_user,password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                if (db_user_id != 0):
                    cursor.execute("SELECT name FROM notes WHERE user_id = %s", (db_user_id,))
                    temp = cursor.fetchall()
                    list1 = []
                    for i in range(len(temp) - 1):
                        list1.append(temp[i][0])
                    return list1


# #
# time = datetime(2024, 5, 25, 23, 36, 0)
# db_conn = DB_connect()


