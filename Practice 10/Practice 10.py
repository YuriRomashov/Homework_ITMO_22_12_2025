
from PySide6.QtWidgets import QPlainTextEdit,QRadioButton,QButtonGroup,QSizePolicy,QMessageBox,QApplication,QDialog,QLineEdit,QPushButton,QVBoxLayout,QLabel,QGridLayout
from PySide6.QtCore import QThread,Signal,Qt,Slot,QEvent
from PySide6.QtGui import QFont
from thread_main import Thread
import socket,sys

""" 
MainWindow - класс явлющимся основным GUI и клиентом для общения с сервером.
В данном окне реализована логика построения GUI и связь между сервером и клиентом.
Основные функции : вывод информации на экран в отдельное поле,подключение к серверу,запуск игры
"""

class MainWindow(QDialog):
    send_data = Signal(str)
    def __init__(self, parent = None):
        super(MainWindow,self).__init__(parent)
        self.hard_number_max = 10000
        self.normal_number_max = 1000
        self.numbers = None
        self.max_attempts = 10
        self.client_socket = None
        self.newline = '\r\n'

        # Основные виджеты
        self.setWindowTitle("Игра: Угадай число!")
        self.label_name_game = QLabel("Угадай число!")
        self.label_name_game.setFont(QFont('Arial', 20))
        self.label_choose_mode = QLabel("Выберите сложность:")
        self.radio_button_group = QButtonGroup()
        self.radio1 = QRadioButton('Средний')
        self.radio2 = QRadioButton('Сложный')
        self.radio_button_group.addButton(self.radio1, 1)
        self.radio_button_group.addButton(self.radio2, 2)
        self.start_game_btn = QPushButton("Начать игру")
        self.input_field = QLineEdit(placeholderText="Введите число - ")
        self.send_btn = QPushButton("Попробовать угадать")
        self.Chat = QPlainTextEdit(" ")
        self.Chat.setReadOnly(True)
        self.Chat.setFixedSize(450, 250)
        self.input_field.setVisible(False)
        self.send_btn.setVisible(False)
        self.Chat.setVisible(False)
        self.Chat.clear()

        # Установка виджетов в окно
        layout = QGridLayout(self)
        layout.addWidget(self.label_name_game,0,0,alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_choose_mode,1,0,alignment=Qt.AlignmentFlag.AlignBaseline)
        layout.addWidget(self.radio_button_group.button(1),2,0,alignment=Qt.AlignmentFlag.AlignBaseline)
        layout.addWidget(self.radio_button_group.button(2),3,0,alignment=Qt.AlignmentFlag.AlignBaseline)
        layout.addWidget(self.start_game_btn,4,0,alignment=Qt.AlignmentFlag.AlignAbsolute)
        layout.addWidget(self.Chat,0,0,1,2)
        layout.addWidget(self.input_field,1,0)
        layout.addWidget(self.send_btn,1,1)
   
        # Привязка кнопок к функциям
        self.radio_button_group.idClicked.connect(self.Radio_butt_clicked)
        self.start_game_btn.clicked.connect(self.start_game)
        self.send_btn.clicked.connect(self.text_signal_to_thread)

    def start_thread(self):
        """Функция включения потока и подключения поля вывода информации"""
        self.game_thread = Thread(True)
        self.game_thread.sig_Chat.connect(self.Chating)
        self.game_thread.max_number = self.numbers
        self.game_thread.start()

    def text_signal_to_thread(self):
        """Функция общения с сервером(отправка и получение информации)"""
        text = self.input_field.text()
        if text:
            self.send_data.emit(text)
            self.input_field.clear()

        try:
            # Создаем соединение, если его еще нет
            if not self.client_socket:
                self.client_socket = socket.socket()
                self.client_socket.connect(('127.0.0.1', 12345))
            text = text + self.newline
            self.client_socket.send(text.encode())
            reply = self.client_socket.recv(1024).decode()
            self.Chating(f"Ответ: {reply}")
            
            if "Игра остановлена." in reply:
                self.client_socket.close()
                self.client_socket = None
                
        except Exception as e:
            self.Chating(f"Ошибка: {e}")
        
        self.input_field.clear()

    def Radio_butt_clicked(self, id):
        """Функция отвечающая за выбор сложности"""
        if id == 1:
            self.numbers = self.normal_number_max
        else:
            self.numbers = self.hard_number_max
    
    def Change_view(self,flag):
        """Функция изменяющая основной вид экрана"""
        self.label_name_game.setVisible(flag)
        self.label_choose_mode.setVisible(flag)
        self.radio_button_group.button(1).setVisible(flag)
        self.radio_button_group.button(2).setVisible(flag)
        self.start_game_btn.setVisible(flag)
        self.input_field.setVisible(not flag)
        self.send_btn.setVisible(not flag)
        self.Chat.setVisible(not flag)
        self.Chat.clear()

    @Slot(str)
    def Chating(self,status):
        """ Слот для получения и вывода информации от сервера."""
        if "Игра остановлена." in status:
            self.Change_view(True)
            self.adjustSize()                       
            self.game_thread.stop()      
        elif "Извините" in status:
            QMessageBox.warning(self,"Конец игры",status)

        elif "Победа" in status:
            QMessageBox.warning(self,"Конец игры",status)
        
            
        self.Chat.appendPlainText(status + "\r\n")

    def start_game(self):
        """Функция запуска игры и соединения с сервером"""
        self.Change_view(False)
        self.start_thread()
        self.client_socket = socket.socket()
        self.client_socket.connect(('127.0.0.1', 12345))
        reply = self.client_socket.recv(1024).decode()
        self.Chating(f"Ответ: {reply}")


    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())