from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QSizePolicy


class NormalText(QLabel):
    def __init__(self, parent: QWidget, text: str):
        super().__init__(parent)
        self.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.setText(text)