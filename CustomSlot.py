import json
import os
import re
import shutil
import sys
from time import sleep

from PyQt5.QtWidgets import QVBoxLayout

from car import Car
from wgr import Wgr


def get_path(relative_path):
    try:
        base_path = sys._MEIPASS  # pyinstaller打包后的路径
    except AttributeError:
        base_path = os.path.abspath(".")  # 当前工作目录的路径
        # print(base_path)
    return os.path.normpath(os.path.join(base_path, relative_path))  # 返回实际路径


class CustomSlot:
    # 建议先在AutoGenerate模块中把槽函数调通后在移植过来
    def set_advance(self):
        os.popen(get_path('asserts/setAdvance.bat'))
        result = '已初始化用户数据'
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
            result = '当前:{}'.format(value)
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

    def chang_screen(self):
        cmd = 'adb shell setprop sys.hw_mc.power.screen_enable.0 {}'
        value = self.pushButton_screen.text()
        if value == '息屏':
            screen = 1
            self.pushButton_screen.setText('亮屏')
        else:
            screen = 0
            self.pushButton_screen.setText('息屏')
        os.popen(cmd.format(screen))
        result = '当前屏幕状态：{}'.format(value)
        self.print_result(result)

    def print_result(self, result):
        self.textEdit_result.clear()
        self.textEdit_result.setText(result)

    def get_battery_threshold(self, value):
        self.lineEdit_battery_threshold.setText(str(value))

    # def get_devices_informatiion(self):
    #     try:
    #         get_all_devices_information_cmd = 'adb devices -l'
    #         get_all_devices_information = []
    #         result = os.popen(get_all_devices_information_cmd).readlines()
    #         pattern = re.compile(pattern=r'([A-Z0-9]*)\s*device product:(.*?) ')
    #         if result[1] == '\n':
    #             self.car_serial = '未读取到设备信息，请确认设备和电脑usb是否连通！！！'
    #             get_all_devices_information = '未读取到设备信息，请确认设备和电脑usb是否连通！！！'
    #         else:
    #             for line in result:
    #                 data = re.match(pattern, line)
    #                 if data:
    #                     get_all_devices_information.append({'serial': data.group(1), 'device': data.group(2)})
    #                     if data.group(2) == 'SGLA-X6S':
    #                         self.carType = 'X6'
    #                         self.car_serial = data.group(1)
    #                         self.nap_path = '/hw_product/etc/json/intelligence/use_mode/nap_mode.json'
    #                         self.pet_path = '/hw_product/etc/json/intelligence/use_mode/pet_mode.json'
    #                         print('设备为X6')
    #                     elif data.group(2) == 'PRVC-F3':
    #                         self.carType = 'F3'
    #                         self.car_serial = data.group(1)
    #                         self.nap_path = "/hw_product/etc/json/intelligence/use_mode/nap_mode.json"
    #                         self.pet_path = '/hw_product/etc/json/intelligence/use_mode/pet_mode.json'
    #                         print('设备为为F3')
    #                     elif data.group(2) == 'ICHU3200F2-ADV':
    #                         self.carType = 'F2A'
    #                         self.car_serial = data.group(1)
    #                         self.nap_path = 'hw_product/hw_oem/submodel/ICHU3200F2-ADV/F2A/json/intelligence/use_mode/nap_mode.json'
    #                         self.pet_path = 'hw_product/hw_oem/submodel/ICHU3200F2-ADV/F2A/json/intelligence/use_mode/pet_mode.json'
    #                         print('设备为为F2A')
    #                     elif data.group(2) == 'ICHU3200X2-ADV':
    #                         self.carType = 'X2'
    #                         self.car_serial = data.group(1)
    #                         self.nap_path = '/hw_product/etc/json/intelligence/use_mode/nap_mode.json'
    #                         self.pet_path = '/hw_product/etc/json/intelligence/use_mode/pet_mode.json'
    #                         print('设备为为X2')
    #                     else:
    #                         self.car_serial = data.group(1)
    #                         self.nap_path = '在代码中请添加对应车型{}及文件路径！！！！！'
    #                         self.pet_path = '在代码中请添加对应车型车型{}及文件路径！！！！！'
    #     except Exception as e:
    #         self.car_serial = '未读取车机sn号！！！'
    #     print(get_all_devices_information)
    #     self.textEdit_all_devices_information.setText(
    #         str(get_all_devices_information) + f'\n小憩json路径：\n{self.nap_path}' + f'\n关怀json路径：\n{self.pet_path}')

    def set_battery_shreshold(self):
        try:
            mode_validate_cmd = f'adb -s {self.car_serial} shell pkill intelligencehap'  # push文件必须执行此命令才能生效
            remount_cmd = f'adb -s {self.car_serial} remount'
            tip_content = ''
            if self.checkBox_open.isChecked() or self.checkBox_exit.isChecked():
                if self.checkBox_nap.isChecked():
                    # 拉取文件
                    pull_nap_json_cmd = f'adb -s {self.car_serial} pull {self.nap_path} nap_mode.json'
                    print('执行拉取文件：', pull_nap_json_cmd)
                    os.popen(pull_nap_json_cmd)
                    sleep(2)
                    print('拉取文件成功')
                    # 备份文件
                    shutil.copy('nap_mode.json', 'nap_mode_bak.json')
                    sleep(2)
                    # 读取json文件
                    with open('nap_mode.json', 'r', encoding='utf8') as f:
                        data = json.load(f)
                        f.close()
                    tasks = data.get('tasks')
                    for task in tasks:
                        if self.checkBox_open.isChecked():
                            if task.get('name') in ['OpenNapMode', "NapMode_CheckPrerequisites", 'PreCheck']:
                                nextTasks = task.get('nextTasks')
                                for next_task in nextTasks:
                                    condition = next_task.get('condition')
                                    pattern = re.compile(r'BatteryLevel (.*?) (.*?) && PowerType')
                                    result = re.search(pattern, condition)
                                    if result:
                                        print('修改前内容：', condition)
                                        repl = 'BatteryLevel {} {}  && PowerType'.format(result.group(1),
                                                                                         self.lineEdit_battery_threshold.text())
                                        condition = re.sub(pattern, repl, condition)
                                        print('修改后内容：', condition)
                                        next_task['condition'] = condition
                        elif self.checkBox_exit.isChecked():
                            # 'WaitBroadcast','MonitorExitSignal', 'CloseNapMode_Difference' X6
                            if task.get('name') in ["NapMode_WaitForDriverSeatSignal", 'NapModeWaitDelayTimeEnd',
                                                    'NapMode_MonitorCloseModeAndDriverSeatSignal',
                                                    'NapMode_CloseNapModeWithDriverSeat', 'WaitBroadcast',
                                                    'MonitorExitSignal',
                                                    'CloseNapMode_Difference']:
                                nextTasks = task.get('nextTasks')
                                for next_task in nextTasks:
                                    condition = next_task.get('condition')
                                    pattern = re.compile(r'BatteryLevel (.*) (.*?) && PowerType')
                                    result = re.search(pattern, condition)
                                    if result:
                                        repl = 'BatteryLevel {} {}  && PowerType'.format(result.group(1),
                                                                                         self.lineEdit_battery_threshold.text())
                                        condition = re.sub(pattern, repl, condition)
                                        next_task['condition'] = condition
                    with open('nap_mode.json', 'w', encoding='utf8') as f:
                        json.dump(data, f, ensure_ascii=False)
                        sleep(5)
                    print('给于推送权限:', remount_cmd)
                    os.popen(remount_cmd)
                    sleep(1)
                    push_nap_json_cmd = f'adb -s {self.car_serial} push nap_mode.json {self.nap_path}'
                    print('执行推送命令：', push_nap_json_cmd)
                    data = os.popen(push_nap_json_cmd).read()
                    sleep(3)
                    print(data)
                    os.popen(mode_validate_cmd)
                    tip_content += '小憩模式电量阈值设置成功\n'

                if self.checkBox_pet.isChecked():
                    # 拉取文件
                    pull_nap_json_cmd = f'adb -s {self.car_serial} pull {self.pet_path} pet_mode.json'
                    os.popen(pull_nap_json_cmd)
                    sleep(2)
                    # 备份文件
                    shutil.copy('pet_mode.json', 'pet_mode_bak.json')
                    sleep(2)
                    # 读取json文件
                    with open('pet_mode.json', 'r', encoding='utf8') as f:
                        data = json.load(f)
                    tasks = data.get('tasks')
                    for task in tasks:
                        if self.checkBox_open.isChecked():
                            # OpenPetMode F2A
                            # PreCheck X6
                            if task.get('name') in ['OpenPetMode', 'PreCheck']:
                                nextTasks = task.get('nextTasks')
                                for next_task in nextTasks:
                                    condition = next_task.get('condition')
                                    pattern = re.compile(r'BatteryLevel (.*?) (.*?) && PowerType')
                                    result = re.search(pattern, condition)
                                    if result:
                                        print('修改前内容：', condition)
                                        repl = 'BatteryLevel {} {}  && PowerType'.format(result.group(1),
                                                                                         self.lineEdit_battery_threshold.text())
                                        condition = re.sub(pattern, repl, condition)
                                        print('修改后内容：', condition)
                                        next_task['condition'] = condition
                        elif self.checkBox_exit.isChecked():
                            if task.get('name') in ['MonitorCloseSignal', 'WaitBroadcast', 'MonitorExitSignal',
                                                    'CloseNapMode_Difference']:
                                nextTasks = task.get('nextTasks')
                                for next_task in nextTasks:
                                    condition = next_task.get('condition')
                                    pattern = re.compile(r'BatteryLevel (.*) (.*?) && PowerType')
                                    result = re.search(pattern, condition)
                                    if result:
                                        print('修改前内容：', condition)
                                        repl = 'BatteryLevel {} {}  && PowerType'.format(result.group(1),
                                                                                         self.lineEdit_battery_threshold.text())
                                        condition = re.sub(pattern, repl, condition)
                                        print('修改后内容：', condition)
                                        next_task['condition'] = condition
                    with open('pet_mode.json', 'w', encoding='utf8') as f:
                        json.dump(data, f, ensure_ascii=False)
                        sleep(5)
                    remount_cmd = f'adb -s {self.car_serial} remount'
                    print('给于推送权限......')
                    os.popen(remount_cmd)
                    sleep(1)
                    push_pet_json_cmd = f'adb -s {self.car_serial} push pet_mode.json {self.pet_path}'
                    print('执行推送命令：', push_pet_json_cmd)
                    os.popen(push_pet_json_cmd)
                    sleep(2)
                    print('推送成功')
                    data = os.popen(mode_validate_cmd).read()
                    print(data)
                    tip_content += '关怀模式电量阈值设置成功\n'
                self.print_result(tip_content)
                print(tip_content)
        except Exception as e:
            print('出现错误：', e)
            self.print_result('出现错误：' + str(e))

    def show_car_page(self):
        # qv = QVBoxLayout()
        page = Car()
        # qv.addWidget(page)
        # self.setLayout(qv)
        self.setCentralWidget(page)
        return page

    def show_wgr_page(self):
        page = Wgr()
        self.setCentralWidget(page)
