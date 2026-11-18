from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal


class CollapsibleCard(QFrame):
    toggled = pyqtSignal(bool)

    def __init__(self, title, badge_text, badge_obj, meta_text, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self._open = False

        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(0, 0, 0, 0)
        self.root.setSpacing(0)

        self.row = QFrame()
        self.row.setObjectName("cardRow")
        self.row.setCursor(Qt.PointingHandCursor)
        row_l = QHBoxLayout(self.row)
        row_l.setContentsMargins(18, 14, 18, 14)
        row_l.setSpacing(12)

        left = QVBoxLayout()
        left.setSpacing(8)
        title_l = QHBoxLayout()
        title_l.setSpacing(12)
        self.name = QLabel(title)
        self.name.setObjectName("taskName")
        self.name.setWordWrap(True)
        title_l.addWidget(self.name, 1)
        self.badge = QLabel(badge_text)
        self.badge.setObjectName(badge_obj)
        self.badge.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        title_l.addWidget(self.badge, 0, Qt.AlignTop)
        left.addLayout(title_l)
        self.meta = QLabel(meta_text)
        self.meta.setObjectName("meta")
        left.addWidget(self.meta)
        row_l.addLayout(left, 1)

        self.arrow = QLabel("▼")
        self.arrow.setObjectName("arrow")
        self.arrow.setFixedWidth(28)
        self.arrow.setAlignment(Qt.AlignCenter)
        row_l.addWidget(self.arrow, 0, Qt.AlignTop)

        self.row.mousePressEvent = self._on_click
        self.root.addWidget(self.row)

        self.detail = QFrame()
        self.detail.setObjectName("detailPanel")
        self.detail_l = QVBoxLayout(self.detail)
        self.detail_l.setContentsMargins(18, 0, 18, 16)
        self.detail_l.setSpacing(8)
        self.detail.setVisible(False)
        self.root.addWidget(self.detail)

    def _on_click(self, ev):
        self.toggle()

    def toggle(self):
        self._open = not self._open
        self.detail.setVisible(self._open)
        self.arrow.setText("▲" if self._open else "▼")
        self.toggled.emit(self._open)

    def add_detail(self, w):
        self.detail_l.addWidget(w)
        return w

    def add_detail_layout(self, lay):
        self.detail_l.addLayout(lay)
        return lay