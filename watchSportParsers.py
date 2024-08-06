from abc import ABC, abstractmethod
import struct
import datetime
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog


class ParserInterface(ABC):
    @abstractmethod
    def parse(self, file_path, filter_field=None, filter_value=None):
        pass

def select_file():
        # 创建Tkinter根窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏根窗口

        # 打开文件选择对话框
        file_path = filedialog.askopenfilename()
        return file_path

class ParserInterface(ABC):
    @abstractmethod
    def parse(self, file_path, filter_field=None, filter_value=None):
        pass

class ChartNormalParser(ParserInterface):
    def __init__(self, format_string='<BHHIHHh'):
        self.format_string = format_string
        self.data_size = struct.calcsize(format_string)
        self.data_sets = []

    def parse(self, file_path, filter_field=None, filter_value=None):
        self.read_binary_file(file_path, filter_field, filter_value)
        self.plot_rtc_times()

    def read_binary_file(self, file_path, filter_field=None, filter_value=None):
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(self.data_size)
                if not data:
                    break
                parsed_data = struct.unpack(self.format_string, data)
                if filter_field and filter_value is not None:
                    if not self.apply_filter(parsed_data, filter_field, filter_value):
                        continue
                self.print_parsed_data(parsed_data)
                self.data_sets.append(parsed_data)

    def apply_filter(self, parsed_data, filter_field, filter_value):
        fields = ['version', 'tag', 'heart_rate', 'rtc_time', 'average_speed', 'step_freq', 'altitude']
        field_index = fields.index(filter_field)
        return parsed_data[field_index] == filter_value

    def print_parsed_data(self, parsed_data):
        version, tag, heart_rate, rtc_time, average_speed, step_freq, altitude = parsed_data
        readable_time = datetime.datetime.fromtimestamp(rtc_time).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Version: {version}")
        print(f"Tag: {tag}")
        print(f"Heart Rate: {heart_rate} counts/minute")
        print(f"RTC Time: {rtc_time} ({readable_time})")
        print(f"Average Speed: {average_speed} seconds/hundred meter")
        print(f"Step Frequency: {step_freq}")
        print(f"Altitude: {altitude} meters")
        print("-" * 40)  # 分隔线

    def plot_rtc_times(self, field_in=None):
        fields = ['version', 'tag', 'heart_rate', 'rtc_time', 'average_speed', 'step_freq', 'altitude']
        plt.figure(figsize=(10, 5))
        
        for field in fields:
            field_index = fields.index(field)
            y_datas = [data[field_index] for data in self.data_sets]

            plt.plot(range(len(y_datas)), y_datas, marker='o', linestyle='-')
            plt.xlabel('Index')
            plt.ylabel(f"{field}")
            plt.title(f"{field} vs. Index")
            plt.grid(True)

        plt.show()

def parse_files(filter_field=None, filter_value=None):
    file_path = select_file()

    if file_path:
        # 检查文件名是否以"chart_normal"结尾
        if file_path.endswith("chart_normal"):
            parser = ChartNormalParser()
            parser.parse(file_path, filter_field, filter_value)
        else:
            print("Error: The selected file does not end with 'chart_normal'.")
    else:
        print("No file path selected")