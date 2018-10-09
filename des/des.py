import argparse
import attributes
import dataset
parser = argparse.ArgumentParser(
	           description='to descritize data')
parser.add_argument('classifier',
                    help='Name of the attribute to use for classification')
parser.add_argument('-a','--attributes',
                    type=argparse.FileType('r'),
                    help='Name of the attribute specification file',
                    dest='attributes_file',
                    required=True)
parser.add_argument('-d','--data',
                    type=argparse.FileType('r'),
                    help='Name of the file to use for training/learning',
                    dest='training_file',
                    required=True)
args = parser.parse_args()
all_attributes = attributes.Attributes(args.attributes_file)
classifier = all_attributes[args.classifier]
training_data = dataset.DataSet(args.training_file, all_attributes)
all_attributes.discretize(classifier,training_data,args.attributes_file.name.split('-')[0])