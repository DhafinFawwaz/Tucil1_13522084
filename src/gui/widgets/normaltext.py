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
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def set_default_style(self):
        self.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)

    def set_error_style(self):
        self.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: red;
                font-size: 14px;
                font-weight: bold;
            }
        """)