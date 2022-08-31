from typing import Dict, List

import pandas as pd

class FileReader():
    def __init__(self, file_path, skip_header=False):
        self.file_path_ = file_path
        with open(file_path, "r", encoding="utf8", errors="ignore") as file:
            self.lines_total_ = len(file.readlines())

        self.line_count_ = 0
        self.file_handle_ = open(file_path, "r", encoding="utf8", 
            errors="ignore") 

        if skip_header:
            header = self.read_line()

    def lines_total(self):
        return self.lines_total_

    def line_count(self):
        return self.line_count_

    def is_end_of_file(self):
        return self.line_count_ >= self.lines_total_

    def read_line(self):
        if self.is_end_of_file():
            return ""
        else:
            line = self.file_handle_.readline()
            self.line_count_ += 1
            return line

class TableReader():
    def __init__(self, layout : Dict[str, int]):
        """ 
        Layout: Dict[str : int, type] - Column layout
        """
        self.layout_ = layout
        self.data_ = { key: [] for key in layout.keys() }

    def format_entry(self, entry, separator):
        entries = entry.split(separator)
        largest_index = max([ index for ( index, value_type ) 
            in self.layout_.values() ])
        assert len(entries) > largest_index, \
            "Index {0} too large for table.".format(largest_index)

        for identifier, (index, value_type) in self.layout_.items():
            self.data_[identifier].append(value_type(entries[index]))

    def get_data(self):
        return self.data_
