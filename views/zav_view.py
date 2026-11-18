from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QMessageBox as MB,
                             QInputDialog)
from PyQt5.QtCore import Qt, QDate
from datetime import date, timedelta
from vm.zav_vm import ZavVM
from models.status import get_status
from ui.ui_zav import Ui_MainWindow
from styles import ZAV_QSS
from widgets.collapsible_card import CollapsibleCard
from widgets.assign_dialog import AssignDialog


FILTERS = [("all", "Все"), ("pending", "Ожидает оценки"), ("evaluated", "Оценена"),
           ("assigned", "Назначена"), ("in_progress", "В процессе"),
           ("completed", "Выполнена"), ("archived", "Архив")]


class ZavView(QMainWindow):
    def __init__(self, vm: ZavVM, staff_list):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet(ZAV_QSS)
        self.vm = vm
        self.staff_list = staff_list
        self.setWindowTitle("История работ · Заведующий кафедрой")

        self.ui.tabs.setDocumentMode(True)
        self.ui.tabs.tabBar().setExpanding(False)
        self.ui.tabs.tabBar().setUsesScrollButtons(False)
        self.ui.tabs.tabBar().setElideMode(Qt.ElideNone)

        self.fbtns = {}
        for k, t in FILTERS:
            b = QPushButton(t)
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _, x=k: self.set_filter(x))
            self.ui.fbar.addWidget(b)
            self.fbtns[k] = b
        self.ui.fbar.addStretch()

        self.ui.sortBtn.clicked.connect(self.toggle_sort)
        self.ui.refreshBtn.clicked.connect(self.reset)
        self.ui.qEdit.returnPressed.connect(self.do_search)
        self.ui.firstBtn.clicked.connect(lambda: self.nav(0))
        self.ui.prevBtn.clicked.connect(lambda: self.nav(-1))
        self.ui.nextBtn.clicked.connect(lambda: self.nav(1))
        self.ui.lastBtn.clicked.connect(lambda: self.nav(2))
        self.ui.newCreate.clicked.connect(self.create)
        self.ui.newEv.valueChanged.connect(self.recalc_dates)
        self.ui.tabs.currentChanged.connect(self.on_tab)

        self.upd_filter_buttons()
        self.recalc_dates()
        self.refresh()

    def upd_filter_buttons(self):
        for k, b in self.fbtns.items():
            active = (k == self.vm.filter.status)
            b.setStyleSheet(
                "background:#b33f3f; color:white; border:1px solid #b33f3f;"
                if active else
                "background:white; color:#3d2e2e; border:1px solid #d4c5c5;"
            )

    def set_filter(self, key):
        self.vm.filter.status = key
        self.vm.paginator.page = 1
        self.upd_filter_buttons()
        self.refresh()

    def toggle_sort(self):
        self.vm.filter.ascending = not self.vm.filter.ascending
        self.ui.sortBtn.setText("По дате ▲" if self.vm.filter.ascending else "По дате ▼")
        self.ui.sortBtn.setStyleSheet(
            "background:#b33f3f; color:white; border:1px solid #b33f3f;" if self.vm.filter.ascending
            else "background:#fdf5f5; color:#3d2e2e; border:1px solid #d4c5c5;")
        self.refresh()

    def reset(self):
        self.vm.filter.status = "all"
        self.vm.filter.ascending = False
        self.vm.filter.query = ""
        self.vm.paginator.page = 1
        self.ui.qEdit.clear()
        self.ui.sortBtn.setText("По дате ▼")
        self.ui.sortBtn.setStyleSheet("")
        self.upd_filter_buttons()
        self.refresh()

    def do_search(self):
        self.vm.filter.query = self.ui.qEdit.text().strip()
        self.vm.paginator.page = 1
        self.refresh()

    def nav(self, action):
        self.vm.paginator.page = {0: 1, 2: 99999}.get(
            action, max(1, self.vm.paginator.page + action))
        self.refresh()

    def recalc_dates(self):
        ev = self.ui.newEv.value()
        min_start = date.today() + timedelta(days=ev)
        qmin = QDate(min_start.year, min_start.month, min_start.day)
        self.ui.newSd.setMinimumDate(qmin)
        self.ui.newSd.setDate(qmin)
        end = min_start + timedelta(days=7)
        self.ui.newEd.setMinimumDate(qmin)
        self.ui.newEd.setDate(QDate(end.year, end.month, end.day))

    def refresh(self):
        tasks, total_pages = self.vm.refresh()
        self.ui.pageLbl.setText(f"{self.vm.paginator.page} / {total_pages}")
        w = QWidget()
        wl = QVBoxLayout(w)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.setSpacing(12)
        for t in tasks:
            wl.addWidget(self.card(t))
        if not tasks:
            lb = QLabel("Нет задач по выбранному фильтру")
            lb.setAlignment(Qt.AlignCenter)
            lb.setStyleSheet("color:#9e7a7a; padding:40px; font-size:13px;")
            wl.addWidget(lb)
        wl.addStretch()
        self.ui.histScroll.setWidget(w)

    def card(self, task):
        meta = get_status(task.status)
        c = CollapsibleCard(task.title, meta.label, f"badge_{meta.badge}", task.meta_text())

        desc = QLabel(task.description)
        desc.setObjectName("desc")
        desc.setTextFormat(Qt.PlainText)
        desc.setWordWrap(True)
        c.add_detail(desc)

        avg = task.average_score()
        if task.status == "pending" and task.ratings and date.today() <= task.eval_deadline:
            box = QLabel(f"Сбор оценок до {task.eval_deadline.strftime('%d.%m.%Y')} · Средняя: {avg} баллов | " +
                         ", ".join(f"{x['name']}: {x['score']}" for x in task.ratings))
            box.setObjectName("collectBox")
            box.setWordWrap(True)
            c.add_detail(box)
        elif task.ratings:
            box = QLabel(f"Средняя оценка: {avg} баллов | " +
                         ", ".join(f"{x['name']}: {x['score']}" for x in task.ratings))
            box.setObjectName("ratingBox")
            box.setWordWrap(True)
            c.add_detail(box)

        row = QHBoxLayout()
        row.setSpacing(8)
        if task.status == "evaluated":
            b1 = QPushButton("Назначить сотрудников")
            b1.setCursor(Qt.PointingHandCursor)
            b1.clicked.connect(lambda _, x=task: self.assign(x))
            row.addWidget(b1)
            row.addWidget(self._danger_btn("Удалить", lambda: self.rm(task)))
        elif task.status == "assigned":
            b = QPushButton("Заменить исполнителей")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _, x=task: self.assign(x))
            row.addWidget(b)
            b2 = QPushButton("Редактировать")
            b2.setCursor(Qt.PointingHandCursor)
            b2.clicked.connect(lambda _, x=task: self.edit(x))
            row.addWidget(b2)
            row.addWidget(self._danger_btn("Удалить", lambda: self.rm(task)))
        elif task.status == "in_progress":
            b2 = QPushButton("Редактировать")
            b2.setCursor(Qt.PointingHandCursor)
            b2.clicked.connect(lambda _, x=task: self.edit(x))
            row.addWidget(b2)
            row.addWidget(self._danger_btn("Удалить", lambda: self.rm(task)))
        elif task.status == "completed":
            b = QPushButton("В архив")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _, x=task: (self.vm.archive(x), self.refresh()))
            row.addWidget(b)
        elif task.status == "pending":
            row.addWidget(self._danger_btn("Удалить", lambda: self.rm(task)))
        elif task.status == "archived":
            b = QPushButton("Создать заново")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _, x=task: self.recreate(x))
            row.addWidget(b)
        if row.count():
            row.addStretch()
            c.add_detail_layout(row)
        return c

    def _danger_btn(self, text, callback):
        b = QPushButton(text)
        b.setCursor(Qt.PointingHandCursor)
        b.setProperty("danger", "true")
        b.clicked.connect(lambda: callback())
        return b

    def rm(self, task):
        if MB.question(self, "Удалить", f'Удалить "{task.title}"?') == MB.Yes:
            self.vm.delete(task)
            self.refresh()

    def recreate(self, task):
        self.ui.tabs.setCurrentIndex(1)
        self.ui.newTitle.setText(task.title)
        self.ui.newDesc.setPlainText(task.description)
        self.ui.newEv.setValue(task.eval_days)
        self.recalc_dates()

    def assign(self, task):
        d = AssignDialog(task, self.staff_list, self.vm.rating_map(), task.average_score(), self)
        if d.exec_() == d.Accepted:
            self.vm.assign(task, d.selected_names())
            self.refresh()

    def edit(self, task):
        val, ok = QInputDialog.getText(self, "Редактировать", "Исполнители:", text=task.performers)
        if ok:
            self.vm.edit_performers(task, val)
            self.refresh()

    def create(self):
        err = self.vm.create(
            self.ui.newTitle.text().strip(),
            self.ui.newDesc.toPlainText().strip(),
            self.ui.newEv.value(),
            self.ui.newSd.date().toPyDate(),
            self.ui.newEd.date().toPyDate(),
        )
        if err:
            MB.warning(self, "Ошибка", err)
            return
        MB.information(self, "Готово", "Работа создана")
        self.ui.tabs.setCurrentIndex(0)
        self.refresh()

    def on_tab(self, i):
        if i == 0:
            self.refresh()