import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QScrollArea, QGridLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class LogsWindow(QWidget):
    def __init__(self, log_dir="app/logs/detections"):
        super().__init__()
        self.setWindowTitle("Historique des intrusions")
        self.setGeometry(300, 200, 700, 500)

        layout = QVBoxLayout()

        # Scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        grid = QGridLayout()
        content.setLayout(grid)

        images = [f for f in os.listdir(log_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        for index, img_name in enumerate(images):
            path = os.path.join(log_dir, img_name)
            pixmap = QPixmap(path).scaledToWidth(200, Qt.SmoothTransformation)

            label = QLabel()
            label.setPixmap(pixmap)
            label.setToolTip(img_name)

            caption = QLabel(img_name)
            caption.setAlignment(Qt.AlignCenter)

            # Ajouter l'image et le nom
            grid.addWidget(label, index // 3, (index % 3) * 2)
            grid.addWidget(caption, index // 3, (index % 3) * 2 + 1)

        scroll.setWidget(content)
        layout.addWidget(scroll)
        self.setLayout(layout)
