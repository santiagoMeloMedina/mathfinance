import tkinter as tk
from tkinter import filedialog

from collections import deque


class DataCSV:
    def __init__(self, divider: str = ","):
        self.divider = divider
        self.__get_file_name_from_window()
        self.__get_array_data()

    def __get_file_name_from_window(self):
        root = tk.Tk()
        root.withdraw()
        self.file_name = filedialog.askopenfilename()

    def __get_array_data(self):
        self.file = open(self.file_name, "r")
        data = deque(self.file.readlines())
        names, enumerated = {}, {}
        first_row = data.popleft().split()[0].split(self.divider)
        for i in range(len(first_row)):
            name = first_row[i]
            enumerated[i] = name
            names[name] = []
        for row in data:
            columns = row.split()[0].split(self.divider)
            for i in range(len(columns)):
                column = columns[i]
                names[enumerated[i]].append(column)

        self.data = names
