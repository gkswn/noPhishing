import typing
from PyQt5.QtCore import QObject
import speech_recognition as sr
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *


#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("C:\\Users\\안한주\\Desktop\\노피싱\\first.ui")[0]
print(form_class) #form_class는 Ui_Dialog라는 class이다.


#QThread 클래스 선언하기, QThread 클래스를 쓰려면 QtCore 모듈을 import 해야함.
class Thread1(QThread):
    #초기화 메서드 구현  
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    
    def STT(self):
        try:
            self.textBrowser.append("보이스피싱 여부 확인을 시작합니다.")
            r = sr.Recognizer()

            with sr.Microphone() as source:
                self.textBrowser.append("말씀해주세요: ")
                audio = r.listen(source)
                
            result = r.recognize_google(audio, language='ko-KR')
            self.textBrowser.append(result)
        except:
            self.textBrowser.append("오류가 발생했습니다.")


#메인 윈도우 클래스
class WindowClass(QMainWindow, form_class) :
    #초기화 메서드
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        #pushButton (시작버튼)을 클릭하면 아래 fuctionStart 메서드와 연결 됨.
        self.Start.clicked.connect(self.functionStart)
        # self.Exit.clicked.connect(self.functionExit) 

    # 시작버튼을 눌렀을 때 실행되는 메서드
    def functionStart(self):
        stt = Thread1(self)
        stt.STT()

    # def functionExit(self):
    #     reply = QMessageBox.question(self, "종료 확인", "종료 하시겠습니까?", QMessageBox.Yes | QMessageBox.No)

    #     if reply == QMessageBox.Yes:
    #         QApplication.quit()  # 어플리케이션을 종료합니다.


#코드 실행시 GUI 창을 띄우는 부분
#__name__ == "__main__" : 모듈로 활용되는게 아니라 해당 
# .py파일에서 직접 실행되는 경우에만 코드 실행
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()