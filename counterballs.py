# made by Drobeled | 2025
import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QListWidget, QListWidgetItem, QDialog, QSpinBox,
                             QTabWidget, QCheckBox, QFileDialog, QMessageBox,
                             QGroupBox, QGridLayout, QTextEdit, QComboBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont

# Translation dictionaries
TRANSLATIONS = {
    "ru": {
        "app_title": "Приложение для подсчёта баллов",
        "console_title": "Консоль приложения",
        "settings_title": "Настройки",
        "add_participant": "Добавить участника",
        "participant_list": "Список участников:",
        "select_participant": "Выберите участника",
        "points": "баллов",
        "custom_points": "Произвольное изменение баллов",
        "apply": "Применить",
        "delete_participant": "Удалить выбранного участника",
        "save_config": "Сохранить конфиг",
        "load_config": "Загрузить конфиг",
        "autosave_off": "Автосохранение: выключено",
        "autosave_on": "Автосохранение: включено",
        "config_folder": "Папка для конфигов:",
        "change_folder": "Изменить папку",
        "autosave_label": "Автосохранение каждые 30 секунд",
        "clear_config": "Очистить текущий конфиг",
        "open_console": "Открыть консоль",
        "clear_console": "Очистить консоль",
        "language": "Язык:",
        "name_placeholder": "Введите имя участника",
        "manage_points": "Управление баллами",
        "settings": "Настройки",
        "confirm_delete": "Вы уверены, что хотите удалить участника '{}'?",
        "confirm_clear": "Вы уверены, что хотите очистить текущий конфиг? Все данные будут удалены.",
        "config_saved": "Конфиг сохранен в {}",
        "config_loaded": "Конфиг загружен из {}",
        "config_empty": "Конфиг уже пустой",
        "select_participant_error": "Выберите участника для удаления",
        "console_opened": "Консоль приложения открыта",
        "participant_added": "Добавлен участник: {}",
        "participant_deleted": "Удален участник: {}",
        "points_changed": "Изменены баллы участника {}: {:+}",
        "config_saved_log": "Конфиг сохранен: {}",
        "config_loaded_log": "Конфиг загружен: {}",
        "autosave_enabled": "Автосохранение включено",
        "autosave_disabled": "Автосохранение выключено",
        "config_cleared": "Текущий конфиг очищен",
        "folder_changed": "Изменена папка для конфигов: {}",
        "autosave_log": "Автосохранение: {}"
    },
    "en": {
        "app_title": "Score Counting Application",
        "console_title": "Application Console",
        "settings_title": "Settings",
        "add_participant": "Add Participant",
        "participant_list": "Participants List:",
        "select_participant": "Select Participant",
        "points": "points",
        "custom_points": "Custom Points Adjustment",
        "apply": "Apply",
        "delete_participant": "Delete Selected Participant",
        "save_config": "Save Config",
        "load_config": "Load Config",
        "autosave_off": "Autosave: disabled",
        "autosave_on": "Autosave: enabled",
        "config_folder": "Config folder:",
        "change_folder": "Change folder",
        "autosave_label": "Autosave every 30 seconds",
        "clear_config": "Clear current config",
        "open_console": "Open console",
        "clear_console": "Clear console",
        "language": "Language:",
        "name_placeholder": "Enter participant name",
        "manage_points": "Points Management",
        "settings": "Settings",
        "confirm_delete": "Are you sure you want to delete participant '{}'?",
        "confirm_clear": "Are you sure you want to clear the current config? All data will be deleted.",
        "config_saved": "Config saved to {}",
        "config_loaded": "Config loaded from {}",
        "config_empty": "Config is already empty",
        "select_participant_error": "Select a participant to delete",
        "console_opened": "Application console opened",
        "participant_added": "Participant added: {}",
        "participant_deleted": "Participant deleted: {}",
        "points_changed": "Points changed for participant {}: {:+}",
        "config_saved_log": "Config saved: {}",
        "config_loaded_log": "Config loaded: {}",
        "autosave_enabled": "Autosave enabled",
        "autosave_disabled": "Autosave disabled",
        "config_cleared": "Current config cleared",
        "folder_changed": "Config folder changed: {}",
        "autosave_log": "Autosave: {}"
    }
}

class ConsoleWindow(QMainWindow):
    log_signal = pyqtSignal(str)
    
    def __init__(self, language="ru"):
        super().__init__()
        self.language = language
        self.setWindowTitle(TRANSLATIONS[language]["console_title"])
        self.setGeometry(200, 200, 800, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        layout.addWidget(self.console)
        
        clear_button = QPushButton(TRANSLATIONS[language]["clear_console"])
        clear_button.clicked.connect(self.console.clear)
        layout.addWidget(clear_button)
        
        self.log_signal.connect(self.add_log)

    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.append(f"[{timestamp}] {message}")

    def set_language(self, language):
        self.language = language
        self.setWindowTitle(TRANSLATIONS[language]["console_title"])
        self.findChild(QPushButton).setText(TRANSLATIONS[language]["clear_console"])

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.setGeometry(200, 200, 400, 200)
        layout = QVBoxLayout()
        self.autosave_checkbox = QCheckBox("Включить автосохранение (каждые 30 секунд)")
        layout.addWidget(self.autosave_checkbox)
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить настройки")
        self.save_button.clicked.connect(self.accept)
        buttons_layout.addWidget(self.save_button)
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
    
    def get_settings(self):
        return {"autosave": self.autosave_checkbox.isChecked()}
    
    def set_settings(self, settings):
        self.autosave_checkbox.setChecked(settings.get("autosave", False))

class ScoreApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language = "ru"
        self.setWindowTitle(TRANSLATIONS[self.language]["app_title"])
        self.setGeometry(100, 100, 800, 700)
        self.participants = {}
        self.settings = {
            "autosave": False,
            "config_dir": os.path.join(os.path.expanduser("~"), "PYcounter"),
            "language": "ru"
        }
        if not os.path.exists(self.settings["config_dir"]):
            os.makedirs(self.settings["config_dir"])
        self.autosave_timer = QTimer()
        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.setInterval(30000)
        self.current_participant = None
        self.current_config_file = None
        self.console_window = None
        self.init_ui()
        self.load_latest_config()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        score_tab = QWidget()
        score_layout = QVBoxLayout()
        score_tab.setLayout(score_layout)
        self.tabs.addTab(score_tab, TRANSLATIONS[self.language]["manage_points"])
        settings_tab = QWidget()
        settings_layout = QVBoxLayout()
        settings_tab.setLayout(settings_layout)
        self.tabs.addTab(settings_tab, TRANSLATIONS[self.language]["settings"])
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(TRANSLATIONS[self.language]["name_placeholder"])
        score_layout.addWidget(self.name_input)
        
        add_button = QPushButton(TRANSLATIONS[self.language]["add_participant"])
        add_button.clicked.connect(self.add_participant)
        score_layout.addWidget(add_button)
        
        self.participant_list = QListWidget()
        self.participant_list.itemClicked.connect(self.select_participant)
        score_layout.addWidget(QLabel(TRANSLATIONS[self.language]["participant_list"]))
        score_layout.addWidget(self.participant_list)
        
        self.score_label = QLabel(TRANSLATIONS[self.language]["select_participant"])
        score_layout.addWidget(self.score_label)
        
        buttons_layout = QHBoxLayout()
        self.add_5_button = QPushButton("+5")
        self.add_5_button.clicked.connect(lambda: self.change_score(5))
        self.add_5_button.setEnabled(False)
        buttons_layout.addWidget(self.add_5_button)
        
        self.add_1_button = QPushButton("+1")
        self.add_1_button.clicked.connect(lambda: self.change_score(1))
        self.add_1_button.setEnabled(False)
        buttons_layout.addWidget(self.add_1_button)
        
        self.sub_1_button = QPushButton("-1")
        self.sub_1_button.clicked.connect(lambda: self.change_score(-1))
        self.sub_1_button.setEnabled(False)
        buttons_layout.addWidget(self.sub_1_button)
        
        self.sub_5_button = QPushButton("-5")
        self.sub_5_button.clicked.connect(lambda: self.change_score(-5))
        self.sub_5_button.setEnabled(False)
        buttons_layout.addWidget(self.sub_5_button)
        
        score_layout.addLayout(buttons_layout)
        
        custom_score_group = QGroupBox(TRANSLATIONS[self.language]["custom_points"])
        custom_layout = QHBoxLayout()
        self.custom_score_input = QSpinBox()
        self.custom_score_input.setRange(-1000, 1000)
        self.custom_score_input.setValue(0)
        custom_layout.addWidget(self.custom_score_input)
        
        self.custom_score_button = QPushButton(TRANSLATIONS[self.language]["apply"])
        self.custom_score_button.clicked.connect(self.apply_custom_score)
        self.custom_score_button.setEnabled(False)
        custom_layout.addWidget(self.custom_score_button)
        
        custom_score_group.setLayout(custom_layout)
        score_layout.addWidget(custom_score_group)
        
        delete_button = QPushButton(TRANSLATIONS[self.language]["delete_participant"])
        delete_button.clicked.connect(self.delete_participant)
        score_layout.addWidget(delete_button)
        
        file_buttons_layout = QHBoxLayout()
        self.save_button = QPushButton(TRANSLATIONS[self.language]["save_config"])
        self.save_button.clicked.connect(self.save_config)
        file_buttons_layout.addWidget(self.save_button)
        
        self.load_button = QPushButton(TRANSLATIONS[self.language]["load_config"])
        self.load_button.clicked.connect(self.load_config)
        file_buttons_layout.addWidget(self.load_button)
        
        score_layout.addLayout(file_buttons_layout)
        
        self.autosave_label = QLabel(TRANSLATIONS[self.language]["autosave_off"])
        self.autosave_label.setObjectName("autosave_label")
        score_layout.addWidget(self.autosave_label)
        
        settings_form = QGridLayout()
        settings_form.addWidget(QLabel(TRANSLATIONS[self.language]["config_folder"]), 0, 0)
        self.config_dir_edit = QLineEdit(self.settings["config_dir"])
        settings_form.addWidget(self.config_dir_edit, 0, 1)
        
        self.change_dir_button = QPushButton(TRANSLATIONS[self.language]["change_folder"])
        self.change_dir_button.clicked.connect(self.change_config_dir)
        settings_form.addWidget(self.change_dir_button, 0, 2)
        
        self.settings_autosave = QCheckBox(TRANSLATIONS[self.language]["autosave_label"])
        self.settings_autosave.setChecked(self.settings["autosave"])
        self.settings_autosave.stateChanged.connect(self.toggle_autosave)
        settings_form.addWidget(self.settings_autosave, 1, 0, 1, 3)
        
        self.clear_config_button = QPushButton(TRANSLATIONS[self.language]["clear_config"])
        self.clear_config_button.clicked.connect(self.clear_current_config)
        settings_form.addWidget(self.clear_config_button, 2, 0, 1, 3)
        
        self.open_console_button = QPushButton(TRANSLATIONS[self.language]["open_console"])
        self.open_console_button.clicked.connect(self.open_console)
        settings_form.addWidget(self.open_console_button, 3, 0, 1, 3)
        
        settings_form.addWidget(QLabel(TRANSLATIONS[self.language]["language"]), 4, 0)
        self.language_combo = QComboBox()
        self.language_combo.addItem("Русский", "ru")
        self.language_combo.addItem("English", "en")
        self.language_combo.setCurrentText("Русский" if self.language == "ru" else "English")
        self.language_combo.currentIndexChanged.connect(self.change_language)
        settings_form.addWidget(self.language_combo, 4, 1, 1, 2)
        
        settings_layout.addLayout(settings_form)
        settings_layout.addStretch()

    def change_language(self):
        new_lang = self.language_combo.currentData()
        if new_lang != self.language:
            self.language = new_lang
            self.settings["language"] = new_lang
            self.update_ui_language()
            if self.console_window:
                self.console_window.set_language(new_lang)
            self.log_message(TRANSLATIONS[new_language]["console_opened"])

    def update_ui_language(self):
        self.setWindowTitle(TRANSLATIONS[self.language]["app_title"])
        self.tabs.setTabText(0, TRANSLATIONS[self.language]["manage_points"])
        self.tabs.setTabText(1, TRANSLATIONS[self.language]["settings"])
        self.name_input.setPlaceholderText(TRANSLATIONS[self.language]["name_placeholder"])
        self.findChild(QPushButton, None).setText(TRANSLATIONS[self.language]["add_participant"])
        self.findChild(QLabel).setText(TRANSLATIONS[self.language]["participant_list"])
        self.score_label.setText(TRANSLATIONS[self.language]["select_participant"])
        self.findChild(QGroupBox).setTitle(TRANSLATIONS[self.language]["custom_points"])
        self.custom_score_button.setText(TRANSLATIONS[self.language]["apply"])
        self.findChildren(QPushButton)[3].setText(TRANSLATIONS[self.language]["delete_participant"])
        self.save_button.setText(TRANSLATIONS[self.language]["save_config"])
        self.load_button.setText(TRANSLATIONS[self.language]["load_config"])
        self.autosave_label.setText(TRANSLATIONS[self.language]["autosave_off"] if not self.settings["autosave"] else TRANSLATIONS[self.language]["autosave_on"])
        self.findChild(QLabel, None).setText(TRANSLATIONS[self.language]["config_folder"])
        self.change_dir_button.setText(TRANSLATIONS[self.language]["change_folder"])
        self.settings_autosave.setText(TRANSLATIONS[self.language]["autosave_label"])
        self.clear_config_button.setText(TRANSLATIONS[self.language]["clear_config"])
        self.open_console_button.setText(TRANSLATIONS[self.language]["open_console"])
        self.findChild(QLabel, None).setText(TRANSLATIONS[self.language]["language"])

    def log_message(self, message):
        print(message)
        if self.console_window:
            self.console_window.log_signal.emit(message)

    def open_console(self):
        if not self.console_window:
            self.console_window = ConsoleWindow(self.language)
        self.console_window.show()
        self.console_window.activateWindow()
        self.log_message(TRANSLATIONS[self.language]["console_opened"])

    def add_participant(self):
        name = self.name_input.text().strip()
        if name and name not in self.participants:
            self.participants[name] = 0
            self.update_participant_list()
            self.name_input.clear()
            self.log_message(TRANSLATIONS[self.language]["participant_added"].format(name))

    def delete_participant(self):
        if not self.current_participant:
            QMessageBox.warning(self, "Error", TRANSLATIONS[self.language]["select_participant_error"])
            return
            
        reply = QMessageBox.question(self, "Confirm", 
                                   TRANSLATIONS[self.language]["confirm_delete"].format(self.current_participant),
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            deleted_name = self.current_participant
            del self.participants[self.current_participant]
            self.current_participant = None
            self.update_participant_list()
            self.score_label.setText(TRANSLATIONS[self.language]["select_participant"])
            self.add_5_button.setEnabled(False)
            self.add_1_button.setEnabled(False)
            self.sub_1_button.setEnabled(False)
            self.sub_5_button.setEnabled(False)
            self.custom_score_button.setEnabled(False)
            self.log_message(TRANSLATIONS[self.language]["participant_deleted"].format(deleted_name))

    def update_participant_list(self):
        self.participant_list.clear()
        for i, (name, score) in enumerate(self.participants.items(), 1):
            item = QListWidgetItem(f"{i}. {name}\t{score}")
            item.setData(Qt.UserRole, name)
            self.participant_list.addItem(item)

    def select_participant(self, item):
        self.current_participant = item.data(Qt.UserRole)
        self.score_label.setText(f"{self.current_participant}: {self.participants[self.current_participant]} {TRANSLATIONS[self.language]['points']}")
        self.add_5_button.setEnabled(True)
        self.add_1_button.setEnabled(True)
        self.sub_1_button.setEnabled(True)
        self.sub_5_button.setEnabled(True)
        self.custom_score_button.setEnabled(True)

    def change_score(self, points):
        if self.current_participant:
            self.participants[self.current_participant] += points
            self.score_label.setText(f"{self.current_participant}: {self.participants[self.current_participant]} {TRANSLATIONS[self.language]['points']}")
            self.update_participant_list()
            self.log_message(TRANSLATIONS[self.language]["points_changed"].format(self.current_participant, points))

    def apply_custom_score(self):
        if self.current_participant:
            points = self.custom_score_input.value()
            self.participants[self.current_participant] += points
            self.score_label.setText(f"{self.current_participant}: {self.participants[self.current_participant]} {TRANSLATIONS[self.language]['points']}")
            self.update_participant_list()
            self.log_message(TRANSLATIONS[self.language]["points_changed"].format(self.current_participant, points))

    def save_config(self):
        options = QFileDialog.Options()
        default_path = os.path.join(self.settings["config_dir"], f"config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Config", default_path, "JSON Files (*.json)", options=options)
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump({
                        "participants": self.participants,
                        "timestamp": datetime.now().isoformat(),
                        "language": self.language
                    }, f, ensure_ascii=False, indent=2)
                self.current_config_file = file_name
                QMessageBox.information(self, "Success", TRANSLATIONS[self.language]["config_saved"].format(file_name))
                self.log_message(TRANSLATIONS[self.language]["config_saved_log"].format(file_name))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save config: {str(e)}")
                self.log_message(f"Error saving config: {str(e)}")

    def load_config(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Config", self.settings["config_dir"], "JSON Files (*.json)", options=options)
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.participants = data.get("participants", {})
                self.current_config_file = file_name
                self.language = data.get("language", "ru")
                self.language_combo.setCurrentText("Русский" if self.language == "ru" else "English")
                self.update_ui_language()
                self.update_participant_list()
                QMessageBox.information(self, "Success", TRANSLATIONS[self.language]["config_loaded"].format(file_name))
                self.log_message(TRANSLATIONS[self.language]["config_loaded_log"].format(file_name))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load config: {str(e)}")
                self.log_message(f"Error loading config: {str(e)}")

    def load_latest_config(self):
        config_dir = self.settings["config_dir"]
        if os.path.exists(config_dir):
            json_files = [f for f in os.listdir(config_dir) if f.endswith('.json')]
            if json_files:
                latest_file = max(json_files, key=lambda x: os.path.getctime(os.path.join(config_dir, x)))
                try:
                    with open(os.path.join(config_dir, latest_file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    self.participants = data.get("participants", {})
                    self.current_config_file = os.path.join(config_dir, latest_file)
                    self.language = data.get("language", "ru")
                    self.language_combo.setCurrentText("Русский" if self.language == "ru" else "English")
                    self.update_ui_language()
                    self.update_participant_list()
                    self.log_message(f"Auto-loaded latest config: {latest_file}")
                except Exception as e:
                    self.log_message(f"Error auto-loading config: {str(e)}")

    def change_config_dir(self):
        new_dir = QFileDialog.getExistingDirectory(self, "Select Config Folder", self.settings["config_dir"])
        if new_dir:
            self.settings["config_dir"] = new_dir
            self.config_dir_edit.setText(new_dir)
            self.log_message(TRANSLATIONS[self.language]["folder_changed"].format(new_dir))

    def clear_current_config(self):
        if not self.participants:
            QMessageBox.information(self, "Info", TRANSLATIONS[self.language]["config_empty"])
            return
            
        reply = QMessageBox.question(self, "Confirm", 
                                   TRANSLATIONS[self.language]["confirm_clear"],
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.participants.clear()
            self.current_participant = None
            self.update_participant_list()
            self.score_label.setText(TRANSLATIONS[self.language]["select_participant"])
            self.add_5_button.setEnabled(False)
            self.add_1_button.setEnabled(False)
            self.sub_1_button.setEnabled(False)
            self.sub_5_button.setEnabled(False)
            self.custom_score_button.setEnabled(False)
            self.log_message(TRANSLATIONS[self.language]["config_cleared"])

    def toggle_autosave(self, state):
        self.settings["autosave"] = state == Qt.Checked
        if self.settings["autosave"]:
            self.autosave_timer.start()
            self.autosave_label.setText(TRANSLATIONS[self.language]["autosave_on"])
            self.log_message(TRANSLATIONS[self.language]["autosave_enabled"])
        else:
            self.autosave_timer.stop()
            self.autosave_label.setText(TRANSLATIONS[self.language]["autosave_off"])
            self.log_message(TRANSLATIONS[self.language]["autosave_disabled"])

    def autosave(self):
        if self.participants:
            if not self.current_config_file:
                self.current_config_file = os.path.join(self.settings["config_dir"], f"config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            try:
                with open(self.current_config_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "participants": self.participants,
                        "timestamp": datetime.now().isoformat(),
                        "language": self.language
                    }, f, ensure_ascii=False, indent=2)
                self.log_message(TRANSLATIONS[self.language]["autosave_log"].format(self.current_config_file))
            except Exception as e:
                self.log_message(f"Autosave error: {str(e)}")

    def closeEvent(self, event):
        if self.settings["autosave"]:
            self.autosave()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScoreApp()
    window.show()
    sys.exit(app.exec_())
