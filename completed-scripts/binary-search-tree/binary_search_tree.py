class TreeNode:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def __str__(self):
        return f'TreeNode(data={self.data}, left={self.left}, right={self.right})'


class BinarySearchTree:
    def __init__(self, tree_data):
        self.root = TreeNode(tree_data[0])
        for value in tree_data[1:]:
            self._insert(self.root, value)

    def _insert(self, node, value):
        if value <= node.data:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)      
            else:
                self._insert(node.right, value)

    def data(self):
        return self.root
               

    def sorted_data(self):
        sorted_list =[]
        self._inorder(self.root, sorted_list)
        return sorted_list
        
    def _inorder(self, node, order):
        if node is None:
            return
        self._inorder(node.left, order)
        order.append(node.data)
        self._inorder(node.right, order)
        