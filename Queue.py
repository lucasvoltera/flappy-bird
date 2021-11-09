class Node:
    def __init__(self, elem):
        self.elem = elem
        self.next = None

class Queue:
    def __init__(self):
        self.begin = None
        self.end = None
        self._size = 0

    def push(self, elem):
        node = Node(elem)
        if self.end is None:
            self.end = node
        else:
            self.end.next = node
            self.end = node
        if self.begin is None:
            self.begin = node
        self._size += 1

    def pop(self):
        if self._size > 0:
            elem = self.begin.elem
            self.begin = self.begin.next
            if self.begin is None:
                self.end = None
            self._size -= 1
            return elem
        raise IndexError('The queue is empty')

    def peek(self):
        if self._size > 0:
            elem = self.begin.elem
            return elem
        raise IndexError('The queue is empty')
    
    def extend(self, tup):
        for i in range(len(tup)):
            self.push(tup[i])
        
    def _getnode(self, index):
        pointer = self.begin
        for i in range(index):
            if pointer:
                pointer = pointer.next
            else:
                raise IndexError('Queue index out of range')
        return pointer

    def __len__(self):
        return self._size

    def __repr__(self):
        if self._size > 0:
            r = ''
            pointer = self.begin
            while(pointer):
                r = r + str(pointer.elem) + ' '
                pointer = pointer.next
            return r
        return 'Empty Queue'

    def __iter__(self):
        pointer = self.begin
        while pointer:
            yield pointer.elem
            pointer = pointer.next

    def __str__(self):
        return self.__repr__()
    
    def __getitem__(self, index):
        pointer = self._getnode(index)
        if pointer:
            return pointer.elem
        else:
            raise IndexError('Queue index out of range')