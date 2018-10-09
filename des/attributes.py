import re
import sys
from operator import itemgetter
from itertools import groupby

class Attribute:
    def __init__(self, name, values, attr_type=0):
        self.name = name
        self.values = values
        self.attr_type = attr_type

    def __str__(self):
        return self.name + ' --> ' + str(self.values)

class Attributes:
    def __init__(self, attribute_file):
        self.attributes = []
        if attribute_file:
            for next_line in attribute_file:
                next_line = re.match("^(.*[^ ]+)\s*:\s*(\S*)\s*$", next_line)
                name = next_line.group(1)
                attr_type = next_line.group(2).split(',')[0]
                values = next_line.group(2).split(',')[1:]
                if attr_type=='1':
                    values = [float(i) for i in values]
                new_attr = Attribute(name, values, attr_type)
                self.attributes.append(new_attr)

    def __getitem__(self, key):
        if isinstance(key, int):
          return self.attributes[key]
        elif isinstance(key, str):
          for attr in self.attributes:
            if attr.name == key:
              return attr
          sys.stderr.write("Erroneous call to __getitem__\n")
          sys.exit(1)

    def __str__(self):
        result = '[\n'
        for attr in self.attributes:
            result += ('  ' + str(attr) + '\n')
        result += ']'
        return result

    def __len__(self):
        return len(self.attributes)

    def all_names(self):
        return [attr.name for attr in self.attributes]

    def discretize(self, class_attr, examples,filename):
        k = len(class_attr.values)
        attrs=self.attributes
        print("Attribute Types:")
        for i in range(len(attrs)):
            print("Attribute: ",attrs[i].name," Type: ",end='')
            if attrs[i].attr_type=='1':
                print("numeric")
            else:
             print("nominal")
        print("No of classes in Classification attribute:",k)
        insts={}
        subinters={}
        counts={}
        num=0
        for i in range(len(attrs)):
            attr = attrs[i].name
            if attr != class_attr.name and attrs[i].attr_type == '1':
                num += 1
                insts[attr] = {}
                subinters[attr] = {}
                counts[attr]={}
                for j in range(k):
                    insts[attr][class_attr.values[j]]=set([])
                    counts[attr][class_attr.values[j]]={}
                #populating data in the dictionary
                for ex in examples.all_examples:
                    insts[attr][ex.values[class_attr.name]].add(ex.values[attr])
                    if ex.values[attr] in counts[attr][ex.values[class_attr.name]]:
                        counts[attr][ex.values[class_attr.name]][ex.values[attr]]+=1
                    else:
                        counts[attr][ex.values[class_attr.name]][ex.values[attr]]=1

                for cls_val in class_attr.values:
                    data=set(insts[attr][cls_val])
                    count=counts[attr][cls_val]
                    # print(count)
                    for csk_val in class_attr.values:
                        if csk_val!=cls_val:
                            # print(counts[attr][csk_val])
                            for m in data:
                                if m in counts[attr][csk_val] and m in count:
                                    # print(m)
                                    # print(count[m])
                                    # print(counts[attr][csk_val][m])
                                    if count[m]<counts[attr][csk_val][m]:
                                    	if m in insts[attr][cls_val]:
                                        	insts[attr][cls_val].remove(m)
                                    if count[m]==counts[attr][csk_val][m]:
                                    	if m in insts[attr][csk_val]:
                                        	insts[attr][csk_val].remove(m)
                            #print(insts[attr][cls_val])

                    data=insts[attr][cls_val]
                    #sorting
                    #insts[attr][cls_val]=sorted(data)
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

                for cls_val in class_attr.values:
                    intrvl=[]
                    for m in subinters[attr][cls_val]:
                        intrvl+=m
                    if intrvl:
                    	subinters[attr][cls_val]=(min(intrvl),max(intrvl))

        print(insts)
        #print(counts)
        print(subinters)
        
        datt_file=open(filename+'-datt.txt','w')
        for x in attrs:
            res=x.name+':'
            if x.attr_type == '1':
                ranges = list(subinters[x.name].values())
                for i in ranges:
                    if str(i)[1:-1]!='':
                        res+=str(i)[1:-1].replace(',','_').replace(' ','')+','
                datt_file.write(res[:-1]+'\n')
            else:
                res+=str(x.values)[1:-1].replace(' ','').replace('\'','')
                datt_file.write(res+'\n')
        datt_file.close()

        d_set=open(filename+'-des.csv','w')
        res=''
        for x in attrs:
            res+=x.name+','
        d_set.write(res[:-1]+'\n')
        for ex in examples.all_examples:
            res=''
            for x in attrs:
                if x.attr_type == '1':
                    ex.get_value(x.name)
                    ranges = list(subinters[x.name].values())
                    rangeArrs = list(insts[x.name].values())
                    for i in range(len(ranges)):
                        if ex.get_value(x.name) in rangeArrs[i]:
                            ex.values[x.name] = str(ranges[i])[1:]
                            ex.values[x.name] = ex.values[x.name][:-1].replace(',','_').replace(' ','')
                            res+=str(ex.values[x.name])+','
                else:
                    res+=str(ex.values[x.name])+','
            d_set.write(res[:-1]+'\n')
        d_set.close()


                    



                


