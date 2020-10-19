# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
import xbox
import motor
import time


def scale_number(number):
    return int(round(254 * abs(number)))


# Instantiate the controller
def run_control():
    joy = xbox.Joystick()
    toggleon = False
    while joy.Guide() != 1:
        if joy.Start() == 1:
            toggleon = not toggleon
            motor.writeBlock([0, 0, 0, 0, 0, 0])
            time.sleep(1)
        if toggleon:
            motor_one_dir, motor_two_dir, motor_three_dir = 1, 1, 1
            if joy.leftX() > 0:
                motor_one_dir = 0
            if joy.leftY() > 0:
                motor_two_dir = 0
            if joy.rightY() > 0:
                motor_three_dir = 0
            motor_speeds = [scale_number(joy.leftX()), scale_number(joy.leftY()), scale_number(joy.rightY())]
            motor.writeBlock(
                [motor_one_dir, motor_speeds[0], motor_two_dir, motor_speeds[1], motor_three_dir, motor_speeds[2]])


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 480)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 440, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 161, 101))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Run Xbox Control"))
        self.pushButton.clicked(run_control)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
