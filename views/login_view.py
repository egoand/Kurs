from PyQt5.QtWidgets import QWidget, QMessageBox
from vm.login_vm import LoginVM
from ui.ui_login import Ui_Form
from styles import LOGIN_QSS


class LoginView(QWidget):
    def __init__(self, vm: LoginVM, on_ok):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setStyleSheet(LOGIN_QSS)
        self.vm = vm
        self.on_ok = on_ok
        self.setWindowTitle("Вход в систему")
        self.ui.loginBtn.clicked.connect(self.do)
        self.ui.lgEdit.returnPressed.connect(self.do)
        self.ui.pwEdit.returnPressed.connect(self.do)

    def do(self):
        user, err = self.vm.login(self.ui.lgEdit.text(), self.ui.pwEdit.text())
        if err:
            QMessageBox.warning(self, "Ошибка", err)
            return
        self.on_ok(user)