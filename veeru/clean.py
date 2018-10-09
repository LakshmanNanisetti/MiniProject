import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', help='file name')
args = parser.parse_args()
fileName = args.file
fr = open(fileName,'r')
fw = open(fileName[:-5]+'cc.data','w')
for line in fr:
    if '?'  in line:
        pass
    else:
        fw.write(line)