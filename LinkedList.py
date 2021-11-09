class Node:
    def __init__(self, elem):
        self.elem = elem
        self.next = None

class LinkedList:
    def __init__(self):
        self.begin = None
        self._size = 0

    def append(self, elem):
        if self.begin:
            pointer = self.begin
            while(pointer.next):
                pointer = pointer.next
            pointer.next = Node(elem)
        else:
            self.begin = Node(elem)
        self._size += 1

    def __len__(self):
        return self._size

    def _getnode(self, index):
        pointer = self.begin
        for i in range(index):
            if pointer:
                pointer = pointer.next
            else:
                raise IndexError('List index out of range')
        return pointer

    def __getitem__(self, index):
        pointer = self._getnode(index)
        if pointer:
            return pointer.elem
        else:
            raise IndexError('List index out of range')

    def __setitem__(self, index, elem):
        pointer = self._getnode(index)
        if pointer:
            pointer.elem = elem
        else:
            raise IndexError('List index out of range')

    def index(self, elem):
        pointer = self.begin
        i = 0
        while(pointer):
            if pointer.elem == elem:
                return i
            pointer = pointer.next
            i += 1
        raise ValueError(f'{elem} is not in list')

    def insert(self, index, elem):
        node = Node(elem)
        if index == 0:
            node.next = self.begin
            self.begin = node
        else:
            pointer = self._getnode(index - 1)
            node.next = pointer.next
            pointer.next = node
        self._size += 1

    def __delitem__(self, elem):
        return self.remove(elem)

    def remove(self, elem):
        if self.begin == None:
            raise ValueError(f'{elem} is not in list')
        elif self.begin.elem == elem:
            self.begin = self.begin.next
            self._size -= 1
            return True
        else:
            before = self.begin
            pointer = self.begin.next
            while(pointer):
                if pointer.elem == elem:
                    before.next = pointer.next
                    pointer.next = None
                    self._size -= 1
                    return True
                before = pointer
                pointer = pointer.next
        raise ValueError(f'{elem} is not in list')
    
    def extend(self, tup):
        for i in range(len(tup)):
            self.append(tup[i])

    def clear(self):
        for elem in self:
            self.remove(elem)
    
    def __iter__(self):
        pointer = self.begin
        while pointer:
            yield pointer.elem
            pointer = pointer.next

    def __repr__(self):
        r = ''
        pointer = self.begin
        while(pointer):
            r = r + str(pointer.elem) + ' '
            pointer = pointer.next
        return r

    def __str__(self):
        return self.__repr__()

if __name__ == '__main__':
    # sequencial = []
    # sequencial.append(7)
    lista = LinkedList()
    lista1 = LinkedList()
    lista1.append(40)
    lista1.append(60)
    lista.append([lista1])
    lista.append(80)
    lista.append(56)
    lista.append(32)
    lista.append(17)

    for l in lista:
        print(l)