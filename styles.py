ZAV_QSS = """
QMainWindow, QWidget { background:#f5f0f0; font-family:'Segoe UI', system-ui, Roboto, sans-serif; color:#2d1e1e; }

QLabel#headerLbl {
    background:qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #b33f3f, stop:0.5 #6b4b9a, stop:1 #2b5797);
    color:white; font-size:18px; font-weight:600;
}

QTabWidget::pane { border:none; background:transparent; }
QTabWidget::tab-bar { left:0; }
QTabWidget > QWidget { background:#f5f0f0; color:#2d1e1e; }
QTabBar { background:transparent; }
QTabBar::tab {
    background:rgba(255,255,255,0.35); color:#7a2f2f;
    padding:10px 28px; min-width:120px;
    border-radius:30px; margin-right:8px;
    font-size:15px; font-weight:600;
}
QTabBar::tab:hover { background:rgba(255,255,255,0.6); color:#b33f3f; }
QTabBar::tab:selected { background:white; color:#b33f3f; font-size:17px; padding:10px 32px; }

QLineEdit, QTextEdit, QSpinBox, QDateEdit {
    padding:9px 14px; border:1px solid #d4c5c5; border-radius:16px;
    background:white; color:#2d1e1e; font-size:13px;
}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDateEdit:focus { border-color:#b33f3f; }

QPushButton {
    background:white; color:#3d2e2e; border:1px solid #d4c5c5;
    padding:5px 14px; border-radius:30px; font-size:13px; font-weight:500;
}
QPushButton:hover { background:#fdf5f5; }
QPushButton[danger="true"] { color:#b33f3f; border-color:#e0c0c0; }
QPushButton[danger="true"]:hover { background:#fff0f0; }

QPushButton#newCreate {
    background:qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #c14949, stop:1 #b33f3f);
    color:white; border:none; border-radius:14px;
    padding:12px 32px; font-size:14px; font-weight:600;
}
QPushButton#newCreate:hover {
    background:qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #b33f3f, stop:1 #9e3535);
}

QFrame#card { background:white; border:1px solid #f0e3e3; border-radius:18px; }
QFrame#cardRow { background:transparent; border:none; }
QFrame#cardRow:hover { background:#fdf8f8; border-radius:18px; }
QFrame#detailPanel { background:transparent; border:none; }

QLabel#arrow { color:#9e7a7a; font-size:20px; }
QLabel#taskName { font-weight:700; font-size:15px; color:#2d1e1e; }
QLabel#meta { color:#7d5e5e; font-size:12px; }
QLabel#desc { color:#2d1e1e; font-size:13px; }

QLabel#formTitle {
    font-size:22px; font-weight:700; color:#2d1e1e;
    padding-bottom:12px; border-bottom:2px solid #f5e5e5;
}
QFrame#formCard {
    background:qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #ffffff, stop:1 #fdf8f8);
    border:1px solid #efe0e0; border-radius:24px;
}

QLabel#badge_await { background:#fff0db; color:#b45309; border-radius:40px; padding:3px 14px; font-size:11px; font-weight:700; }
QLabel#badge_eval  { background:#e9d8fd; color:#6b21a5; border-radius:40px; padding:3px 14px; font-size:11px; font-weight:700; }
QLabel#badge_asg   { background:#dbeafe; color:#1e40af; border-radius:40px; padding:3px 14px; font-size:11px; font-weight:700; }
QLabel#badge_prog  { background:#ccf0eb; color:#0f5c54; border-radius:40px; padding:3px 14px; font-size:11px; font-weight:700; }
QLabel#badge_done  { background:#d1fae5; color:#0b5e42; border-radius:40px; padding:3px 14px; font-size:11px; font-weight:700; }
QLabel#badge_arch  { background:#f5eeee; color:#7d6b6b; border-radius:40px; padding:3px 14px; font-size:11px; font-weight:700; }

QLabel#ratingBox  { background:#fdf5ff; border-radius:16px; padding:8px 12px; font-size:13px; color:#4a2f7a; font-weight:500; }
QLabel#collectBox { background:#fff8e6; border-radius:16px; padding:8px 12px; font-size:13px; color:#8a5a00; font-weight:500; }
QLabel#pageLbl { background:#fdf5f5; border-radius:40px; padding:6px 18px; color:#3d2e2e; }
QLabel#myHead { background:#f0f4ff; padding:14px 18px; border-radius:16px; font-weight:600; color:#1e3a6f; }

QFrame#taskBanner { background:#fdf5f5; border-left:4px solid #b33f3f; border-radius:14px; }
QLabel#bannerTitle { font-weight:700; font-size:16px; color:#2d1e1e; }
QLabel#bannerMeta { font-size:13px; color:#7d5e5e; }

QFrame#executorSection { background:white; border:1px solid #e8d5d5; border-radius:14px; }
QLabel#sectionHeaderPink { background:#fde7e9; color:#a80000; padding:10px 14px; font-weight:700; font-size:13px; }
QLabel#sectionHeaderBlue { background:#e9e5fd; color:#3b2d7a; padding:10px 14px; font-weight:700; font-size:13px; }
QFrame#executorItem { background:transparent; border-bottom:1px solid #f5eded; }
QFrame#executorItem[selected="true"] { background:#fff8e1; }
QLabel#execName { font-weight:600; font-size:14px; color:#2d1e1e; }
QLabel#execStats { font-size:11px; color:#7d5e5e; }
QLabel#execBadgeTeacher { background:#e9e5fd; color:#3b2d7a; border-radius:12px; padding:2px 8px; font-size:10px; font-weight:600; }
QLabel#execBadgeSupport { background:#fff4ce; color:#8e6b00; border-radius:12px; padding:2px 8px; font-size:10px; font-weight:600; }
QLabel#selectedCount { background:#fdf5f5; border-radius:12px; padding:10px 14px; font-size:13px; font-weight:500; color:#3d2e2e; }

QCheckBox { color:#2d1e1e; font-size:13px; }
QCheckBox::indicator { width:16px; height:16px; border:1px solid #d4c5c5; border-radius:4px; background:white; }
QCheckBox::indicator:checked { background:#b33f3f; border-color:#b33f3f; }

QDialog { background:white; }
QScrollArea { border:none; background:transparent; }
QScrollArea > QWidget > QWidget { background:transparent; }
"""

ISP_QSS = """
QMainWindow, QWidget { background:#eef2f7; font-family:'Segoe UI', system-ui, Roboto, sans-serif; color:#0f172a; }

QLabel#headerLbl {
    background:qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #1e3a6f, stop:1 #2b5797);
    color:white; font-size:18px; font-weight:600;
}

QTabWidget::pane { border:none; background:transparent; }
QTabWidget::tab-bar { left:0; }
QTabWidget > QWidget { background:#eef2f7; color:#0f172a; }
QTabBar { background:transparent; }
QTabBar::tab {
    background:rgba(255,255,255,0.35); color:#1e3a6f;
    padding:10px 28px; min-width:120px;
    border-radius:30px; margin-right:8px;
    font-size:15px; font-weight:600;
}
QTabBar::tab:hover { background:rgba(255,255,255,0.6); color:#2b5797; }
QTabBar::tab:selected { background:white; color:#1e3a6f; font-size:17px; padding:10px 32px; }

QLineEdit, QSpinBox {
    padding:8px 16px; border:1px solid #cbd5e1; border-radius:16px;
    background:white; color:#0f172a; font-size:13px;
}
QLineEdit:focus, QSpinBox:focus { border-color:#1e3a6f; }

QPushButton {
    background:white; color:#1e293b; border:1px solid #cbd5e1;
    padding:5px 14px; border-radius:30px; font-size:13px; font-weight:500;
}
QPushButton:hover { background:#eef2f7; }
QPushButton#rateBtn, QPushButton#startBtn, QPushButton#doneBtn {
    background:#1e3a6f; color:white; border:none; padding:5px 14px; border-radius:30px;
}
QPushButton#rateBtn:hover, QPushButton#startBtn:hover, QPushButton#doneBtn:hover {
    background:#2b5797;
}

QFrame#card { background:white; border:1px solid #e2edf7; border-radius:18px; }
QFrame#cardRow { background:transparent; border:none; }
QFrame#cardRow:hover { background:#f8fafc; border-radius:18px; }
QFrame#detailPanel { background:transparent; border:none; }

QLabel#arrow { color:#6c86a3; font-size:20px; }
QLabel#taskName { font-weight:700; font-size:15px; color:#0f172a; }
QLabel#meta { color:#5b6e8c; font-size:12px; }
QLabel#desc { color:#1e2a47; font-size:13px; }

QLabel#badge_await { background:#fff0db; color:#b45309; border-radius:40px; padding:3px 14px; font-size:11px; font-weight:700; }
QLabel#badge_eval  { background:#e9d8fd; color:#6b21a5; border-radius:40px; padding:3px 14px; font-size:11px; font-weight:700; }
QLabel#badge_asg   { background:#dbeafe; color:#1e40af; border-radius:40px; padding:3px 14px; font-size:11px; font-weight:700; }
QLabel#badge_prog  { background:#ccf0eb; color:#0f5c54; border-radius:40px; padding:3px 14px; font-size:11px; font-weight:700; }
QLabel#badge_done  { background:#d1fae5; color:#0b5e42; border-radius:40px; padding:3px 14px; font-size:11px; font-weight:700; }
QLabel#badge_arch  { background:#eef2f5; color:#6b7d95; border-radius:40px; padding:3px 14px; font-size:11px; font-weight:700; }

QLabel#ratingBox  { background:#f5f0ff; border-radius:16px; padding:8px 12px; font-size:13px; color:#4a2f7a; font-weight:500; }
QLabel#collectBox { background:#fff8e6; border-radius:16px; padding:8px 12px; font-size:13px; color:#8a5a00; font-weight:500; }
QLabel#pageLbl { background:#edf2f7; border-radius:40px; padding:6px 18px; color:#1e3a6f; }

QFrame#myHeader { background:#f0f4ff; border-radius:16px; }
QLabel#avatar { background:#1e3a6f; color:white; border-radius:24px; font-weight:700; font-size:20px; }
QLabel#profileName { font-weight:700; font-size:16px; color:#0f172a; }
QLabel#profileStats { font-size:12px; color:#5b6e8c; }
QLabel#statVal { color:#1e3a6f; font-weight:600; }

QScrollArea { border:none; background:transparent; }
QScrollArea > QWidget > QWidget { background:transparent; }
"""

LOGIN_QSS = """
QWidget { background:#f0f2f5; font-family:'Segoe UI', system-ui, Roboto, sans-serif; }
QFrame#loginCard { background:white; border-radius:24px; }
QLabel { color:#3d2e2e; font-size:13px; font-weight:600; }
QLabel#titleLbl {
    background:qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #b33f3f, stop:0.5 #6b4b9a, stop:1 #2b5797);
    color:white; font-size:18px; font-weight:600; padding:18px 24px;
}
QLineEdit {
    padding:11px 16px; border-radius:30px; border:1px solid #d4c5c5;
    background:white; font-size:14px; color:#2d1e1e;
}
QLineEdit:focus { border-color:#6b4b9a; }
QPushButton#loginBtn {
    background:qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #b33f3f, stop:0.5 #6b4b9a, stop:1 #2b5797);
    color:white; padding:11px; border-radius:30px; font-weight:600; font-size:15px; border:none;
}
QPushButton#loginBtn:hover {
    background:qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #a03838, stop:0.5 #5f4289, stop:1 #264d87);
}
QLabel#hintLbl { color:#8a7a7a; font-size:11px; font-weight:400; }
"""