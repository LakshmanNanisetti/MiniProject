
# coding: utf-8

# # Improved ID3 algorithm for clinical data classification

# In[1]:


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
# parser.add_argument('-a','--attributes',
#                     help='Name of the attributes file',
#                     dest='dattFile',
#                     required=True)
# parser.add_argument('-c','--class',
#                     help='Name of the class file',
#                     dest='cattFile',
#                     required=True)                                     
args = parser.parse_args()                    
# In[10]:


diagnosis = []
print(args.dataFile)
f = open(args.dataFile + '-des.csv', 'rb')
reader = unicodecsv.DictReader(f)
for row in reader:
    diagnosis.append(row)
f.close()


# In[14]:


# Length of read data set
print(len(diagnosis))
# A tuple in the data set 
diagnosis[0]


# In[15]:


# Data Wrangling: If the tuple contains missing values remove that tuple
def check(data):
    for v in data.values():
        if v=='?':
            return False
    return True


# In[17]:


# clean the data and store it in the cleanedData variable
cleanedData=[]
for diag in diagnosis:
    if check(diag):
        cleanedData.append(diag)
    


# In[18]:


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
    if not isinstance(n,Node) or len(n.children)==0:
        return
    print('children are:')
    for k,v in n.children.items():
        print(k,v)
    for v in n.children.values():
        printTree(v)


# In[25]:


# Import breastAttr.txt into breastAttr
# The breastAttr contains attributes in the data set and their possible values
with open(args.dataFile + '-datt.txt','r') as f:
    breastAttr=f.read()
s=breastAttr.split('\n')


# In[27]:


# possVals is a dictionary containing attrname and its possible values
possVals={}
for line in s:
    temp=line.split(':')
    possVals[temp[0]]=temp[1].split(',')
possVals


# In[30]:


# From breastClass get the classes present and their respective values
possClassValues=[]
with open(args.dataFile + '-catt.txt', 'r') as f:
    breastClass=f.read()
classLine=breastClass.split(':')
className = classLine[0]
possClassValues = classLine[1].split(',')


# In[31]:


# print(possClassValues,className)


# In[32]:


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


# In[33]:


# IID3 improvisation: balance function to reduce multivariate splits
def balance(attrLen,imp = False):
    if not imp:
        return 1
    ans=cos(3.5*attrLen-1.5)/1.8
    ans*=log2(sqrt(attrLen+1))
    return abs(ans)


# In[35]:


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
            gain[attr] = (e-info[attr])/balance(len(attrVals),imp = True)
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
    for splitAttrVal, splitData in splitTrainData.items():
        n.children[splitAttrVal]=train(splitData,newAttrs)
    return n


# In[36]:




# In[37]:


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
            print("except")
    return x,ab


# In[42]:
size = len(cleanedData)
trainSize = 4*size//5
testSize = size-trainSize
print('trainSize={0},size={1}'.format(trainSize,size))
cleanedData = np.random.permutation(cleanedData)
n=train(cleanedData[:trainSize],list(possVals.keys()))

cor,incor=testing1(n,cleanedData[trainSize:])


# In[45]:

print(cor,incor,testSize,trainSize)
print('accuracy={0}\terror rate={1}\t'.format(cor/testSize*100,incor/testSize*100))
printTree(n)
