from carSlot import CarSlot
from carUi import Ui_Car


class Car(Ui_Car, CarSlot):
    def __init__(self):
        super().__init__()
        self.car_serial = '未读取车机sn号！！！'
        self.nap_path = ''
        self.pet_path = ''
        self.setupUi()

    def setupUi(self):
        super().setupUi()
        self.get_devices_informatiion()
        self.pushButton_set_battery_threshold.clicked.connect(self.set_battery_shreshold)
        self.horizontalScrollBar_battery_threshold.valueChanged.connect(self.get_battery_threshold)
