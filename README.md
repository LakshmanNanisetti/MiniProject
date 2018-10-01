# Mini Project - Data Mining

CSE sem 7 2018-2019

## Overview

An improved ID3 algorithm for clinical data classification based on
[Yang, Shuo, Jing-Zhi Guo, and Jun-Wei Jin. "An improved Id3 algorithm for medical data classification." Computers & Electrical 
Engineering 65 (2018): 474-487.](https://www.sciencedirect.com/science/article/pii/S004579061732517X "reference paper")

## Datasets Cleaning and Representation

the data sets are publicly available at:
[UCI archive](https://archive.ics.uci.edu/ml/)

### Data Cleaning
clean the data set by removing examples that have missing values

### Representation
create exactly three files: 

1. attributes file

        name-attributes.txt

2. training dataset file
        
        name-train.csv


3. testing dataset file
        
        name-test.csv

_name_ is name of the data set.

#### Attributes File
This file contains the list of all the attributes and their possible values (this will include the classifier and its values).
Each line in the attributes file should be in the format "attribute: _type of attribute_,  value0, value1, ... valueN". 
For example see the breast cancer attributes:

    Clump Thickness:1,1,2,3,4,5,6,7,8,9,10
    Cell Size:1,1,2,3,4,5,6,7,8,9,10
    Cell Shape:1,1,2,3,4,5,6,7,8,9,10
    Marginal Adhesion:1,1,2,3,4,5,6,7,8,9,10
    Single Epithelial
    Cell Size:1,1,2,3,4,5,6,7,8,9,10
    Bare Nuclei:1,1,2,3,4,5,6,7,8,9,10
    Bland Chromatin:1,1,2,3,4,5,6,7,8,9,10
    Normal Nucleoli:1,1,2,3,4,5,6,7,8,9,10
    Mitoses:1,1,2,3,4,5,6,7,8,9,10
    Class:0,2,4

first value _type of attribute_ if  _0_ then the attribute is nominal else if it is _1_ then it is numeric.

in above example the first zero in Class tells it is a nominal attribute
 
#### Dataset Files
Each of the dataset files should have a list of examples, with one example per line. Each example is simply a comma-separated
list of values, one for each attribute in the order provided in the attributes file. There may also be a "name:" at the 
beginning of a line to use as a label for the data. These labels are optional and simply for readability: they are thrown 
away by the parser. Three lines from a dataset of breast cancer may look like this:

    patient_1:5,1,1,1,2,1,3,1,1,2
    patient_2:5,4,4,5,7,10,3,2,1,2
    patient_3:3,1,1,1,2,2,3,1,1,2

Next, partition all the examples in two dataset files, one to use for training the decision tree algorithm (training set)
and one for testing the effectiveness of trained tree (testing set).

### Data Sets used for this Project

All the data sets are publicly available at:
[UCI archive](https://archive.ics.uci.edu/ml/)

1.  Acute inflammations

2.  breast cancer (Wisconsin)

3.  lung cancer

4.  mammographic mass

5.  statlog (Heart)


## Decision Tree Creation and Testing

Improved Id3 algorithm is implemented to create a decision tree. It will accept a set of data in the format described in Data 
cleaning, and from that data produce a decision tree. It will also allow testing the accuracy of the decision tree by running test 
cases against the tree and comparing the decision tree's performance against the known classifications.

In some cases, It will run out of attributes before uniformly classifying the examples.The following are guidelines followed in 
such cases

*1.If it run out of attributes and there are examples with different classifications, it chooses the classification for which 
there are the most examples. If there are a duplicate number of examples in more than one group, choose the greatest number of 
examples from the parent, recursing as needed. If all sets are equal up to the root, the population is probably too small, so 
choose the value that comes earliest in the alphabet.*

*2. If it has a subpopulation that has no examples for an attribute value, it chooses the most prevalent example from the
population that falls into the parent's domain, as per guideline 1.*

### Usage 
*main.py:* Provides a command-line interface to the decision tree. It takes parameter for the decision tree
algorithm module, and name of the classification attribute. Invoke --help to see complete list of options.


    usage: main.py [-h] [-d] -a ATTRIBUTES_FILE -l TRAINING_FILE [-t TESTING_FILE]
                   dtree-module classifier
    Train (and optionally test) a decision tree
    positional arguments:
      dtree-module          Decision tree module name
      classifier            Name of the attribute to use for classification
    optional arguments:
      -h, --help            show this help message and exit
      -d, --debug           enables debug
      -a ATTRIBUTES_FILE, --attributes ATTRIBUTES_FILE
                            Name of the attribute specification file
      -l TRAINING_FILE, --train TRAINING_FILE
                            Name of the file to use for training/learning
      -t TESTING_FILE, --test TESTING_FILE
                            Name of the file to use for testing 

 
### Example

    python main.py id3 Class -d -a tests/bcw-attributes.txt -l tests/bcw-train.csv -t tests/bcw-test.csv

### Decision tree representation
The format of the dump output for a __non-terminal__ node in the decision tree is:

    attribute-name:attribute-value-1
    
    attribute-name:attribute-value-2
    
    ...
    
    attribute-name:attribute-value-n

A __terminal__ node is represented as:

    <classification>


Each line is indented one space for each level it is below the first.

For example, consider the following decision tree for classifying brest cancer:

    Cell Size
        |
        ->1.0
           |
           -Bare Nuclei
                |
                ->[1.0-4.0]
                |    |
                |    -><2>
                ->5.0
                |   |
                |   -Clump Thickness
                |   |
                |   ->[1.0-4.0]
                |        |   
                |        -><2>
                |
                .
                .
                .
                .
                ->[6.0-9.0]
                    |
                    -Bland Chromatin
                    |       |
                    |       ->[1.0-2.0]
                    |           |
                    |           -><4>
                    .
                    .

It would be represented as:

    Cell Size:1.0
     Bare Nuclei:[1.0-4.0]
      <2>
     Bare Nuclei:5.0
      Clump Thickness:[1.0-4.0]
       <2>
       .
       .
       .
     Bare Nuclei:[6.0-9.0]
      Bland Chromatin:[1.0-2.0]
       <4>
       .
       .
       .


___________________________________________________________________________________________________________________________________
