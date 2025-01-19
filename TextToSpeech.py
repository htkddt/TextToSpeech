import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QPushButton, QTextEdit, QSlider
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl

from gtts import gTTS
from langdetect import detect
# Test git workflow again
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text-To-Speech Application")
        self.setGeometry(100, 100, 1280, 720)

        # Create layout
        layout = QVBoxLayout()

        # Create text editor
        self.textEdit = QTextEdit(self)
        self.textEdit.setFont(QFont("Time New Roman", 13))
        layout.addWidget(self.textEdit)

        btnLayout = QHBoxLayout()
        # Create push button convert text-to-speech
        btnFont = QFont("Time New Roman", 13)
        btnFont.setBold(True)

        self.btnPlayPause = QPushButton("Play", self)
        self.btnPlayPause.setFont(btnFont)
        self.btnPlayPause.clicked.connect(self.runTTS)

        self.btnStop = QPushButton("Stop", self)
        self.btnStop.setEnabled(False)
        self.btnStop.setFont(btnFont)
        self.btnStop.clicked.connect(self.stopTTS)

        self.btnSave = QPushButton("Save", self)
        self.btnSave.setFont(btnFont)
        self.btnSave.clicked.connect(self.saveTTS)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.setPosition)

        btnLayout.addWidget(self.btnPlayPause)
        btnLayout.addWidget(self.btnStop)
        btnLayout.addWidget(self.slider)
        btnLayout.addWidget(self.btnSave)
        layout.addLayout(btnLayout)

        # Create media
        self.player = QMediaPlayer()
        self.player.positionChanged.connect(self.updatePosition)
        self.player.durationChanged.connect(self.updateDuration)
        self.player.mediaStatusChanged.connect(self.mediaStatusChange)
        self.tempAudioPath = "Temp_audio.mp3"
        self.mediaContent = QMediaContent(QUrl.fromLocalFile(self.tempAudioPath))

        # Init layout
        mainWidget = QWidget()
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

    def mediaStatusChange(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.player.setMedia(QMediaContent())
            if os.path.exists(self.tempAudioPath):
                os.remove(self.tempAudioPath)
            self.btnPlayPause.setText("Play")
            self.btnStop.setEnabled(False)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Information', 
                                     "Are you sure you want to exit?", 
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def runTTS(self):
        # Read text from QTextEdit
        text = self.textEdit.toPlainText()
        if text:
            if (self.btnPlayPause.text() == "Play"):
                lang = detect(text)
                try:
                    tts = gTTS(text, lang=lang)
                    tts.save(self.tempAudioPath)
                    self.player.setMedia(self.mediaContent)
                except Exception as e:
                    print(f"Error processing: {e}")
                    return
                self.player.play()
                self.btnPlayPause.setText("Pause")
                self.btnStop.setEnabled(True)
            elif (self.btnPlayPause.text() == "Pause"):
                if self.player.state() == QMediaPlayer.PlayingState:
                    self.player.pause()
                    self.btnPlayPause.setText("Continue")
            elif (self.btnPlayPause.text() == "Continue"):
                self.player.play()
                self.btnPlayPause.setText("Pause")
        else:
            QMessageBox.warning(self, 'Warning', "Text box is Empty", QMessageBox.Ok)

    def stopTTS(self):
        self.btnPlayPause.setText("Play")
        self.btnStop.setEnabled(False)
        self.player.setMedia(QMediaContent())
        # Delete Temp_audio.mp3
        if os.path.exists(self.tempAudioPath):
            os.remove(self.tempAudioPath)
        self.btnPlayPause.setText("Play")

    def saveTTS(self):
        # Read text from QTextEdit
        text = self.textEdit.toPlainText()
        if text:
            file, _ = QFileDialog.getSaveFileName(self, "Save", "", "MP3 (*.mp3)")
            if file:
              try:
                tts = gTTS(text, lang='vi')
                tts.save(file)
              except Exception as e:
                  print(f"Error processing: {e}")
        else:
            QMessageBox.warning(self, 'Warning', "Text box is Empty", QMessageBox.Ok)

    def updatePosition(self, position):
        self.slider.setValue(position)

    def updateDuration(self, duration):
        self.slider.setRange(0, duration)

    def setPosition(self, position):
        self.player.setPosition(position)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
