from  mysql.connector import connect
import json
from datetime import datetime
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
                        note_name = (db_name + ' ' + str(db_time))
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


    def get_note_text(self, db_name = None, db_user_id  = 0): #хз как вернуть message
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                if ((db_name != None) and (db_user_id!= 0) ):
                    cursor.execute("SELECT message FROM notes WHERE user_id = %s AND name = %s ORDER BY date_time LIMIT 1", (db_user_id, str(db_name)))
                    message = list(cursor.fetchall())[0]
                    return message

    def get_file_id(self, db_name = None):#хз как вернуть file_id
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                if (db_name != None):
                    cursor.execute("SELECT file_id FROM files WHERE name = %s", (str(db_name), ))
                    file_id = list(cursor.fetchall())[0]
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
                    time_delta = db_notice_date - datetime.now()
                    db_time_unix = int(time_delta.total_seconds())
                    cursor.execute("INSERT INTO schedule(note_id, time_to_wait, is_regular, notice_time) VALUES (%s, %s, %s, %s)", (db_id, db_time_unix, db_is_reg, db_notice_date))
                    conn.commit()
                    print("напоминание установлено")
    def delete_notification(self, db_name = None, db_user_id = 0, db_notice_date = datetime.now()):
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                if(db_name!=None and db_user_id != 0):
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


    def print_note_info(self, db_name = None, db_user_id = 0):
        with connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password) as conn:
            with conn.cursor(buffered=True) as cursor:
                if(db_name!=None and db_user_id != 0):
                    cursor.execute("SELECT * FROM notes WHERE name = %s AND user_id = %s", (str(db_name), db_user_id))
                    info = cursor.fetchall()
                    print(info)
                else:
                   print("WILL BE ERROR")


db_conn = DB_connect()

#db_conn.add_user(12, "not_kotik", "waf", )
#db_conn.add_file(1836518, )
#db_conn.set_state(12, "beeing tired")
time = datetime(2024, 5, 2, 12, 45, 0)
print(db_conn.get_file_id("2024-05-01 19:51:13.310499"))
#db_conn.set_notification("я есть запись", 12, time, False)
#db_conn.delete_notification("я есть запись", 12, time)
#db_conn.delete_note("я есть запись", 123456)
#db_conn.add_note("я есть запись", 12, "do laba")
#db_conn.print_note_info("я есть запись", 123456)



#db_time = datetime.fromtimestamp(db_time)  # from unix to datetime


''' ADD :
 get state func'''




