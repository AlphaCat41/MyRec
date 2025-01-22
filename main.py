import subprocess
import sys
import pyaudio
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLCDNumber,
    QMessageBox,
    QComboBox,
    QLabel
) 
from PySide6.QtCore import (
    QTime,
    QTimer,
)

class Recorder():
    def __init__(self):
        self.ffmpeg_process = None
        self.sound_device = None

    def run(self):
        command = f'ffmpeg/bin/ffmpeg.exe -y -f dshow -i audio="{self.sound_device}" -f gdigrab -framerate 30 -i desktop -pix_fmt yuv420p -filter:a "volume={"40dB"}" output.mp4'
        self.ffmpeg_process = subprocess.Popen(command, stdin=subprocess.PIPE, text=True)

    def stop(self):
        self.ffmpeg_process.stdin.write("q\n")
        self.ffmpeg_process.communicate()
        
    def set_sound_device(self, name):
        self.sound_device = name

class MyRec(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyRec")
        self.resize(400, 100)

        main_layout = QVBoxLayout()
        content_layout = QHBoxLayout()
        button_layout = QVBoxLayout()
        option_layout = QHBoxLayout()

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        self.sound_device_list = QComboBox()
        select_sound_label = QLabel("Select Sound Device: ")
        self.sound_device_list.setEditable(True)
        self.add_items_to_combobox()
        self.sound_device_list.currentTextChanged.connect(self.on_text_changed)

        self.stop_button.setDisabled(True)
        self.start_button.setDisabled(False)

        self.start_button.clicked.connect(self.click_start)
        self.stop_button.clicked.connect(self.click_stop)

        self.time = QTime(0, 0, 0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_time)

        self.lcd_clock = QLCDNumber()
        self.lcd_clock.setDigitCount(8)
        self.lcd_clock.display(self.time.toString("hh:mm:ss"))

        option_layout.addWidget(select_sound_label)
        option_layout.addWidget(self.sound_device_list)
        content_layout.addWidget(self.lcd_clock)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        content_layout.addLayout(button_layout)
        main_layout.addLayout(option_layout)
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

        self.reccorder = Recorder()
        self.reccorder.set_sound_device(self.sound_device_list.currentText())

    def on_text_changed(self, text):
        self.sound_device_list.setCurrentText(text)
        self.reccorder.set_sound_device(self.sound_device_list.currentText())

    def add_items_to_combobox(self):
        p = pyaudio.PyAudio()

        device_count = p.get_device_count()
        for i in range(device_count):
            device_info = p.get_device_info_by_index(i)
            # print(f"Device {i}: {device_info['name']} - {device_info['maxInputChannels']} input channels, {device_info['maxOutputChannels']} output channels")
            self.sound_device_list.addItem(device_info['name'])
            

    def show_time(self):
        self.time = self.time.addSecs(1)
        self.lcd_clock.display(self.time.toString("hh:mm:ss"))

    def click_start(self):
        try:
            self.reccorder.run()

        except Exception as e:
            self.message_box(-1, e)

        self.timer.start(1000)
        self.stop_button.setDisabled(False)
        self.start_button.setDisabled(True)
    
    def click_stop(self):
        self.timer.stop()
        try:
            self.reccorder.stop()

            self.clear_time()
            self.stop_button.setDisabled(True)
            self.start_button.setDisabled(False)  
            self.message_box(0, "The video has been successfully saved.")    

        except Exception as e:
            self.message_box(-1, e)


    def clear_time(self):
        self.timer = QTimer()
        self.time = QTime(0, 0, 0)
        self.timer.timeout.connect(self.show_time)
        self.lcd_clock.display(self.time.toString("hh:mm:ss"))

    def message_box(self, type, msg):
        msgBox = QMessageBox()
        match(type):
            case -1:
                msgBox.setIcon(QMessageBox.Icon.Critical)  
                msgBox.setText(f"{msg}")
                msgBox.exec()

            case 0:
                msgBox.setIcon(QMessageBox.Icon.Information)  
                msgBox.setText(f"{msg}")
                msgBox.exec()

if __name__== "__main__":
    app = QApplication()

    myRec = MyRec()
    myRec.show()

    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec())