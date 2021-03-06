"""
Description:

ID3 Construction:
Recursively split until:
- all examples are the same classification, or
- we have no more features to split on, or
- we have no more examples

Split according to the feature that does the best job dividing the examples by
classification (Entropy)
"""

import copy
import dataset
from node import Node
from attributes import Attribute


class DTree:
    """Represents a decision tree created with the ID3 algorithm"""

    def __init__(self, classifier, training_data, attributes):
        """
        Creates a new decision tree

        :param classifier: (Attribute) Attribute that is being used for classification
        :param training_data: (DataSet) Set of training data
        :param attributes: (Attributes) All attributes in this domain
        """
        self.classifier = classifier
        self.training_data = training_data
        self.attributes = attributes

        # initialize the beginning of the tree
        root = Node(data=self.training_data, parent=None, children=list(), attribute=None)
        self.id3(root=root, target_attribute=self.classifier, attrs=self.attributes, debug=False)
        self.decision_tree = root

    def test(self, classifier, testing_data):
        """
        Uses a decision tree to classify test examples

        :param classifier: (Attribute) Attribute that is being used for classification
        :param testing_data: (DataSet) Set of testing data
        :return: (int) Number of test examples that were correctly classified by the decision tree
        """
        count = 0

        def warning(test1, test2):
            if test1 == test2:
                return ":)", 1
            else:
                return "!!!", 0

        for example in testing_data.all_examples:
            val1, val2 = self.test_case(instance=example, node=self.decision_tree), example.get_value(classifier)
            sign, add = warning(val1, val2)
            count += add
            print('test: {}, actual: {}  -- {}'.format(val1, val2, sign))

        return count

    def dump(self):
        """
        Prints out a visual representation of the decision tree
        """
        return self.pre_order(classifier=self.classifier, node=self.decision_tree, indent=0)

    def pre_order(self, classifier, node, indent):
        """

        :param classifier:
        :param node:
        :param indent:
        :return:
        """
        text = ''
        if node.attribute.name in self.classifier.values:
            text += "{}<{}>\n".format(str(' '*indent), node.attribute.name)
            return text
        else:
            for child in node.children:
                part = ''
                part += "{}{}:{}\n".format(str(' ' * indent), node.attribute.name, child[0])
                text += "{}{}".format(part, self.pre_order(classifier=classifier, node=child[1], indent=indent+1))
        return text

    # HELPER FUNCTIONS
    def test_case(self, instance, node):
        """

        :param instance: (Example) the information to classify
        :param node: (Node) current node
        :return:
        """
        if 'end' in node.attribute.values:
            return node.attribute.name
        else:
            example_value = instance.get_value(node.attribute)

            for child in node.children:
                if example_value == child[0]:
                    return self.test_case(instance=instance, node=child[1])
        return 'unknown'

    # HELPER FUNCTIONS
    def like_parent_like_child(self, classifier, node):
        """

        :param classifier:
        :param node:
        :return:

        Attribute: return the attribute that this child should model based on their parent
        """
        while node is not None:

            parent_entropy = node.data_set.entropy(classifier=classifier)
            if parent_entropy[0] != 1:
                # there is an unequal amount of positive and negative value
                # choose the most dominant value for the attribute
                return Attribute(parent_entropy[1], 'end')
            else:
                # the data set is completely random
                # meaning that there are equal amounts of positive classifications and negative
                # classifications
                # move to the next parent
                return self.like_parent_like_child(classifier=classifier, node=node.parent)

        else:
            # finishes the loop correctly
            # at the parent node
            # SUSPICIOUS
            print('error: finished the loop and there is no parent with a dominant value')
            return Attribute(classifier.values.sort()[0], 'end')

    def id3(self, root, target_attribute, attrs, debug=False):
        """

        :param root:
        :param target_attribute:
        :param attrs:
        :param indent:
        :return:
        """
        # pass in root
        # do a general check based on entropy
        if root.data_set.entropy(classifier=target_attribute)[0] == 0:
            value = root.data_set.all_examples[0].get_value(target_attribute)
            root.attribute = Attribute(value, 'end')
            return

        # there are attributes to split upon
        # decide the split based on gain

        if len(attrs) > 0:
            # START: BEST ATTRIBUTE
            best_attributes = list()

            # find the best attribute
            for attr in attrs:
                # iterate through each value in the attribute
                gain = root.data_set.gain(target_attribute, attr, debug)

                if len(best_attributes) == 0:
                    best_attributes.append((attr, gain))
                elif best_attributes[0][1] == gain:
                    best_attributes.append((attr, gain))
                elif best_attributes[0][1] < gain:
                    best_attributes = [(attr, gain)]

            # organize alphabetically
            # "Also, if there is a tie in entropy reduction between multiple attributes, you should choose the
            # attribute
            # whose name is earlier in the alphabet (using Python's native string comparison)
            def name(elem):
                return elem[0].name

            # sort based on name
            best_attributes.sort(key=name)
            if debug is True:
                print()
                print('best attributes: ')
                for attr in best_attributes:
                    print(attr[0].name, " ", end=' ')
                print()

            # BUILD CHILDREN
            # create the attribute for this node
            root.attribute = best_attributes[0][0]

            root.attribute.values.sort()

            # END: BEST ATTRIBUTES
            if debug is True:
                print("best attribute: ", root.attribute.name)
                input('...')
            # ADD CHILDREN

            for value in root.attribute.values:
                example_set = [x for x in root.data_set.all_examples if x.get_value(root.attribute) == value]

                # examples to work with
                # make new node to pass down
                next_node = Node(data=dataset.DataSet(), parent=root, children=list(), attribute=None)

                attributes = copy.copy(attrs)
                attributes.remove(root.attribute)

                # CASE: RUN OUT OF EXAMPLES
                if len(example_set) == 0:
                    if debug is True:
                        print('warning: out of examples')
                    # choose the most prevalent example from the population that falls into the parent's domain
                    parent = root
                    next_node.attribute = self.like_parent_like_child(classifier=target_attribute, node=parent)

                    # no need to delve any more into next node
                    root.children.append((value, next_node))
                    continue

                # make a dataset with all the value-specific information and store in next node
                next_node.data_set.all_examples = example_set

                # update the children of the node by recursing through
                self.id3(root=next_node, target_attribute=target_attribute, attrs=attributes, debug=debug)

                root.children.append((value, next_node))

        else:
            # RUN OUT OF FEATURES
            # no attributes
            if debug is True:
                print('warning: out of features')

            num_pos = root.data_set.partial_count(target_attribute)
            num_neg = len(root.data_set) - num_pos
            tie = num_pos == num_neg

            if tie:
                # this is what we do in the event of a tie:
                parent = root
                root.attribute = self.like_parent_like_child(classifier=target_attribute, node=parent)
            else:
                # in the event of NOT a tie
                dominant_value = root.data_set.entropy(classifier=target_attribute)[1]
                root.attribute = Attribute(dominant_value, 'end')
