from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
                             QScrollArea, QVBoxLayout, QWidget, QLineEdit)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import urllib.request
import threading


def main():
    app = QApplication([])

    inputBox = QLineEdit()
    inputBox.setPlaceholderText("type something here")
    inputBox.returnPressed.connect(lambda: on_click(inputBox.text(), out))

    submit_button = QPushButton("meowify")
    submit_button.clicked.connect(lambda: on_click(inputBox.text(), out))

    reload_button = QPushButton("refresh")
    reload_button.clicked.connect(lambda: refresh_cat(img))

    form = QHBoxLayout()
    form.addWidget(inputBox)
    form.addWidget(submit_button)

    out = QLabel()
    out.setWordWrap(True)
    out.setAlignment(Qt.AlignmentFlag.AlignLeft
                     | Qt.AlignmentFlag.AlignTop)  # type: ignore

    scroll = QScrollArea()
    scroll.setWidget(out)
    scroll.setWidgetResizable(True)

    img = QLabel()
    img.setPixmap(get_cat_pixmap())

    layout = QVBoxLayout()
    layout.addLayout(form)
    layout.addWidget(scroll)
    layout.addWidget(reload_button)
    layout.addWidget(img)

    window = QWidget()
    window.setFixedSize(400, 400)
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


def on_click(text: str, label: QLabel):
    label.setText(meowify(text))


def meowify(text: str):
    return text.replace("a", "meow")


if __name__ == "__main__":
    main()
