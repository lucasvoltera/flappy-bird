ROOT = 'root'

class Node:
    def __init__(self, elem):
        self.elem = elem
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.elem)

class BinaryTree:
    def __init__(self, elem=None, node=None):
        if node:
            self.root = node
        elif elem:
            node = Node(elem)
            self.root = node
        else:
            self.root = None

    def inOrder(self, node=None):
        if node is None:
            node = self.root
        if node.left:
            print('(', end='') 
            self.inOrder(node.left)
        print(node, end='')
        if node.right:
            self.inOrder(node.right)
            print(')', end='')
    
    def postOrder(self, node=None):
        if node is None:
            node = self.root
        if node.left:
            self.postOrder(node.left)
        if node.right:
            self.postOrder(node.right)
        print(node)
    
    def height(self, node=None):
        if node is None:
            node = self.root
        height_left = 0
        height_right = 0
        if node.left:
            height_left = self.height(node.left)
        if node.right:
            height_right = self.height(node.right)
        if height_right > height_left:
            return height_right + 1
        return height_left + 1

class BinarySearchTree(BinaryTree):
    def insert(self, value):
        parent = None
        x = self.root
        while x:
            parent = x
            if value < x.elem:
                x = x.left
            else:
                x = x.right
        if parent is None:
            self.root = Node(value)
        elif value < parent.elem:
            parent.left = Node(value)
        else:
            parent.right = Node(value)

    def search(self, value):
        return self._search(value, self.root)

    def _search(self, value, node):
        if node is None:
            return node
        if node.elem == value:
            return BinarySearchTree(node)
        if value < node.elem:
            return self._search(value, node.left)
        return self._search(value, node.right)

    def min(self, node=ROOT):
        if node == ROOT:
            node = self.root
        while node.left:
            node = node.left
        return node.elem

    def max(self, node=ROOT):
        if node == ROOT:
            node = self.root
        while node.right:
            node = node.right
        return node.elem

    def remove(self, value, node=ROOT):
        if node == ROOT:
            node = self.root
        if node is None:
            return node
        if value < node.elem:
            node.left = self.remove(value, node.left)
        elif value > node.elem:
            node.right = self.remove(value, node.right)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                substitute = self.min(node.right)
                node.elem = substitute
                node.right = self.remove(substitute, node.right)
        return node

if __name__ == "__main__":
    tree = BinaryTree(7)
    tree.root.left = Node(18)
    tree.root.right = Node(14)

    print(tree.root)
    print(tree.root.right)
    print(tree.root.left)