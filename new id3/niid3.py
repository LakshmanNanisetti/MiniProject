
# coding: utf-8

# # Improved ID3 algorithm for clinical data classification

# In[64]:


# Import the libraries used
import unicodecsv
from collections import defaultdict
from math import cos,sqrt,log2
import argparse
import numpy as np

parser = argparse.ArgumentParser(description = 'to take data files')
parser.add_argument('-d','--data',
                    help='Name of the dataset file',
                    dest='dataFile',
                    required=True)
args = parser.parse_args()        
# In[65]:


# Read the data set into reader
with open(args.dataFile + '-des.csv', 'rb') as f:
    reader = unicodecsv.DictReader(f)


# In[66]:


diagnosis = []
f = open(args.dataFile + '-des.csv', 'rb')
reader = unicodecsv.DictReader(f)
for row in reader:
    diagnosis.append(row)
f.close()


# In[67]:


# Length of read data set
print(len(diagnosis))
# A tuple in the data set 
diagnosis[0]


# In[68]:


# Data Wrangling: If the tuple contains missing values remove that tuple
def check(data):
    for v in data.values():
        if v=='?':
            return False
    return True


# In[69]:


# clean the data and store it in the cleanedData variable
cleanedData=[]
for diag in diagnosis:
    if check(diag):
        # diag.pop('id')
        cleanedData.append(diag)
    


# In[70]:


# Node in a ID3 tree
class Node:
    def __init__(self,testAttr,predictedClass):
        self.testAttr=testAttr
        self.predictedClass=predictedClass
        self.children={}
    def __str__(self):
        return self.testAttr
                    
                        
        
def printTree(n):
    print(n)
    if len(n.children)==0:
        return
    print('children are:')
    for k,v in n.children.items():
        print(k,v)
    for v in n.children.values():
        printTree(v)


# In[71]:


# Import breastAttr.txt into breastAttr
# The breastAttr contains attributes in the data set and their possible values
with open(args.dataFile + '-datt.txt','r') as f:
    breastAttr=f.read()
s=breastAttr.split('\n')


# In[201]:


# possVals is a dictionary containing attrname and its possible values
possVals={}
for line in s:
    temp=line.split(':')
    possVals[temp[0]]=temp[1].split(',')
possVals


# In[202]:


# From breastClass get the classes present and their respective values
possClassValues=[]
with open(args.dataFile + '-catt.txt','r') as f:
    breastClass=f.read()
classLine=breastClass.split(':')
className = classLine[0]
possClassValues = classLine[1].split(',')


# In[203]:


print(possClassValues,className)


# In[204]:


# Balance function which decides on which attribute the node should split the tree
def entropy(edata):
    temp = defaultdict(int)
    for eavpair in edata:
        temp[eavpair[className]]+=1
    en = len(edata)
    e=1
    for epv in temp.values():
        e*=(epv/en)*log2(epv/en)
    return e


# In[205]:


# IID3 improvisation: balance function to reduce multivariate splits
def balance(attrLen):
    ans=cos(3.5*attrLen-1.5)/1.8
    ans*=log2(sqrt(attrLen+1))
    return abs(ans)


# In[217]:


def getChild(trainData):
    classCount = defaultdict(int)
    for ex in trainData:
        classCount[ex[className]] += 1
    vals = list(classCount.values())
    keys = list(classCount.keys())
    cls = keys[vals.index(max(vals))]
    return Node('',cls)


# In[218]:


# The Improved ID3 algorithm written here as train
# The algorithm return the root of the tree
def train(trainData,attributes):
    e = entropy(trainData)
    if e==0:
        return Node('',trainData[0][className])
    if len(attributes) == 0:
        classCount = defaultdict(int)
        for ex in trainData:
            classCount[ex[className]] += 1
        maxClass= possClassValues[0]
        maxCount= classCount[maxClass]
        for k,v in classCount.items():
            if maxCount<v:
                maxCount = v
                maxClass = k
        return Node('',maxClass)
    info = {}
    gain = {}
    n = len(trainData)
    for attr in attributes:
        attrVals = possVals[attr]
        attrTrainData = {}
        attrTrainData = defaultdict(list)
        for avpair in trainData:
            attrTrainData[avpair[attr]].append(avpair)
        info[attr] = 1
        for attrVal in attrTrainData.values():
            info[attr] += (len(attrVal)/n)*entropy(attrVal)
            if len(attrVals)==0:
                print(attr)
                print(possVals)
            gain[attr] = (e-info[attr])/balance(len(attrVals))
    maxAttr = attributes[0]
    maxGain = gain[maxAttr]
    for k,v in gain.items():
        if maxGain < v:
            maxGain = v
            maxAttr = k
    n=Node(maxAttr,'')
    splitTrainData = defaultdict(list)
    for ex in trainData:
        splitTrainData[ex[maxAttr]].append(ex)
    newAttrs = attributes[:]
    newAttrs.remove(maxAttr)
    allAttrs = possVals[maxAttr][:]
    for splitAttrVal, splitData in splitTrainData.items():
        if splitAttrVal in allAttrs:
            allAttrs.remove(splitAttrVal)
        n.children[splitAttrVal]=train(splitData,newAttrs)
    for att in allAttrs:
        print(maxAttr,att)
        n.children[att] = getChild(trainData)
    return n


# In[219]:


trainSize = len(cleanedData)*4//5
testSize = len(cleanedData) - trainSize
cleanedData = np.random.permutation(cleanedData)
n=train(cleanedData[:trainSize],list(possVals.keys()))


# In[220]:


# Testing function to check the accuracy of the algorithm
def testing1(n,trainData):
    ab=0
    x=0
    for ex in trainData:
        p=n
        try:
            while p.testAttr!='':
                child=ex[p.testAttr]
                p=p.children[child]
            print(p.predictedClass,ex[className])
            if p.predictedClass==ex[className]:
                x+=1
        except:
            ab+=1
    return x,ab


# In[221]:


x, ab=testing1(n,cleanedData[trainSize:])


# In[226]:


print(x,ab)


# In[223]:


print((x)*100/(testSize))


# In[224]:


printTree(n)


# In[173]:


# n=getChild(cleanedData[515:519])


# In[135]:


n.predictedClass

print('accuracy=',(x)*100/(testSize))
