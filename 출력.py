from PyQt5 import QtCore, QtGui, QtWidgets
import speech_recognition as sr
import sys


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(804, 447)
        self.Start = QtWidgets.QPushButton(Dialog)
        self.Start.setGeometry(QtCore.QRect(230, 370, 81, 41))
        self.Start.setObjectName("Start")

        self.Exit = QtWidgets.QPushButton(Dialog)
        self.Exit.setGeometry(QtCore.QRect(480, 370, 81, 41))
        self.Exit.setObjectName("Exit")

        self.Fraud = QtWidgets.QProgressBar(Dialog)
        self.Fraud.setGeometry(QtCore.QRect(200, 50, 161, 41))
        self.Fraud.setProperty("value", 24)
        self.Fraud.setObjectName("Fraud")

        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(80, 130, 641, 201))
        self.textBrowser.setObjectName("textBrowser")

        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(430, 50, 121, 41))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.append("안전")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.Start.clicked.connect(self.start_button_clicked)
        self.Exit.clicked.connect(self.exit_button_clicked)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "노피싱"))
        self.Start.setText(_translate("Dialog", "시작"))
        self.Exit.setText(_translate("Dialog", "종료"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

    def start_button_clicked(self):
        while(1):  
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


                
    def exit_button_clicked(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())



# #QThread 클래스 선언하기, QThread 클래스를 쓰려면 QtCore 모듈을 import 해야함.
# class Thread(QThread):
#     #초기화 메서드 구현    
#     def __init__(self, parent): #parent는 WndowClass에서 전달하는 self이다.(WidnowClass의 인스턴스)
#         super().__init__(parent)    
#         self.parent = parent #self.parent를 사용하여 WindowClass 위젯을 제어할 수 있다.
        
#     def run(self):
#         pass
#         #쓰레드로 동작시킬 함수 내용 구현
# class WindowClass(QMainWindow, form_class): 
#     def threadAction(self):
#         x = Thread(self) #self는 WindowClass의 인스턴스, Thread 클래스에서 parent로 전달
#         x.start() #쓰레드 클래스의 run 메서드를 동작시키는 부분