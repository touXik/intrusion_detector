# app/main.py
from face_recognition1 import load_known_faces, recognize_faces_in_frame
import datetime
import os

import sys
import cv2

from register_face import capture_new_face
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout, QInputDialog
)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Intrusion Detector - Reconnaissance Faciale")
        self.setGeometry(100, 100, 800, 500)

        
        # Widgets
        self.image_label = QLabel("Webcam feed")
        self.image_label.setFixedSize(640, 480)
        self.image_label.setAlignment(Qt.AlignCenter)

               # Boutons
        self.start_button = QPushButton("🎥 Start Surveillance")
        self.add_face_button = QPushButton("🧍 Add New Face")
        self.view_logs_button = QPushButton("📜 View Logs")

                # Connexions
        self.start_button.clicked.connect(self.start_surveillance)
        self.add_face_button.clicked.connect(self.add_new_face)
        self.view_logs_button.clicked.connect(self.view_logs)

           # Layouts
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.add_face_button)
        button_layout.addWidget(self.view_logs_button)
        button_layout.addStretch()

        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(button_layout)

        # Zone centrale
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Timer et camera 
        self.capture = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    # Fonctions reliées aux boutons (on met juste un message pour le moment)
    def start_surveillance(self):
        if not self.capture:
            self.capture = cv2.VideoCapture(0)
            self.known_encodings, self.known_names = load_known_faces()
            self.timer.start(30)
            QMessageBox.information(self,"Surveillance", "Webcam activée ✅")
        else:
            self.timer.stop()
            self.capture.release()
            self.capture = None
            self.image_label.clear()
            self.image_label.setText("Webcam feed")
            QMessageBox.information(self, "Surveillance", "Webcam désactivée ❌")

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            recognized_faces = recognize_faces_in_frame(frame, self.known_encodings, self.known_names)

            for name , (top, right, bottom, left) in recognized_faces : 
                color = (0, 255, 0) if name != "Inconnu" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left, top - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

                # sauvgarder limage si inconnu 
                if name == "Inconnu" :
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    os.makedirs("app/logs/detections", exist_ok=True)
                    cv2.imwrite(f"app/logs/detections/intrus_{timestamp}.jpg", frame)
            
            # affichage 
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = rgb.shape
            bytes_per_line = 3 * width
            q_image = QImage(rgb, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)    

    def add_new_face(self):
        name, ok = QInputDialog.getText(self,"Ajouter un visage","Entrer le nom de la personne :")
        if ok and name:
            success = capture_new_face(name)
            if success:
                QMessageBox.information(self,"Succés",f"le visage de {name} a été enregistré avec succés.")
            else:
                QMessageBox.critical(self,"Erreur")


    def view_logs(self):
        QMessageBox.information(self, "Logs", "Affichage des logs... (à venir)")

# Point d’entrée
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
