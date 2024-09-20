import eel
from apps_timer import AppsTimer
# from apscheduler.schedulers.blocking import BlockingScheduler
from pystray import Icon, Menu, MenuItem
from PIL import Image
import os

# scheduler = BlockingScheduler()
apps_timer = AppsTimer()
page = 1
eel.init("web")


#функции для кнопок
@eel.expose
def previous_page(*args):
    global page
    page = page - 1 if page > 1 else 1
    eel.delete_blocks()
    eel.sleep(0.3)
    eel.create_appsblocks(apps_timer.get_five_apps(page)[0], apps_timer.get_five_apps(page)[1])

@eel.expose
def next_page(*args):
    global page
    page = page + 1 if page < len(apps_timer.apps_and_time)/5 else page
    eel.delete_blocks()
    eel.sleep(0.3)
    eel.create_appsblocks(apps_timer.get_five_apps(page)[0], apps_timer.get_five_apps(page)[1])


#start application
def start_app():
    eel.create_globaltime(apps_timer.get_global_time())
    eel.create_appsblocks(apps_timer.get_five_apps(page=page)[0], apps_timer.get_five_apps(page=page)[1])
    eel.start("index.html", size=(400, 600))

#трей
img = Image.open("icon.png")
icon = Icon(name="MyScreenTime", icon=img, menu=Menu(MenuItem(text="Открыть", action=start_app)))

# @scheduler.scheduled_job("interval", seconds=3)
# def check_time():
#     apps_timer.append_time()

if __name__ == "__main__":
    icon.run()