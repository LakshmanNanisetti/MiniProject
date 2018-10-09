import re
import sys
from math import log
class Example:
    def __init__(self, values, attributes):
        self.values = {}
        for i in range(len(attributes)):
            value = values[i]
            attr = attributes.attributes[i]
            if attr.attr_type=='1':
                value=float(value)
            self.values[attr.name] = value
    def get_value(self, attr):
        if isinstance(attr, str):
            return self.values[attr]
        else:
            return self.values[attr.name]

class DataSet:
    def __init__(self, data_file, attributes):
        self.all_examples = []
        if data_file:
            for next_line in data_file:
                next_line = next_line.rstrip()
                next_line = re.sub(".*:(.*)$", "\\1", next_line)
                attr_values = next_line.split(',')
                new_example = Example(attr_values, attributes)
                self.all_examples.append(new_example)

    def __len__(self):
        return len(self.all_examples)

    def __getitem__(self, key):
        return self.all_examples[key]

    def append(self, example):
        self.all_examples.append(example)