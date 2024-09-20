from time import sleep
import re
import win32gui
import sqlite3
import datetime
import json
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

class AppsTimer:

    # apps_and_time = {"wot":43, "Minecraft":999, "spotify":12, "VSCode":34, "FireFox":345,
    #                  "Dota2":1, "Word":1345,"fsdgfdh":24,"mnb":456, "444":111, "ee":765,
    #                  "jojo":21}
    apps_and_time = {}
    last_date = datetime.date.today().isoformat()


    def __init__(self) -> None:
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS data_apps (
                           date STRING NOT NULL,
                           apps STRING
                           )""")
            
            cursor.execute("""SELECT apps FROM data_apps WHERE date=?""", (self.last_date,))
            result = cursor.fetchone()
            if result != None:
                self.apps_and_time = json.loads(result[0])
                print(self.apps_and_time)
            

    
    def get_global_time(self,):
        return sum(self.apps_and_time.values())
    
    def get_five_apps(self, page:int):
        sorted_apps = sorted(self.apps_and_time.items(), key=lambda item: item[1], reverse=True)
        
        apps = [item[0] for item in sorted_apps[(page-1)*5:page*5]]
        time = [item[1] for item in sorted_apps[(page-1)*5:page*5]]
        return apps, time
    
    def __get_apptitle(self):
        w = win32gui
        app_title = w.GetWindowText(w.GetForegroundWindow())
        
        if (not "-" in app_title and not "—" in app_title and not re.findall("[(]\d+[)]",app_title) and not "Личный:" in app_title):
            return app_title
        
        if ":" in app_title:
            splited_title = app_title.split(":")[-1][1:]
            return splited_title
        elif "-" in app_title:
            splited_title = app_title.split("-")
            return splited_title[-1][1:]
        elif "—" in app_title:
            splited_title = app_title.split("—")
            return splited_title[-1][1:]
        elif re.findall("[(]\d+[)]", app_title):
            return "Telegram"
    
    def update_db(self, date, apps):
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            cursor.execute("""SELECT date, apps FROM data_apps WHERE date=?""", (date,))
            result = cursor.fetchone()
            if result != None:
                cursor.execute("""UPDATE data_apps SET apps = ? WHERE date = ?""", (apps, date,))
                return
            
            cursor.execute("""INSERT INTO data_apps VALUES (?,?)""", (date,apps,))

    
    def append_time(self):
        if self.last_date != datetime.date.today().isoformat():
            self.apps_and_time.clear()
        app = self.__get_apptitle()
        if app == "":
            return
        self.apps_and_time[app] = self.apps_and_time.get(app, 0) + 1
        date = datetime.date.today().isoformat()
        self.update_db(date=date, apps=json.dumps(self.apps_and_time))
        print(app)

apps_timer = AppsTimer()


@scheduler.scheduled_job("interval", seconds=3)
def main():
    apps_timer.append_time()


if __name__ == "__main__":
    scheduler.start()

        

    