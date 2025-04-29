import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from CustomSlot import CustomSlot
from car import Car
from qjmsUi import Ui_QJMS


class QjmsTool(Ui_QJMS, CustomSlot):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.car_serial = ''
        self.nap_path = ''
        self.pet_path = ''

    def setupUi(self):
        super().setupUi()
        self.toolBar.addAction(self.action_car)
        self.toolBar.addAction(self.action_wgr)
        self.action_car.triggered.connect(self.show_car_page)
        self.action_wgr.triggered.connect(self.show_wgr_page)
        car_page = Car()
        self.setCentralWidget(car_page)  # 切换窗口，改页面对象会被销毁


if __name__ == '__main__':
    # 实例化，传参
    app = QApplication(sys.argv)

    # 创建对象
    mainWindow = QMainWindow()

    # 创建ui，引用AutoGenerateUi文件中的Ui_MainWindow类
    qjms = QjmsTool()

    # 设置窗口名称
    qjms.setWindowTitle('QJMS TOOL')
    qjms.show()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())
