import eel
import datetime
from apps_timer import AppsTimer

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


@eel.expose
def create_home_page(date = None):
    global page
    page = 1
    eel.create_globaltime(apps_timer.get_global_time())
    eel.create_appsblocks(apps_timer.get_five_apps(page=page)[0], apps_timer.get_five_apps(page=page)[1])


#чтобы работать с датой и историей
@eel.expose
def recreate_appstimer(*args):
    global apps_timer
    try:
        apps_timer = AppsTimer(args[0])
    except:
        apps_timer = AppsTimer()

#start application
def start_app():
    # eel.create_globaltime(apps_timer.get_global_time())
    # eel.create_appsblocks(apps_timer.get_five_apps(page=page)[0], apps_timer.get_five_apps(page=page)[1])
    eel.start("index.html", size=(400, 600))


if __name__ == "__main__":
    start_app()