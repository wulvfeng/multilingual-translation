"""
现代化样式模块 - UI全局QSS样式
"""


class ModernStyles:

    MAIN_STYLESHEET = """
    QWidget {
        background-color: #f0f2f5;
        font-family: 'Segoe UI', 'Microsoft YaHei', 'PingFang SC', Arial, sans-serif;
        font-size: 10pt;
        color: #334155;
    }
    QMainWindow { background: #f0f2f5; }

    QLabel { color: #334155; background: transparent; }

    QTextEdit, QLineEdit {
        background: white;
        border: 1px solid #cbd5e1;
        border-radius: 6pt;
        padding: 6pt 8pt;
        font-size: 10pt;
        color: #334155;
        selection-background-color: #6366f1;
    }
    QTextEdit:hover, QLineEdit:hover { border-color: #6366f1; }
    QTextEdit:focus, QLineEdit:focus { border-color: #4f46e5; }

    QComboBox {
        background: white;
        border: 1px solid #cbd5e1;
        border-radius: 6pt;
        padding: 5pt 8pt;
        font-size: 10pt;
        color: #334155;
        min-width: 60pt;
    }
    QComboBox:hover { border-color: #6366f1; }
    QComboBox::drop-down { border: none; width: 20pt; }
    QComboBox::down-arrow {
        image: url(none);
        border-left: 4pt solid transparent;
        border-right: 4pt solid transparent;
        border-top: 5pt solid #64748b;
        margin-right: 6pt;
    }
    QComboBox QAbstractItemView {
        background: white;
        border: 1px solid #cbd5e1;
        border-radius: 4pt;
        padding: 3pt;
        selection-background-color: #6366f1;
        selection-color: white;
        outline: none;
    }

    QPushButton {
        background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #6366f1, stop:1 #8b5cf6);
        color: white;
        border: none;
        border-radius: 6pt;
        padding: 8pt 16pt;
        font-size: 10pt;
        font-weight: 600;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #4f46e5, stop:1 #7c3aed);
    }
    QPushButton:pressed { background: #4338ca; }
    QPushButton:disabled { background: #cbd5e1; color: #94a3b8; }

    QPushButton#swap-btn {
        background: #f1f5f9;
        color: #6366f1;
        border: 1px solid #c7d2fe;
        border-radius: 17pt;
        font-size: 14pt;
        font-weight: 700;
        padding: 0;
    }
    QPushButton#swap-btn:hover { background: #e0e7ff; border-color: #6366f1; }

    QTableWidget {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 6pt;
        gridline-color: #f1f5f9;
        selection-background-color: #e0e7ff;
        selection-color: #1e293b;
        font-size: 9pt;
    }
    QTableWidget::item { padding: 4pt 6pt; border-bottom: 1px solid #f1f5f9; }
    QTableWidget::item:selected { background: #e0e7ff; }
    QHeaderView::section {
        background: #f8fafc;
        color: #475569;
        padding: 6pt 8pt;
        border: none;
        border-bottom: 1px solid #e2e8f0;
        font-weight: 600;
        font-size: 9pt;
    }

    QScrollBar:vertical {
        background: #f1f5f9; width: 7pt; margin: 0; border-radius: 3pt;
    }
    QScrollBar::handle:vertical {
        background: #cbd5e1; min-height: 20pt; border-radius: 3pt;
    }
    QScrollBar::handle:vertical:hover { background: #94a3b8; }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
    QScrollBar:horizontal {
        background: #f1f5f9; height: 7pt; margin: 0; border-radius: 3pt;
    }
    QScrollBar::handle:horizontal {
        background: #cbd5e1; min-width: 20pt; border-radius: 3pt;
    }
    QScrollBar::handle:horizontal:hover { background: #94a3b8; }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

    QProgressBar {
        background: #e2e8f0; border: none; border-radius: 3pt;
        max-height: 5pt; text-align: center;
    }
    QProgressBar::chunk {
        background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #6366f1, stop:1 #8b5cf6);
        border-radius: 3pt;
    }

    QStatusBar {
        background: white; color: #64748b;
        border-top: 1px solid #e2e8f0;
        font-size: 9pt; padding: 2pt 6pt;
    }
    QStatusBar::item { border: none; }

    QSplitter::handle { background: #e2e8f0; }
    QSplitter::handle:horizontal { width: 4pt; }
    QSplitter::handle:vertical { height: 4pt; }
    QSplitter::handle:hover { background: #a5b4fc; }

    QToolTip {
        background: #1e293b; color: white; border: none;
        border-radius: 4pt; padding: 5pt 8pt; font-size: 9pt;
    }
    """

    @classmethod
    def get_stylesheet(cls):
        return cls.MAIN_STYLESHEET
