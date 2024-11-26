import os
import sys





def get_path(relative_path):
    try:
        base_path = sys._MEIPASS  # pyinstaller打包后的路径
    except AttributeError:
        base_path = os.path.abspath(".")  # 当前工作目录的路径
        # print(base_path)
    return os.path.normpath(os.path.join(base_path, relative_path))  # 返回实际路径
class CustomSlot:
    # 建议现在AutoGenerate模块中把槽函数调通后在移植过来
    def set_advance(self):
        os.popen(get_path('asserts/setAdvance.bat'))
        result='已初始化用户数据'
        self.print_result(result)

    def clearData(self):
        os.popen(get_path('asserts/clear.bat'))
        result = "已经清除用户数据"
        self.print_result(result)

    def play(self):
        cmd = 'adb shell input keyevent 85'  # 方控暂停/播放
        value = self.pushButton_play.text()
        if value == "播放":
            self.pushButton_play.setText("暂停")
        if value == "暂停":
            self.pushButton_play.setText("播放")
        os.popen(cmd)
        result = '当前声源为：{}'.format(value)
        print(result)
        self.print_result(result)

    def press_or_release_brake(self):
        try:
            cmd = 'adb shell /system/bin/motivate -n Vehicle.Chassis.Brake.PedalStatus -m 1 -v {} -s 3'
            value = self.pushButton_brake.text()
            if value == "踩刹车":
                brake = 1
                self.pushButton_brake.setText("松刹车")
                os.popen(
                    cmd.format(brake))
            else:
                self.pushButton_brake.setText("踩刹车")
                brake = 0
                os.popen(cmd.format(brake))
            result='当前:{}'.format(value)
            self.print_result(result)
        except Exception as e:
            print(e)


    # 切换档位
    def shift_gears(self):
        cmd = 'adb shell /system/bin/motivate -n Vehicle.Drivetrain.Transmission.Gear -m 1 -v {} -s 1'
        value = self.comboBox_gears.currentText()
        if value == "P":
            gears = 1
        elif value == "N":
            gears = 2
        elif value == "R":
            gears = 3
        elif value == "D":
            gears = 4
        os.popen(cmd.format(gears))
        result = '当前档位设置为：{}'.format(value)
        print(result)
        self.print_result(result)

    def get_speed(self):
        speed = self.horizontalScrollBar_speed.value()
        self.lineEdit_speed.setText(str(speed))

    def change_speed(self):
        cmd = 'adb shell /system/bin/motivate -n Vehicle.Body.Speed -m 2 -t 200 -v {} -s 9'
        speed = self.lineEdit_speed.text()
        os.popen(cmd.format(speed))
        result = '当前车度设置为：{}'.format(speed)
        print(result)
        self.print_result(result)

    # 滑块设置、获取电量
    def get_battery(self):
        value = self.horizontalScrollBar_battery.value()
        self.lineEdit_battery.setText(str(value))

    # 修改电量
    def change_battery(self):
        cmd = 'adb shell /system/bin/motivate -n Vehicle.Drivetrain.BatteryManagement.BatteryCapacity -m 1 -v {} -s 9'
        battery = self.lineEdit_battery.text()
        os.popen(cmd.format(battery))
        result = '当前电量设置为：{}'.format(battery)
        print(result)
        self.print_result(result)

    def get_sound(self):
        sound = self.horizontalScrollBar_sound.value()
        self.lineEdit_sound.setText(str(sound))

    def change_sound(self):
        cmd = 'adb shell /system/bin/motivate -n Vehicle.Drivetrain.BatteryManagement.BatteryCapacity -m 1 -v {} -s 9'
        sound = self.lineEdit_sound.text()
        # os.popen(cmd.format(sound))
        result = '需提供命令!!!!!!!!!'
        print(result)
        self.print_result(result)

    def print_result(self,result):
        self.textEdit_result.clear()
        self.textEdit_result.setText(result)


