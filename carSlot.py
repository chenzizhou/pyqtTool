import json
import os
import re
import shutil
from time import sleep


class CarSlot:
    def print_result(self, result):
        self.textEdit_result.clear()
        self.textEdit_result.setText(result)

    def get_devices_informatiion(self):
        get_all_devices_information_cmd = 'adb devices -l'
        get_all_devices_information = []
        result = os.popen(get_all_devices_information_cmd).readlines()
        pattern = re.compile(pattern=r'([A-Z0-9]*)\s*device product:(.*?) ')
        self.nap_path = '在代码中请添加对应车型{}！！！！！'
        self.pet_path = '在代码中请添加对应车型{}！！！！！'
        for line in result:
            data = re.match(pattern, line)
            if data:
                get_all_devices_information.append({'serial': data.group(1), 'device': data.group(2)})
                if data.group(2) == 'SGLA-X6S':
                    self.carType = 'X6'
                    self.car_serial = data.group(1)
                    self.nap_path = '/hw_product/etc/json/intelligence/use_mode/nap_mode.json'
                    self.pet_path = '/hw_product/etc/json/intelligence/use_mode/pet_mode.json'
                    print('设备为X6')
                elif data.group(2) == 'PRVC-F3':
                    self.carType = 'F3'
                    self.car_serial = data.group(1)
                    self.nap_path = "/hw_product/etc/json/intelligence/use_mode/nap_mode.json"
                    self.pet_path = '/hw_product/etc/json/intelligence/use_mode/pet_mode.json'
                    print('设备为为F3')
                elif data.group(2) == 'ICHU3200F2-ADV':
                    self.carType = 'F2A'
                    self.car_serial = data.group(1)
                    self.nap_path = 'hw_product/hw_oem/submodel/ICHU3200F2-ADV/F2A/json/intelligence/use_mode/nap_mode.json'
                    self.pet_path = 'hw_product/hw_oem/submodel/ICHU3200F2-ADV/F2A/json/intelligence/use_mode/pet_mode.json'
                    print('设备为为F2A')
                elif data.group(2) == 'ICHU3200X2-ADV':
                    self.carType = 'X2'
                    self.car_serial = data.group(1)
                    self.nap_path = '/hw_product/etc/json/intelligence/use_mode/nap_mode.json'
                    self.pet_path = '/hw_product/etc/json/intelligence/use_mode/pet_mode.json'
                    print('设备为为X2')

        print(get_all_devices_information)
        self.textEdit_all_devices_information.setText(
            str(get_all_devices_information) + f'\n小憩json路径：\n{self.nap_path}' + f'\n关怀json路径：\n{self.pet_path}')

    def get_battery_threshold(self, value):
        self.lineEdit_battery_threshold.setText(str(value))

    def set_battery_shreshold(self):
        tip_content = ''
        self.pushButton_set_battery_threshold.setEnabled(False)
        mode_validate_cmd = f'adb -s {self.car_serial} shell pkill intelligencehap'  # push文件必须执行此命令才能生效
        remount_cmd = f'adb -s {self.car_serial} remount'
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
                                pattern = re.compile(r'BatteryLevel (.*?) (.*?) && PowerType')
                                result = re.search(pattern, condition)
                                if result:
                                    print('修改前内容：', condition)
                                    repl = 'BatteryLevel {} {}  && PowerType'.format(result.group(1),
                                                                                     self.lineEdit_battery_threshold.text())
                                    condition = re.sub(pattern, repl, condition)
                                    print('修改后内容：', condition)
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

            # 关怀操作
            if self.checkBox_pet.isChecked():
                # 拉取文件
                pull_nap_json_cmd = f'adb -s {self.car_serial} pull {self.pet_path} pet_mode.json'
                print('执行拉取文件：', pull_nap_json_cmd)
                os.popen(pull_nap_json_cmd)
                sleep(2)
                print('拉取文件成功')
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
                                pattern = re.compile(r'BatteryLevel (.*?) (.*?) && PowerType')
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
                print('给于推送权限：', remount_cmd)
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
        self.pushButton_set_battery_threshold.setEnabled(True)
