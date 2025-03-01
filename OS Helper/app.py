import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QCheckBox, QPushButton, QWidget, QVBoxLayout, \
    QLabel, QFileDialog, QGraphicsBlurEffect
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl, Qt
import json

def load_config(file_path='settings.json'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки конфигурации: {e}")
        return {}

def save_config(data, file_path='settings.json'):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка сохранения конфигурации: {e}")

class MainWindow(QMainWindow):
    settings = load_config()
    width = settings['window']['width']
    height = settings['window']['height']
    settings_visible = False

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OS Helper")
        self.setGeometry(self.settings['window']['pos_x'], self.settings['window']['pos_y'], self.width, self.height)
        self.setFixedSize(self.width, self.height)

        self.background_widget = QWidget(self)
        self.background_widget.setStyleSheet("image: url('backgrounds/base.png'); background-size: cover;")
        self.background_widget.setGeometry(self.rect())

        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile("sounds\settings.wav"))

        self.main_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.button_container = QVBoxLayout()
        # self.button_container.addStretch()
        self.main_layout.addLayout(self.button_container)


        # settings
        self.settings_panel = QWidget(self)
        self.settings_panel.setGeometry(self.rect())
        self.settings_panel.setStyleSheet("background: rgba(255, 255, 255, 200);")
        self.settings_panel.setGraphicsEffect(QGraphicsBlurEffect(blurRadius=10))
        self.settings_panel_layout = QVBoxLayout()
        self.settings_panel_layout.setAlignment(Qt.AlignTop)
        self.settings_panel.setLayout(self.settings_panel_layout)

        self.exit_checkbox = QCheckBox("Подтверждать выход", self)
        self.exit_checkbox.setStyleSheet("background: none; margin-bottom: 5px")
        self.settings_panel_layout.addWidget(self.exit_checkbox)
        self.background_isOn = QCheckBox("Выключить фон", self)
        self.background_isOn.setStyleSheet("background: none; margin-bottom: 5px")
        self.settings_panel_layout.addWidget(self.background_isOn)

        self.settings_panel.hide()


        self.settings_button = QPushButton(self)
        self.settings_button.setGeometry(self.width - 34, 0, 32, 32)
        self.settings_button.setStyleSheet(
            "background: transparent; image: url('sprites/settings.png'); background-size: cover;")
        self.settings_button.clicked.connect(self.toggle_settings)

        self.add_button = QPushButton(self)
        self.add_button.setGeometry(self.width - 34, self.height - 34, 32, 32)
        self.add_button.setStyleSheet(
            "background: transparent; image: url('sprites/add.png'); background-size: cover;")
        self.add_button.clicked.connect(self.add_dynamic_button)

    def generate_desktop(self):
        self.apps = self.settings['apps']
        for app_name in self.apps:
            pass

    def toggle_settings(self):
        self.sound_effect.play()
        self.settings_visible = not self.settings_visible
        if self.settings_visible:
            self.settings_panel.show()
        else:
            self.settings_panel.hide()

    def add_dynamic_button(self):
        new_button = QPushButton("Новая кнопка", self)
        new_button.clicked.connect(lambda: print("Заглушка функции"))
        self.button_container.addWidget(new_button)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Все файлы (*)")
        if file_path:
            pass

    def closeEvent(self, event):
        self.sound_effect.play()
        if self.settings.get('onClose', False):
            event.accept()
            return

        close_msg = QMessageBox(self)
        close_msg.setWindowTitle("Выход")
        close_msg.setText("Выйти из OS Helper?")
        close_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        check_box = QCheckBox("Не спрашивать снова")
        close_msg.setCheckBox(check_box)

        reply = close_msg.exec()

        if check_box.isChecked():
            self.settings['onClose'] = True
            save_config(self.settings)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())