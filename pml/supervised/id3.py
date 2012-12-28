# Copyright (C) 2012 David Rusk
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to 
# deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
# IN THE SOFTWARE.
"""
Implements the ID3 decision tree algorithm.

@author: drusk
"""

from pml.supervised.trees import Node, Tree
from pml.tools.info_theory import info_gain
from pml.utils.collection_utils import (get_key_with_highest_value, 
                                        get_most_common)

def build_tree(dataset):
    """
    Builds the decision tree for a data set using the ID3 algorithm.
    
    Args:
      dataset: model.DataSet
        The data for which the decision tree will be built.
    
    Return:
      tree: dictionary
        The decision tget_most_common(dataset.get_labels())ree stored as a dictionary of dictionaries.
        
        For example, a daree stored as a dictionary of dictionaries.
        
        For example, a data set with dogs, cats and birds and features 
        "num_legs" and "barks" might have a tree like follows:
        
        {
          "num_legs": {ta set with dogs, cats and birds and features 
        "num_legs" and "barks" might have a tree like follows:
        
        {
          "num_legs": {
            4: {
              "barks": {
                True: "dog",
                False: "cat"
              }
            2: "bird"
        }
    """
    return Tree(_build_tree_recursively(dataset))

def _build_tree_recursively(dataset):
    """
    """
    label_set = set(dataset.get_labels())
    if len(label_set) == 1:
        # All remaining samples have the same label, no need to split further
#        return label_set.pop()
        return Node(label_set.pop())
    
    if len(dataset.feature_list()) == 0:
        # No more features to split on
#        return get_most_common(dataset.get_labels())
        return Node(get_most_common(dataset.get_labels()))

    # We can still split further
    split_feature = choose_feature_to_split(dataset)
    
#    tree = {split_feature: {}}
    node = Node(split_feature)
    
    for value in dataset.get_feature_values(split_feature):
        subset = dataset.value_filter(
                            split_feature, value).drop_column(split_feature)
        node.add_child(value, _build_tree_recursively(subset))
#        tree[split_feature][value] = build_tree(subset)
    
    return node

def choose_feature_to_split(dataset):
    """
    Choose the root to be the feature which has the highest information 
    gain.
    
    Args:
      dataset: model.DataSet
        The data set being used to build the decision tree.
        
    Returns:
      feature: string
        The feature which should be the root.
    """
    gains = {}
    for feature in dataset.feature_list():
        gains[feature] = info_gain(feature, dataset)
    
    return get_key_with_highest_value(gains)
