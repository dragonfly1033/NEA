
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

def fakePopulate():

    T = BinaryTree(1)

    T.root.left = Node(val=2)
    T.root.left.left = Node(val=4)
    T.root.left.left.left = Node(val=8)
    T.root.left.left.right = Node(val=9)
    T.root.left.right = Node(val=5)
    T.root.left.right.left = Node(val=10)
    T.root.left.right.right = Node(val=11)

    T.root.right = Node(val=3)
    T.root.right.left = Node(val=6)
    T.root.right.left.left = Node(val=12)
    T.root.right.left.right = Node(val=13)
    T.root.right.right = Node(val=7)
    T.root.right.right.left = Node(val=14)
    T.root.right.right.right = Node(val=15)

    return T