"""
File:           node.py

Description:
A node object that will be used to develop the decision tree

"""


class Node:
    """Represents the nodes that make up the decision tree"""

    def __init__(self, data, parent, children, attribute=None):
        """
        Creates a new node

        :param: data: (DataSet) the set of data associated with this node
        :param: classifier: (str) describe from which attribute are we classifying the information
        :param: parent: (Node) the reference to the node that self is attached to
        :param: children: ([Node, ...]) list of children nodes attached to self
        """
        """
        self.__attribute (Attribute) : the quality of the object that the dataset organized by and the pop. we wish to
                                        classify by
                                        
        self.__data_set (DataSet): the group of Examples that make up the entire population that are organized by the 
                                    given attribute
                                    
        self.__parent (Node): a reference to the parent of SELF
        
        self.__children ( list( (value, child_ref)) ): A list of tuples of size two, the first value of the tuple is
                                                        the value used to split upon, the second value of the tuple is
                                                        the reference to the child node
                                                        
                                                        EXAMPLE:
                                                        [ (value1, child1), (value2, child2), ... (valueN, <YES>) ]
        """

        self.attribute = attribute
        self.data_set = data
        self.parent = parent
        self.children = children
