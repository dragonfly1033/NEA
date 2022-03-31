"""module with data structure classes"""


class Stack:
    """Stack class"""

    def __init__(self):
        self.vals = []

    def __bool__(self):
        return len(self.vals) > 0

    def push(self, val):
        """adds val to stack"""
        self.vals.append(val)

    def pop(self):
        """removes top value from stack and returns it"""
        return self.vals.pop()

    def reverse(self):
        """reverse stack"""
        self.vals = self.vals[::-1]

    @property
    def top(self):
        """return top value from stack"""
        return self.vals[-1]

    @property
    def length(self):
        """return length of stack"""
        return len(self.vals)


class Queue:
    """Queue class"""

    def __init__(self):
        self.vals = []

    def __bool__(self):
        return len(self.vals) > 0

    def enqueue(self, val):
        """add val to queue"""
        self.vals.append(val)

    def dequeue(self):
        """remove item from front of queue and return it"""
        return self.vals.pop(0)

    def reverse(self):
        """reverse queue"""
        self.vals = self.vals[::-1]

    @property
    def front(self):
        """return front of queue"""
        return self.vals[0]

    @property
    def rear(self):
        """return rear of queue"""
        return self.vals[-1]

    @property
    def length(self):
        """return length of queue"""
        return len(self.vals)


class Node:
    """Class for node of binary tree"""

    def __init__(self, parent=None, val=None):
        self.parent = parent
        self.val = val
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.val)

    def add_val(self, val):
        """set the value of the node"""
        self.val = val

    def add_child(self, val):
        """add child to node"""
        if self.right is not None:
            if self.left is not None:
                return False
            else:
                self.left = Node(self, val=val)
                return self.left
        else:
            self.right = Node(self, val=val)
            return self.right

    def traverse(self, order="in"):
        """function to traverse binary tree"""

        this = self.val

        if self.left is not None:
            left = self.left.traverse()
        else:
            left = ""

        if self.right is not None:
            right = self.right.traverse()
        else:
            right = ""

        if order == "pre":
            return f"({this}{left}{right})"
        elif order == "in":
            return f"({left}{this}{right})"
        elif order == "post":
            return f"({left}{right}{this})"


class BinaryTree(Node):
    """Binary Tree class"""

    def __init__(self, val=None):
        super().__init__(None, val)
