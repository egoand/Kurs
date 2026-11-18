from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QMessageBox, QSpinBox)
from PyQt5.QtCore import Qt
from datetime import date
from vm.isp_vm import IspVM
from models.status import get_status
from ui.ui_isp import Ui_MainWindow
from styles import ISP_QSS
from widgets.collapsible_card import CollapsibleCard


FILTERS = [("all", "Все"), ("pending", "Ожидает оценки"), ("evaluated", "Оценена"),
           ("assigned", "Назначена"), ("in_progress", "В процессе"),
           ("completed", "Выполнена"), ("archived", "Архив")]


class IspView(QMainWindow):
    def __init__(self, vm: IspVM):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet(ISP_QSS)
        self.vm = vm
        self.setWindowTitle("Исполнитель · Панель работ")

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
        self.ui.mySortBtn.clicked.connect(self.toggle_sort)
        self.ui.myRefreshBtn.clicked.connect(self.reset)
        self.ui.myQEdit.returnPressed.connect(self.do_search)
        self.ui.firstBtn.clicked.connect(lambda: self.nav(0))
        self.ui.prevBtn.clicked.connect(lambda: self.nav(-1))
        self.ui.nextBtn.clicked.connect(lambda: self.nav(1))
        self.ui.lastBtn.clicked.connect(lambda: self.nav(2))
        self.ui.tabs.currentChanged.connect(self.on_tab)

        self.upd_filter_buttons()
        self.refresh_history()

    def upd_filter_buttons(self):
        for k, b in self.fbtns.items():
            active = (k == self.vm.filter.status)
            b.setStyleSheet(
                "background:#1e3a6f; color:white; border:1px solid #1e3a6f;"
                if active else
                "background:white; color:#1e293b; border:1px solid #cbd5e1;"
            )

    def set_filter(self, key):
        self.vm.filter.status = key
        self.vm.paginator.page = 1
        self.upd_filter_buttons()
        self.on_tab(self.ui.tabs.currentIndex())

    def toggle_sort(self):
        self.vm.filter.ascending = not self.vm.filter.ascending
        txt = "По дате ▲" if self.vm.filter.ascending else "По дате ▼"
        self.ui.sortBtn.setText(txt)
        self.ui.mySortBtn.setText(txt)
        st = ("background:#1e3a6f; color:white; border:1px solid #1e3a6f;" if self.vm.filter.ascending
              else "background:#f1f5f9; color:#1e293b; border:1px solid #cbd5e1;")
        self.ui.sortBtn.setStyleSheet(st)
        self.ui.mySortBtn.setStyleSheet(st)
        self.on_tab(self.ui.tabs.currentIndex())

    def reset(self):
        self.vm.filter.status = "all"
        self.vm.filter.ascending = False
        self.vm.filter.query = ""
        self.vm.paginator.page = 1
        self.ui.qEdit.clear()
        self.ui.myQEdit.clear()
        self.ui.sortBtn.setText("По дате ▼")
        self.ui.mySortBtn.setText("По дате ▼")
        self.ui.sortBtn.setStyleSheet("")
        self.ui.mySortBtn.setStyleSheet("")
        self.upd_filter_buttons()
        self.on_tab(self.ui.tabs.currentIndex())

    def do_search(self):
        if self.ui.tabs.currentIndex() == 0:
            self.vm.filter.query = self.ui.qEdit.text().strip()
        else:
            self.vm.filter.query = self.ui.myQEdit.text().strip()
        self.vm.paginator.page = 1
        self.on_tab(self.ui.tabs.currentIndex())

    def nav(self, action):
        self.vm.paginator.page = {0: 1, 2: 99999}.get(
            action, max(1, self.vm.paginator.page + action))
        self.on_tab(self.ui.tabs.currentIndex())

    def refresh_history(self):
        tasks, total_pages = self.vm.refresh_history()
        self.ui.pageLbl.setText(f"{self.vm.paginator.page} / {total_pages}")
        w = QWidget()
        wl = QVBoxLayout(w)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.setSpacing(12)
        for t in tasks:
            wl.addWidget(self.card(t, mine=False))
        if not tasks:
            lb = QLabel("Нет задач по выбранному фильтру")
            lb.setAlignment(Qt.AlignCenter)
            lb.setStyleSheet("color:#6c86a3; padding:40px; font-size:13px;")
            wl.addWidget(lb)
        wl.addStretch()
        self.ui.histScroll.setWidget(w)

    def refresh_my(self):
        self.ui.myQEdit.blockSignals(True)
        self.ui.myQEdit.setText(self.vm.filter.query)
        self.ui.myQEdit.blockSignals(False)

        tasks, total_pages = self.vm.refresh_my()
        self.ui.pageLbl.setText(f"{self.vm.paginator.page} / {total_pages}")
        my = self.vm.my_tasks()
        active = sum(1 for t in my if t.status in ("assigned", "in_progress"))
        done = sum(1 for t in my if t.status == "completed")
        rated = sum(1 for t in my if t.status == "evaluated")

        name = self.vm.user["name"]
        initials = "".join(w[0] for w in name.split() if w)[:2].upper()

        head = QFrame()
        head.setObjectName("myHeader")
        hl = QHBoxLayout(head)
        hl.setContentsMargins(18, 14, 18, 14)
        hl.setSpacing(16)
        av = QLabel(initials)
        av.setObjectName("avatar")
        av.setFixedSize(48, 48)
        av.setAlignment(Qt.AlignCenter)
        hl.addWidget(av)
        info = QVBoxLayout()
        info.setSpacing(3)
        nm = QLabel(name)
        nm.setObjectName("profileName")
        info.addWidget(nm)
        stats = QLabel(
            f"Активных: <span style='color:#1e3a6f;font-weight:600'>{active}</span>"
            f"    Завершено: <span style='color:#1e3a6f;font-weight:600'>{done}</span>"
            f"    Оценено: <span style='color:#1e3a6f;font-weight:600'>{rated}</span>")
        stats.setObjectName("profileStats")
        stats.setTextFormat(Qt.RichText)
        info.addWidget(stats)
        hl.addLayout(info, 1)

        self.ui.myHead.setVisible(False)
        if getattr(self, "_head_installed", False):
            self.ui.myLay.removeWidget(self._head_widget)
            self._head_widget.deleteLater()
        self._head_widget = head
        self.ui.myLay.insertWidget(0, head)
        self._head_installed = True

        w = QWidget()
        wl = QVBoxLayout(w)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.setSpacing(12)
        for t in tasks:
            wl.addWidget(self.card(t, mine=True))
        if not tasks:
            lb = QLabel("У вас пока нет назначенных работ")
            lb.setAlignment(Qt.AlignCenter)
            lb.setStyleSheet("color:#6c86a3; padding:40px; font-size:13px;")
            wl.addWidget(lb)
        wl.addStretch()
        self.ui.myScroll.setWidget(w)

    def card(self, task, mine):
        meta = get_status(task.status)
        c = CollapsibleCard(task.title, meta.label, f"badge_{meta.badge}",
                            f"Дата: {task.date_range()}    Сотрудники: {task.performers or '—'}")

        desc = QLabel(task.description)
        desc.setObjectName("desc")
        desc.setTextFormat(Qt.PlainText)
        desc.setWordWrap(True)
        c.add_detail(desc)

        if task.status == "evaluated" and task.ratings:
            box = QLabel(f"Средняя оценка: {task.average_score()} баллов | " +
                         ", ".join(f"{x['name']}: {x['score']}" for x in task.ratings))
            box.setObjectName("ratingBox")
            box.setWordWrap(True)
            c.add_detail(box)

        if not mine and task.status == "pending":
            if self.vm.can_rate(task):
                row = QHBoxLayout()
                row.setSpacing(8)
                sb = QSpinBox()
                sb.setRange(1, 100)
                sb.setValue(80)
                sb.setMaximumWidth(90)
                row.addWidget(sb)
                b = QPushButton("Оценить")
                b.setObjectName("rateBtn")
                b.setCursor(Qt.PointingHandCursor)
                b.clicked.connect(lambda _, x=task, s=sb: self.rate(x, s.value()))
                row.addWidget(b)
                row.addStretch()
                c.add_detail_layout(row)
            elif task.ratings and date.today() <= task.eval_deadline:
                box = QLabel(f"Сбор оценок до {task.eval_deadline.strftime('%d.%m.%Y')} · Оценок получено: {len(task.ratings)}. "
                             f"Оценки других сотрудников будут видны после назначения работы.")
                box.setObjectName("collectBox")
                box.setWordWrap(True)
                c.add_detail(box)

        if mine:
            row = QHBoxLayout()
            row.setSpacing(8)
            if task.status == "assigned":
                if task.start_date <= date.today():
                    b = QPushButton("Приступить")
                    b.setObjectName("startBtn")
                    b.setCursor(Qt.PointingHandCursor)
                    b.clicked.connect(lambda _, x=task: self.start(x))
                    row.addWidget(b)
                else:
                    row.addWidget(QLabel(f"Работа начнётся {task.start_date.strftime('%d.%m.%Y')}"))
            elif task.status == "in_progress":
                performers = task.performer_list()
                if task.start_date > date.today():
                    row.addWidget(QLabel(f"Недоступно до {task.start_date.strftime('%d.%m.%Y')}"))
                elif len(performers) > 1 and task.marked_done:
                    row.addWidget(QLabel("Ожидает подтверждения другими исполнителями"))
                elif len(performers) > 1:
                    b = QPushButton("Отметить выполнение")
                    b.setObjectName("doneBtn")
                    b.setCursor(Qt.PointingHandCursor)
                    b.clicked.connect(lambda _, x=task: self.done(x))
                    row.addWidget(b)
                else:
                    b = QPushButton("Завершить")
                    b.setObjectName("doneBtn")
                    b.setCursor(Qt.PointingHandCursor)
                    b.clicked.connect(lambda _, x=task: self.done(x))
                    row.addWidget(b)
            elif task.status == "completed":
                row.addWidget(QLabel("Ожидает подтверждения зав. кафедрой"))
            row.addStretch()
            c.add_detail_layout(row)
        return c

    def rate(self, task, score):
        err = self.vm.rate(task, score)
        if err:
            QMessageBox.warning(self, "Ошибка", err)
            return
        self.refresh_history()

    def start(self, task):
        err = self.vm.start(task)
        if err:
            QMessageBox.warning(self, "Ошибка", err)
            return
        self.refresh_my()

    def done(self, task):
        err = self.vm.complete(task)
        if err:
            QMessageBox.warning(self, "Ошибка", err)
            return
        self.refresh_my()

    def on_tab(self, index):
        if index == 0:
            self.refresh_history()
        else:
            self.refresh_my()