"""
现代化主窗口界面 - 支持多分辨率、高DPI、响应式布局
"""
import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QLineEdit, QFrame, QSplitter, QHeaderView,
    QStatusBar, QProgressBar, QApplication, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import Translator, LanguageSupport
from .styles import ModernStyles


_CARD_QSS = """
QFrame {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8pt;
}
"""


class TranslationWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, translator, text, src_lang, tgt_lang):
        super().__init__()
        self.translator = translator
        self.text = text
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang

    def run(self):
        try:
            result = self.translator.translate(self.text, self.src_lang, self.tgt_lang)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class TranslatorMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.translator = None
        self.worker = None
        self._scale = 1.0
        self._init_translator()
        self._calc_scale()
        self._init_ui()

    def _calc_scale(self):
        try:
            screen = QApplication.primaryScreen()
            if screen:
                self._scale = max(1.0, screen.logicalDotsPerInch() / 96.0)
        except Exception:
            pass

    def _s(self, v):
        return int(v * self._scale)

    def _init_translator(self):
        try:
            self.translator = Translator(model_name='./models', debug=True)
            self.translator.load_model()
        except Exception as e:
            print(f"初始化翻译器失败: {e}")
            self.translator = None

    def _init_ui(self):
        self.setWindowTitle('Neural Translator Pro - 现代化多语言翻译系统')
        screen = QApplication.primaryScreen()
        geo = screen.availableGeometry() if screen else None
        if geo:
            sw, sh = geo.width(), geo.height()
            w = max(960, min(int(sw * 0.72), 1500))
            h = max(640, min(int(sh * 0.72), 960))
            self.resize(w, h)
            self.setMinimumSize(max(720, int(sw * 0.45)), max(480, int(sh * 0.45)))
            self.move((sw - w) // 2 + geo.x(), (sh - h) // 2 + geo.y())
        else:
            self.resize(1100, 720)
            self.setMinimumSize(720, 480)

        self.setStyleSheet(ModernStyles.get_stylesheet())

        central = QWidget()
        central.setStyleSheet("background:#f0f2f5;")
        self.setCentralWidget(central)
        lay = QVBoxLayout(central)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay.addWidget(self._build_header())
        lay.addWidget(self._build_body(), 1)
        self._build_status_bar()

    def _build_header(self):
        w = QWidget()
        w.setObjectName("header")
        w.setStyleSheet("""
            QWidget#header {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #06b6d4);
            }
        """)
        w.setFixedHeight(self._s(96))
        lay = QVBoxLayout(w)
        lay.setContentsMargins(self._s(20), self._s(8), self._s(20), self._s(8))
        lay.setSpacing(self._s(2))
        lay.setAlignment(Qt.AlignCenter)

        t = QLabel("Neural Translator Pro")
        t.setAlignment(Qt.AlignCenter)
        t.setFont(QFont("Segoe UI", 18, QFont.Bold))
        t.setStyleSheet("color:white; background:transparent;")
        lay.addWidget(t)

        s = QLabel("基于 M2M-100 模型的智能多语言翻译系统")
        s.setAlignment(Qt.AlignCenter)
        s.setFont(QFont("Segoe UI", 10))
        s.setStyleSheet("color:rgba(255,255,255,0.85); background:transparent;")
        lay.addWidget(s)
        return w

    def _build_body(self):
        body = QWidget()
        body.setStyleSheet("background:#f0f2f5;")
        lay = QVBoxLayout(body)
        m = self._s(14)
        lay.setContentsMargins(m, m, m, m)
        lay.setSpacing(self._s(10))

        vs = QSplitter(Qt.Vertical)
        vs.setChildrenCollapsible(False)

        hs = QSplitter(Qt.Horizontal)
        hs.setChildrenCollapsible(False)
        hs.addWidget(self._build_settings_card())
        hs.addWidget(self._build_result_card())
        hs.setStretchFactor(0, 1)
        hs.setStretchFactor(1, 1)

        vs.addWidget(hs)
        vs.addWidget(self._build_table_card())
        vs.setStretchFactor(0, 5)
        vs.setStretchFactor(1, 3)

        lay.addWidget(vs, 1)
        return body

    def _build_settings_card(self):
        card = QFrame()
        card.setMinimumWidth(self._s(300))
        card.setStyleSheet(_CARD_QSS)
        lay = QVBoxLayout(card)
        p = self._s(16)
        lay.setContentsMargins(p, p, p, p)
        lay.setSpacing(self._s(12))

        t = QLabel("翻译设置")
        t.setFont(QFont("Segoe UI", 12, QFont.Bold))
        t.setStyleSheet("color:#1e293b;")
        lay.addWidget(t)

        lang_row = QHBoxLayout()
        lang_row.setSpacing(self._s(8))

        src_col = QVBoxLayout()
        src_col.setSpacing(self._s(4))
        sl = QLabel("源语言")
        sl.setFont(QFont("Segoe UI", 9))
        sl.setStyleSheet("color:#64748b;")
        src_col.addWidget(sl)
        self.src_lang_combo = QComboBox()
        self.src_lang_combo.setMinimumHeight(self._s(36))
        langs = LanguageSupport.get_all_languages(use_chinese=True)
        for code, name in langs:
            self.src_lang_combo.addItem(f"{code} - {name}", code)
        self.src_lang_combo.setCurrentText("zh - 中文")
        src_col.addWidget(self.src_lang_combo)
        lang_row.addLayout(src_col, 1)

        swap = QPushButton("⇄")
        swap.setObjectName("swap-btn")
        swap.setFixedSize(self._s(34), self._s(34))
        swap.setCursor(Qt.PointingHandCursor)
        swap.setToolTip("交换源语言和目标语言")
        swap.clicked.connect(self._swap_languages)
        lang_row.addWidget(swap, 0, Qt.AlignVCenter)

        tgt_col = QVBoxLayout()
        tgt_col.setSpacing(self._s(4))
        tl = QLabel("目标语言")
        tl.setFont(QFont("Segoe UI", 9))
        tl.setStyleSheet("color:#64748b;")
        tgt_col.addWidget(tl)
        self.tgt_lang_combo = QComboBox()
        self.tgt_lang_combo.setMinimumHeight(self._s(36))
        for code, name in langs:
            self.tgt_lang_combo.addItem(f"{code} - {name}", code)
        self.tgt_lang_combo.setCurrentText("en - 英语")
        tgt_col.addWidget(self.tgt_lang_combo)
        lang_row.addLayout(tgt_col, 1)

        lay.addLayout(lang_row)

        il = QLabel("输入文本")
        il.setFont(QFont("Segoe UI", 9))
        il.setStyleSheet("color:#64748b;")
        lay.addWidget(il)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("请输入要翻译的文本...")
        self.input_text.setMinimumHeight(self._s(80))
        self.input_text.setFont(QFont("Segoe UI", 10))
        self.input_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lay.addWidget(self.input_text, 1)

        self.translate_btn = QPushButton("开始翻译")
        self.translate_btn.setMinimumHeight(self._s(42))
        self.translate_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.translate_btn.setCursor(Qt.PointingHandCursor)
        self.translate_btn.clicked.connect(self.perform_translation)
        lay.addWidget(self.translate_btn)
        return card

    def _build_result_card(self):
        card = QFrame()
        card.setMinimumWidth(self._s(300))
        card.setStyleSheet(_CARD_QSS)
        lay = QVBoxLayout(card)
        p = self._s(16)
        lay.setContentsMargins(p, p, p, p)
        lay.setSpacing(self._s(12))

        t = QLabel("翻译结果")
        t.setFont(QFont("Segoe UI", 12, QFont.Bold))
        t.setStyleSheet("color:#1e293b;")
        lay.addWidget(t)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Segoe UI", 10))
        self.output_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.output_text.setStyleSheet("""
            QTextEdit {
                background:#f8fafc; border:1px solid #e2e8f0;
                border-radius:6pt; padding:8pt; color:#334155;
            }
        """)
        lay.addWidget(self.output_text, 1)

        cl = QLabel("驼峰命名")
        cl.setFont(QFont("Segoe UI", 9))
        cl.setStyleSheet("color:#64748b;")
        lay.addWidget(cl)

        self.camel_text = QLineEdit()
        self.camel_text.setReadOnly(True)
        self.camel_text.setMinimumHeight(self._s(36))
        self.camel_text.setFont(QFont("Consolas", 10))
        self.camel_text.setStyleSheet("""
            QLineEdit {
                background:#fffbeb; border:1px solid #fbbf24;
                border-radius:6pt; padding:6pt 10pt; color:#92400e;
            }
        """)
        lay.addWidget(self.camel_text)
        return card

    def _build_table_card(self):
        card = QFrame()
        card.setMinimumHeight(self._s(150))
        card.setStyleSheet(_CARD_QSS)
        lay = QVBoxLayout(card)
        p = self._s(14)
        lay.setContentsMargins(p, p, p, p)
        lay.setSpacing(self._s(8))

        top = QHBoxLayout()
        t = QLabel("支持的语言")
        t.setFont(QFont("Segoe UI", 12, QFont.Bold))
        t.setStyleSheet("color:#1e293b;")
        top.addWidget(t)
        top.addStretch()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索语言...")
        self.search_input.setMinimumHeight(self._s(32))
        self.search_input.setMaximumWidth(self._s(220))
        self.search_input.textChanged.connect(self.filter_languages)
        top.addWidget(self.search_input)
        lay.addLayout(top)

        langs = LanguageSupport.get_all_languages(use_chinese=True)
        self.lang_table = QTableWidget(len(langs), 2)
        self.lang_table.setHorizontalHeaderLabels(["语言代码", "语言名称"])
        self.lang_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.lang_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.lang_table.setAlternatingRowColors(True)
        self.lang_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.lang_table.verticalHeader().setVisible(False)
        self.lang_table.verticalHeader().setDefaultSectionSize(self._s(28))
        self.lang_table.setShowGrid(False)

        rh = self._s(28)
        for row, (code, name) in enumerate(langs):
            ci = QTableWidgetItem(code)
            ci.setTextAlignment(Qt.AlignCenter)
            ci.setFont(QFont("Consolas", 9, QFont.Bold))
            ci.setBackground(QColor("#e0e7ff"))
            self.lang_table.setItem(row, 0, ci)
            ni = QTableWidgetItem(name)
            ni.setFont(QFont("Segoe UI", 9))
            self.lang_table.setItem(row, 1, ni)
            self.lang_table.setRowHeight(row, rh)

        lay.addWidget(self.lang_table, 1)
        return card

    def _build_status_bar(self):
        self.statusBar().showMessage("就绪")
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(self._s(160))
        self.progress_bar.setVisible(False)
        self.statusBar().addPermanentWidget(self.progress_bar)

    def _swap_languages(self):
        si = self.src_lang_combo.currentIndex()
        ti = self.tgt_lang_combo.currentIndex()
        self.src_lang_combo.setCurrentIndex(ti)
        self.tgt_lang_combo.setCurrentIndex(si)

    def filter_languages(self, text):
        key = text.lower().strip()
        for row in range(self.lang_table.rowCount()):
            c = self.lang_table.item(row, 0)
            n = self.lang_table.item(row, 1)
            if c and n:
                if not key:
                    self.lang_table.setRowHidden(row, False)
                else:
                    self.lang_table.setRowHidden(
                        row, key not in c.text().lower() and key not in n.text().lower())

    def perform_translation(self):
        text = self.input_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "提示", "请输入要翻译的文本！")
            return
        if not self.translator:
            QMessageBox.warning(self, "错误", "翻译器未初始化，请检查模型文件！")
            return
        src = self.src_lang_combo.currentData()
        tgt = self.tgt_lang_combo.currentData()
        self.translate_btn.setEnabled(False)
        self.translate_btn.setText("翻译中...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.statusBar().showMessage("正在翻译...")
        self.worker = TranslationWorker(self.translator, text, src, tgt)
        self.worker.finished.connect(self._on_done)
        self.worker.error.connect(self._on_err)
        self.worker.start()

    def _on_done(self, result):
        self.translate_btn.setEnabled(True)
        self.translate_btn.setText("开始翻译")
        self.progress_bar.setVisible(False)
        self.statusBar().showMessage("翻译完成")
        src = self.src_lang_combo.currentData()
        tgt = self.tgt_lang_combo.currentData()
        sn = LanguageSupport.get_language_name(src, use_chinese=True)
        tn = LanguageSupport.get_language_name(tgt, use_chinese=True)
        self.output_text.setText(
            f"【源语言】{sn} ({src})\n【目标语言】{tn} ({tgt})\n【翻译结果】{result}")
        if tgt == 'en':
            self.camel_text.setText(
                LanguageSupport.process_translation_to_camel(
                    result, self.input_text.toPlainText(), src))
        else:
            self.camel_text.clear()

    def _on_err(self, error):
        self.translate_btn.setEnabled(True)
        self.translate_btn.setText("开始翻译")
        self.progress_bar.setVisible(False)
        self.statusBar().showMessage("翻译失败")
        QMessageBox.critical(self, "翻译错误", f"翻译过程中发生错误：{error}")
