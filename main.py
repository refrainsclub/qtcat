from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import urllib.request
import threading


def main():
    app = QApplication([])

    text_edit = QTextEdit()
    text_edit.setPlaceholderText("type something here")
    text_edit.textChanged.connect(lambda: on_change(text_edit, out))

    out = QLabel()
    out.setWordWrap(True)
    out.setAlignment(Qt.AlignmentFlag.AlignLeft
                     | Qt.AlignmentFlag.AlignTop)  # type: ignore

    out_scroll = QScrollArea()
    out_scroll.setWidget(out)
    out_scroll.setWidgetResizable(True)

    refresh_button = QPushButton("refresh")
    refresh_button.clicked.connect(lambda: refresh_cat(cat_image))

    cat_image = QLabel()
    refresh_cat(cat_image)

    layout = QVBoxLayout()
    layout.addWidget(text_edit)
    layout.addWidget(out_scroll)
    layout.addWidget(refresh_button)
    layout.addWidget(cat_image)

    window = QWidget()
    window.setFixedSize(500, 500)
    window.setWindowTitle("qtcat <3")
    window.setLayout(layout)
    window.show()

    app.exec()


def get_cat_pixmap():
    data = urllib.request.urlopen("https://cataas.com/cat").read()
    img = QImage()
    img.loadFromData(data)
    pixmap = QPixmap(img)
    return pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio)


def refresh_cat(label: QLabel):
    thread = threading.Thread(target=lambda: label.setPixmap(get_cat_pixmap()))
    thread.start()


def on_change(text_edit: QTextEdit, label: QLabel):
    text = text_edit.toPlainText()
    meowified = meowify(text)
    label.setText(meowified)


def meowify(text: str):
    mapping = str.maketrans({"e": "meow", "t": "mrrp", "a": "nya"})
    return text.translate(mapping)


if __name__ == "__main__":
    main()
