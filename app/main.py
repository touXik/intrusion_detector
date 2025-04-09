# app/main.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Intrusion Detector - Reconnaissance Faciale")
        self.setGeometry(200, 200, 400, 300)

        # Layout principal
        layout = QVBoxLayout()

        # Boutons
        self.start_button = QPushButton("🎥 Start Surveillance")
        self.add_face_button = QPushButton("🧍 Add New Face")
        self.view_logs_button = QPushButton("📜 View Logs")

        # Connexions
        self.start_button.clicked.connect(self.start_surveillance)
        self.add_face_button.clicked.connect(self.add_new_face)
        self.view_logs_button.clicked.connect(self.view_logs)

        # Ajout au layout
        layout.addWidget(self.start_button)
        layout.addWidget(self.add_face_button)
        layout.addWidget(self.view_logs_button)

        # Zone centrale
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # Fonctions reliées aux boutons (on met juste un message pour le moment)
    def start_surveillance(self):
        QMessageBox.information(self, "Surveillance", "Démarrage de la surveillance... (à venir)")

    def add_new_face(self):
        QMessageBox.information(self, "Nouvel utilisateur", "Ajout d’un nouveau visage... (à venir)")

    def view_logs(self):
        QMessageBox.information(self, "Logs", "Affichage des logs... (à venir)")

# Point d’entrée
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
