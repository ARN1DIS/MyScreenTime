import sqlite3
import json
import eel
import getpass

class History:
    # last_days = {}

    def __init__(self):
        pass

    @eel.expose
    @staticmethod
    def get_last_days(count:int = 5):
        dir = fr"C:\Users\{getpass.getuser()}\Documents\ScreenTime_data"
        with sqlite3.connect(fr"{dir}\database.db") as db:
            cursor = db.cursor()
            cursor.execute("""SELECT date, apps FROM data_apps ORDER BY rowid DESC LIMIT ? """,(count,))
            result = cursor.fetchall()
            if result == None:
                return None
            new_dict = {k:sum(json.loads(v).values()) for k,v in result}
            return list(new_dict.keys()), list(new_dict.values())
    
    @eel.expose
    def call_history(*args):
        gld = History.get_last_days()
        eel.days_time(gld[0], gld[1])



