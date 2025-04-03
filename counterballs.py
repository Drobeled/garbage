import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt


class ScoreApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение для подсчёта баллов")
        self.setGeometry(100, 100, 400, 500)
        
        # Словарь для хранения участников и их баллов
        self.participants = {}
        
        # Создаем центральный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Виджеты для добавления участника
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите имя участника")
        main_layout.addWidget(self.name_input)
        
        add_button = QPushButton("Добавить участника")
        add_button.clicked.connect(self.add_participant)
        main_layout.addWidget(add_button)
        
        # Виджеты для управления баллами
        self.participant_list = QListWidget()
        self.participant_list.itemClicked.connect(self.select_participant)
        main_layout.addWidget(QLabel("Список участников:"))
        main_layout.addWidget(self.participant_list)
        
        self.score_label = QLabel("Выберите участника")
        main_layout.addWidget(self.score_label)
        
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
        
        main_layout.addLayout(buttons_layout)
        
        # Текущий выбранный участник
        self.current_participant = None
    
    def add_participant(self):
        name = self.name_input.text().strip()
        if name and name not in self.participants:
            self.participants[name] = 0
            item = QListWidgetItem(name)
            # Сохраняем оригинальное имя в данных элемента
            item.setData(Qt.UserRole, name)
            self.participant_list.addItem(item)
            self.name_input.clear()
    
    def select_participant(self, item):
        # Получаем оригинальное имя из данных элемента
        self.current_participant = item.data(Qt.UserRole)
        self.score_label.setText(f"{self.current_participant}: {self.participants[self.current_participant]} баллов")
        
        # Активируем кнопки после выбора участника
        self.add_5_button.setEnabled(True)
        self.add_1_button.setEnabled(True)
        self.sub_1_button.setEnabled(True)
        self.sub_5_button.setEnabled(True)
    
    def change_score(self, points):
        if self.current_participant:
            self.participants[self.current_participant] += points
            self.score_label.setText(f"{self.current_participant}: {self.participants[self.current_participant]} баллов")
            
            # Обновляем отображение в списке
            for i in range(self.participant_list.count()):
                item = self.participant_list.item(i)
                if item.data(Qt.UserRole) == self.current_participant:
                    item.setText(f"{self.current_participant} ({self.participants[self.current_participant]})")
                    break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScoreApp()
    window.show()
    sys.exit(app.exec_())
