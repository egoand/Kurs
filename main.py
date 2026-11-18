import os
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'C:\Users\Андрей\PycharmProjects\PIS_new\.venv\Lib\site-packages\PyQt5\Qt5\plugins\platforms'
import sys
from PyQt5.QtWidgets import QApplication
from factories import make_auth_service, make_task_service, make_task_repo, load_staff
from vm.login_vm import LoginVM
from vm.zav_vm import ZavVM
from vm.isp_vm import IspVM
from views.login_view import LoginView
from views.zav_view import ZavView
from views.isp_view import IspView


class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_vm = LoginVM(make_auth_service())
        self.lv = LoginView(self.login_vm, self.on_login)
        self.zv = None
        self.iv = None

    def run(self):
        self.lv.show()
        sys.exit(self.app.exec_())

    def on_login(self, user):
        task_service = make_task_service()
        task_repo = make_task_repo()
        if user["role"] == "zav":
            staff_list = load_staff()
            vm = ZavVM(task_service, staff_list)
            self.zv = ZavView(vm, staff_list)
            self.zv.show()
        else:
            vm = IspVM(user, task_service, task_repo)
            self.iv = IspView(vm)
            self.iv.show()
        self.lv.close()


if __name__ == "__main__":
    App().run()