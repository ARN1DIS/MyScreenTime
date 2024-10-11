import os
import getpass
import shutil
from win32com.client import Dispatch
from win32com.shell import shell
from colorama import Fore



class Installer:

    def __init__(self, parametrs: dict):
        self.parametrs = parametrs
        self.user_name = getpass.getuser()
        self.program_files =  r"C:\Program Files\ScreenTime"
        self.app_path = r"\app\ScreenTime.exe"
        self.apps_timer_path = r"\app\apps_timer.exe"
        self.desktop = rf"C:\Users\{self.user_name}\Desktop"
        self.current_dir = os.getcwd()
        self.pr_app_path = self.program_files + r"\ScreenTime.exe"
        self.pr_apps_timer_path = self.program_files + r"\apps_timer.exe"
        self.mainmenu = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
        self.autorun = rf"C:\Users\{self.user_name}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
        self.create_folder_in_pr()
    

    def create_folder_in_pr(self):
        try:
            try:    
                os.mkdir(self.program_files)    
                shutil.copy2(src=self.current_dir + self.app_path, dst=self.program_files)
                shutil.copy2(src=self.current_dir + self.apps_timer_path, dst=self.program_files)
            except FileExistsError:
                shutil.copy2(src=self.current_dir + self.app_path, dst=self.program_files)
                shutil.copy2(src=self.current_dir + self.apps_timer_path, dst=self.program_files)

            print(Fore.GREEN + "[+] Рабочая директория создана")
        except:
            print(Fore.RED + "[-] Рабочая директория не создана")

    
    def create_shortcut(self, program_path: str, path_to_shct: str):
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path_to_shct+".lnk")
            shortcut.Targetpath = program_path
            shortcut.save()


    def create_on_desktop(self):
        try:
            self.create_shortcut(program_path=self.pr_app_path, path_to_shct=self.desktop + "\ScreenTime")
            print(Fore.GREEN + "[+] Ярлык на рабочем столе создан")
        except:
            print(Fore.RED + "[-] Ярлык на рабочем столе не создан")


    def create_on_mainmenu(self):
        try:
            self.create_shortcut(program_path=self.pr_app_path, path_to_shct=self.mainmenu + "\ScreenTime")
            print(Fore.GREEN + "[+] Ярлык в меню создан")
        except:
            print(Fore.RED + "[-] Ярлык в главном меню не создан")


    def add_to_autorun(self):
        try:
            self.create_shortcut(program_path=self.pr_apps_timer_path, path_to_shct=self.autorun + r"\appstimer")
            print(Fore.GREEN + "[+] Приложение добавлено в автозагрузку")
        except:
            print(Fore.RED + "[-] Приложение не добавлено в автозагрузку")


    def reboot(self):
        os.system("shutdown /r /t 0")


    @staticmethod
    def check_admin() -> bool:
        if shell.IsUserAnAdmin():
            return True
        else:
            return False
    

    def install(self):
        self.add_to_autorun()
        if self.parametrs.get("mainmenu") == "y":
            self.create_on_mainmenu()
        if self.parametrs.get("desktop") == "y":
            self.create_on_desktop()


def main():
    isAdmin = Installer.check_admin()
    if isAdmin == True:
        print(Fore.YELLOW + "Любой символ кроме y или n, будет учитан как n" + Fore.WHITE)
        print("Создать ярлык на рабочем столе? (y/n)")
        is_desktop = input("")
        print("Создать ярлык в главном меню? (y/n)")
        is_mainmenu = input("")
        parametrs = {"mainmenu":is_mainmenu, "desktop":is_desktop}
        installer = Installer(parametrs=parametrs)
        installer.install()

        print("Приложение запуститься после перезагрузки ПК. Перезапустить сейчас? (y/n)")
        is_reload = input()
        if is_reload == "y":
            installer.reboot()
        print("Спасибо за установку ScreenTime <3")
    else:
        print(Fore.RED + "Запустите установщик от имени администратора, иначе установка невозможна")




if __name__ == "__main__":
    main()