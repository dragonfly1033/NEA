
class BinaryTree:
    def __init__(self, rootVal=None):
        self.root = Node(val=rootVal)

    def traverse(self, order='in'):
        return self.root.traverse(order)

    def find_and_replace(self, val, new):
        self.root.find_and_replace(val, new) 

class Node:
    def __init__(self, parent=None, val=None):
        self.parent = parent
        self.val = val
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.val)

    def find_and_replace(self, val, newNode):
        if self.left == None:
            return
        if self.left.val == val:
            self.left = newNode
            return
        self.left.find_and_replace(val, newNode)
        if self.right == None:
            return
        if self.right.val == val:
            self.right = newNode
            return
        self.right.find_and_replace(val, newNode)

    def addVal(self, val):
        self.val = val
    
    def addChild(self, val):
        if self.left is not None:
            if self.right is not None:
                pass
            else:
                self.right = Node(val=val)
        else:
            self.left = Node(val=val)

    def traverse(self, order='in'):

        if self.left is None:
            return f'{self.val}'

        this = self.val
        left = str(self.left.traverse(order=order))
        right = str(self.right.traverse(order=order))

        if order == 'pre':
            return f'({this},{left},{right})'
        elif order == 'in':
            return f'({left}{this}{right})'
        elif order == 'post':
            return f'({left},{right},{this})'
