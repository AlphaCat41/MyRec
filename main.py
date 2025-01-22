import subprocess
import sys
import signal
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLCDNumber,
    QMessageBox
) 
from PySide6.QtCore import (
    QTime,
    QTimer,
)

class Recorder():
    def __init__(self):
        self.ffmpeg_process = None

    def run(self):
        command = f'ffmpeg/bin/ffmpeg.exe -y -f dshow -i audio="{"Stereo Mix (Realtek Audio)"}" -f gdigrab -framerate 30 -i desktop -pix_fmt yuv420p -filter:a "volume={"40dB"}" output.mp4'
        self.ffmpeg_process = subprocess.Popen(command, stdin=subprocess.PIPE, text=True)

    def stop(self):
        self.ffmpeg_process.stdin.write("q\n")
        self.ffmpeg_process.communicate()
    
class MyRec(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyRec")
        self.resize(400, 100)

        main_layout = QVBoxLayout()
        content_layout = QHBoxLayout()
        button_layout = QVBoxLayout()

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

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

        content_layout.addWidget(self.lcd_clock)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        content_layout.addLayout(button_layout)
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

        self.reccorder = Recorder()

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