from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
                             QCheckBox, QPushButton, QScrollArea, QWidget, QSizePolicy)
from PyQt5.QtCore import Qt


class ExecutorItem(QFrame):
    def __init__(self, staff, rating, current_score, checked, parent=None):
        super().__init__(parent)
        self.setObjectName("executorItem")
        self.name = staff.name
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        l = QHBoxLayout(self)
        l.setContentsMargins(14, 12, 14, 12)
        l.setSpacing(10)
        l.setAlignment(Qt.AlignVCenter)

        self.cb = QCheckBox()
        self.cb.setFixedSize(18, 18)
        l.addWidget(self.cb, 0, Qt.AlignVCenter)

        info = QVBoxLayout()
        info.setSpacing(6)
        info.setContentsMargins(0, 0, 0, 0)
        info.setAlignment(Qt.AlignVCenter)

        nm = QLabel(staff.name)
        nm.setObjectName("execName")
        nm.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        info.addWidget(nm)

        score_text = f"Оценка этой работы: {current_score}" if current_score else "Не оценивал"
        stats = QLabel(f"{staff.role}    Рейтинг: {rating['tot']} (пост.{rating['p']}/врем.{rating['t']})    {score_text}")
        stats.setObjectName("execStats")
        stats.setWordWrap(True)
        stats.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        info.addWidget(stats)

        badge = QLabel("Преподаватель" if staff.type == "teacher" else "УВП")
        badge.setObjectName("execBadgeTeacher" if staff.type == "teacher" else "execBadgeSupport")
        badge.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        info.addWidget(badge, 0, Qt.AlignLeft)

        l.addLayout(info, 1)

        self.cb.setChecked(checked)
        self._apply_sel(checked)
        self.cb.stateChanged.connect(self._on_state)
        self.mousePressEvent = self._on_click

    def _apply_sel(self, sel):
        self.setProperty("selected", "true" if sel else "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def _on_click(self, ev):
        self.cb.setChecked(not self.cb.isChecked())

    def _on_state(self, state):
        self._apply_sel(self.cb.isChecked())
        self.window().update_count()


class AssignDialog(QDialog):
    def __init__(self, task, staff_list, rating_map, avg, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Назначение сотрудников: {task.title}")
        self.resize(900, 640)
        self.task = task
        self.items = []

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        banner = QFrame()
        banner.setObjectName("taskBanner")
        bl = QVBoxLayout(banner)
        bl.setContentsMargins(18, 14, 18, 14)
        bl.setSpacing(4)
        bt = QLabel(task.title)
        bt.setObjectName("bannerTitle")
        bt.setWordWrap(True)
        bl.addWidget(bt)
        bm = QLabel(f"Срок: {task.date_range()}    Средняя оценка: "
                    f"{str(avg) + ' баллов' if avg else 'не оценена'}")
        bm.setObjectName("bannerMeta")
        bl.addWidget(bm)
        root.addWidget(banner)

        cols = QHBoxLayout()
        cols.setSpacing(16)

        teachers = [s for s in staff_list if s.type == "teacher"]
        support = [s for s in staff_list if s.type == "support"]
        current = task.performer_list()
        self.score_by_name = {r["name"]: r["score"] for r in task.ratings}

        cols.addWidget(self._section("Преподаватели", "sectionHeaderPink", teachers,
                                     rating_map, current), 1)
        cols.addWidget(self._section("Учебно-вспомогательный персонал",
                                     "sectionHeaderBlue", support, rating_map, current), 1)
        root.addLayout(cols, 1)

        self.count_lbl = QLabel("Выбрано сотрудников: 0")
        self.count_lbl.setObjectName("selectedCount")
        root.addWidget(self.count_lbl)

        btns = QHBoxLayout()
        btns.addStretch()
        cancel = QPushButton("Отмена")
        cancel.setCursor(Qt.PointingHandCursor)
        cancel.clicked.connect(self.reject)
        btns.addWidget(cancel)
        ok = QPushButton("Назначить")
        ok.setObjectName("newCreate")
        ok.setCursor(Qt.PointingHandCursor)
        ok.clicked.connect(self._accept)
        btns.addWidget(ok)
        root.addLayout(btns)

        self.update_count()

    def _section(self, title, header_obj, staff_list, rating_map, current):
        sec = QFrame()
        sec.setObjectName("executorSection")
        v = QVBoxLayout(sec)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)

        head = QLabel(title)
        head.setObjectName(header_obj)
        v.addWidget(head)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        inner = QWidget()
        il = QVBoxLayout(inner)
        il.setContentsMargins(0, 0, 0, 0)
        il.setSpacing(0)

        for s in staff_list:
            r = rating_map.get(s.name, {"p": 0, "t": 0, "tot": 0})
            it = ExecutorItem(s, r, self.score_by_name.get(s.name), s.name in current)
            self.items.append(it)
            il.addWidget(it)
        il.addStretch()
        scroll.setWidget(inner)
        v.addWidget(scroll, 1)
        return sec

    def update_count(self):
        n = sum(1 for it in self.items if it.cb.isChecked())
        self.count_lbl.setStyleSheet("")
        self.count_lbl.setText(f"Выбрано сотрудников: {n}")

    def selected_names(self):
        return [it.name for it in self.items if it.cb.isChecked()]

    def _accept(self):
        if not self.selected_names():
            self.count_lbl.setText("Выберите хотя бы одного сотрудника")
            self.count_lbl.setStyleSheet("color:#a80000;")
            return
        self.accept()