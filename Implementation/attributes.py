"""
File:           attributes.py

Specifies an interface for storing information about attributes, including reading them from a file in
the format described in section 1. Note that attributes are sometimes treated as ordered (when reading in examples and
mapping the values to attributes), and sometimes treated as keyed (when accessing attributes to retrieve the possible
values).
"""
import re
import sys
from operator import itemgetter
from itertools import groupby

class Attribute:
    'A single attribute description: name + permissible values'

    def __init__(self, name, values, attr_type=0):
        self.name = name
        self.values = values
        self.attr_type = attr_type

    def __str__(self):
        return self.name + ' --> ' + str(self.values)


class Attributes:
    """An ordered collection of attributes and values"""

    # Create a new instance of an attribute collection. If a file is
    # specified, use it to initialize the collection from that file.
    # The expected file format is:
    # attr-name:value[,value]...
    def __init__(self, attribute_file=False):
        self.attributes = []
        if attribute_file:
            line_num = 1
            for next_line in attribute_file:
                valid_line = re.match("^(.*[^ ]+)\s*:\s*(\S*)\s*$", next_line)
                if not valid_line:
                    sys.stderr.write("%s: %d: Failed to parse\n" %
                               (attribute_file.name, line_num))
                    sys.exit(1)
                name = valid_line.group(1)
                attr_type = valid_line.group(2).split(',')[0]
                values = valid_line.group(2).split(',')[1:]
                if attr_type=='1':
                    values = [float(i) for i in values]
                new_attr = Attribute(name, values, attr_type)
                self.attributes.append(new_attr)
                line_num += 1

    # Implement the [] operator. If an index is specified, return the
    # corresponding attribute. This is useful for correlating an attribute
    # to a value from an example, where we don't know the attribute's
    # name, but we have the order from the example. A string can also
    # be used as an index to retrieve the attribute with the specified
    # name.
    def __getitem__(self, key):
        if isinstance(key, int):
          return self.attributes[key]
        elif isinstance(key, str):
          for attr in self.attributes:
            if attr.name == key:
              return attr
          sys.stderr.write("Erroneous call to __getitem__\n")
          sys.exit(1)

    def __len__(self):
        return len(self.attributes)

    def __str__(self):
        result = '[\n'
        for attr in self.attributes:
            result += ('  ' + str(attr) + '\n')
        result += ']'
        return result

    def __copy__(self):
        new_instance = Attributes()
        new_instance.attributes = self.attributes[:]
        return new_instance

    def all_names(self):
        return [attr.name for attr in self.attributes]

    # If the key is a name, remove the attribute(s) with that name. If the
    # key is an attribute, remove that attribute.
    def remove(self, key):
        if isinstance(key, str):
            for attr in self.attributes:
                if attr.name == key:
                    self.attributes.remove(attr)
        else:
            self.attributes.remove(key)
    """
    a method to descritize numeric attributes to nominal

    """
    def discretize(self, class_attr, examples,debug=False):
        k = len(class_attr.values)
        attrs=self.attributes
        if debug is True:
            print("Attribute Types:")
            for i in range(len(attrs)):
                print("Attribute: ",attrs[i].name," Type: ",end='')
                if attrs[i].attr_type=='1':
                    print("numeric")
                else:
                 print("nominal")
            print("No of classes in Classification attribute:",k)
        insts={}
        inters={}
        subinters={}
        num=0
        for i in range(len(attrs)):
            attr = attrs[i].name
            if attr != class_attr.name and attrs[i].attr_type == '1':
                num += 1
                insts[attr] = {}
                inters[attr] = {}
                subinters[attr] = {}
                for j in range(k):
                    insts[attr][class_attr.values[j]]=set([])
                #populating data in the dictionary
                for ex in examples.all_examples:
                    insts[attr][ex.values[class_attr.name]].add(ex.values[attr])

                for j in range(k):
                    cls_val=class_attr.values[j]
                    data=insts[attr][cls_val]
                    #sorting
                    insts[attr][cls_val]=sorted(data)
                    #min and max
                    inters[attr][cls_val]=[min(data) ,max(data)]
                    #init of subintervels
                    subinters[attr][cls_val]=[]

                    #calculating numeric continuity
                    #https://stackoverflow.com/questions/2154249/identify-groups-of-continuous-numbers-in-a-list
                    for _, g in groupby(enumerate(data), lambda x:x[0]-x[1]):
                        lst=list(map(itemgetter(1), g))
                        if len(lst)==1:
                            #single data point is added in subintervels
                            subinters[attr][cls_val].append(lst)
                        else:
                            #range is added as subintervels
                            subinters[attr][cls_val].append([min(lst),max(lst)])
        if debug is True:
            print("seperation of values on clasification class:")
            print(insts)
            print("min max:")
            print(inters)
            print("sub inters:")
            print(subinters)
        #todo
        """
        combine single datapionts with nearest intervel

        sort DATA based on the attribue in each cls_val 
        """