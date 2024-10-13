from dataclasses import dataclass
from functools import reduce
from typing import Any, Self, Callable


@dataclass
class Node:
    value: Any = None
    left: Self | None = None
    right: Self | None = None


class BST:
    IN_ORDER = "in"
    PRE_ORDER = "pre"
    POST_ORDER = "post"

    """A class representation of a Binary Search Tree"""

    def __init__(self, compare: Callable[[Any, Any], int] = None):
        """
       :param compare: function that returns the value of arg1 - arg2
       """
        self.root = None
        self.compare = compare
        self.length = 0

    pass

    def is_empty(self):
        """
        Checks whether a tree is empty.
        :return: True or False
        """
        return self.root is None

    def insert(self, value):
        """
        inserts a given element into the tree.
        :param value: The element to be inserted.
        :return: None
        """
        new_node = Node(value)
        if self.is_empty():
            self.root = new_node
            self.length += 1
            return

        current = self.root

        while True:
            comp = self.compare(value, current.value)
            if comp < 0:
                if current.left is None:
                    current.left = new_node
                    self.length += 1
                    return
                else:
                    current = current.left

            else:
                if current.right is None:
                    current.right = new_node
                    self.length += 1
                    return
                else:
                    current = current.right




    def for_each(self, traversal_type, action_func):
        if traversal_type == self.IN_ORDER:
            self._in_order_traversal(self.root, action_func)
        elif traversal_type == self.PRE_ORDER:
            self._pre_order_traversal(self.root,action_func)
        elif traversal_type == self.POST_ORDER:
            self._post_order_traversal(self.root,action_func)
        else:
            return None



    def _in_order_traversal(self, node, action_func):
        if node:
            self._in_order_traversal(node.left, action_func)
            action_func(node.value) #action func takes values, not nodes, so user cant change bst properties
            self._in_order_traversal(node.right, action_func)


    def _pre_order_traversal(self, node, action_func):
        if node:
            action_func(node.value)
            self._pre_order_traversal(node.left, action_func)
            self._pre_order_traversal(node.right, action_func)

    def _post_order_traversal(self, node, action_func):
        if node:
            self._post_order_traversal(node.left, action_func)
            self._post_order_traversal(node.right, action_func)
            action_func(node.value)


    def _find(self,value):
        parent = None
        current = self.root

        while current is not None:
            cmp = self.compare(value, current.value)
            if cmp == 0:
                return current, parent
            elif cmp < 0:
                parent = current
                current = current.left
            else:
                parent = current
                current = current.right

            if current is None:
                return current,parent

        return None,None




    def remove(self, value):
        """
        Removes a given element from the tree.
        :param value: The element to be removed.
        :return: True if the element was removed, False if it wasn't found.
        """

        current,parent = self._find(value)

        if current is None:
            return False

        else:
            self.length -= 1
            if current.left is None or current.right is None: # node to remove has 0 or 1 children
                child = current.left if current.left is not None else current.right
                if parent is None: # node to remove is the root and have 0 or 1 children
                    self.root = child
                elif parent.left == current:# node to remove is a left child of his parent
                    parent.left = child
                else: #node to remove is a right child of his parent
                    parent.right = child
            else: # node to remove have 2 valid children, we find his succ and his succ parent
                succ_parent = current
                succ = current.right
                while succ.left is not None:
                    succ_parent = succ
                    succ = succ.left
                current.value = succ.value
                if succ_parent.left == succ:  # if the succ is a left child of his parent (1 or more iter in the while)
                    succ_parent.left = succ.right  # succ right sub tree is a left son of succ_parent
                else:  # if the succ is a right child of his parent (0 while iters, succ of current is his right child)
                    succ_parent.right = succ.right  # succ right sub tree is a left son of succ-parent

        return True




    def __contains__(self, value):
        """

        :param value: The value to be searched.
        :return: True if the element is in the tree, False otherwise.
        """
        current, _ = self._find(value)
        if current:
            return True

        return False




    def __str__(self):
        """
        Returns a string representation of the tree in in-order traversal.
        :return: A string representation of the tree.
        """
        data_of_nodes = []
        self.for_each(self.IN_ORDER, lambda value: data_of_nodes.append(value))
        return reduce(lambda ret_string, value: ret_string + str(value) + " "  ,  data_of_nodes, "")


    def __len__(self):
        """
        :return: The number of elements of in the tree.
        """
        return self.length


def compare_func(x: Any, y: Any) -> int:
    if x < y:
        return -1
    elif x > y:
        return 1
    else:
        return 0





