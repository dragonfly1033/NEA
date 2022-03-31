if __name__ == "__main__":
    from data_structures import BinaryTree, Stack
    from tokens import Not, Product, Sum, Var, Expression
else:
    from parsing.data_structures import BinaryTree, Stack
    from parsing.tokens import Not, Product, Sum, Var, Expression


def generate_ast(postfix):
    """make binary tree out of postfix"""

    ans_stack = Stack()
    for _ in range(postfix.length):
        val = postfix.pop()
        if 65 <= ord(val) <= 90 or val == "0" or val == "1":
            ans_stack.push(val)
        elif val == "¬":
            root = BinaryTree(val)
            v1 = ans_stack.pop()
            if isinstance(v1, str):
                root.add_child(v1)
            else:
                root.right = v1
            ans_stack.push(root)
        else:
            root = BinaryTree(val)
            v1 = ans_stack.pop()
            v2 = ans_stack.pop()
            if isinstance(v1, str):
                root.add_child(v1)
            else:
                root.right = v1
            if isinstance(v2, str):
                root.add_child(v2)
            else:
                root.left = v2
            ans_stack.push(root)

    return ans_stack.pop()


def nof_convert(node):
    """generate NOF from binary tree"""
    if node.val == "¬":
        return Not(nof_convert(node.right))
    elif node.val == "+":
        return Sum(nof_convert(node.left), nof_convert(node.right))
    elif node.val == "*":
        return Product(nof_convert(node.left), nof_convert(node.right))
    else:
        return Var(node.val)


def shunting_yard(expr):
    """convert infix to postfix"""
    op_stack = Stack()
    ans_stack = Stack()

    for char in expr:
        if 65 <= ord(char) <= 90 or char == "0" or char == "1":
            ans_stack.push(char)
        elif char == "(":
            op_stack.push(char)
        elif char == ")":
            while op_stack.top != "(":
                ans_stack.push(op_stack.pop())
            op_stack.pop()
        else:
            while op_stack and precedence[op_stack.top] >= precedence[char]:
                ans_stack.push(op_stack.pop())
            op_stack.push(char)

    while op_stack:
        ans_stack.push(op_stack.pop())
    return ans_stack


def parse(expr):
    """function to convert expression to NOF"""
    expr = expr.upper().replace(" ", "")
    are_not_valid = [i not in valid_chars for i in expr]
    if any(are_not_valid):
        print(are_not_valid)
        raise ValueError
    if len(expr) == 1:
        return Expression(Var(expr))

    postfix = shunting_yard(expr)
    postfix.reverse()
    ast = generate_ast(postfix)
    nof = Expression(nof_convert(ast))
    return nof


valid_chars = [chr(i) for i in range(65, 91)]
valid_chars += [chr(i) for i in range(97, 123)]
valid_chars += ["0", "1"]
valid_chars += ["+", "*", "¬", "(", ")"]
precedence = {"¬": 3, "*": 2, "+": 1, "(": -1}
