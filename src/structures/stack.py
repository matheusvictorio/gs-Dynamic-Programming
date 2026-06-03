class Stack:
    """Pilha (LIFO) usada para histórico de navegação de meteoritos."""

    def __init__(self, max_size=50):
        self._items = []
        self._max_size = max_size

    def push(self, item):
        if len(self._items) >= self._max_size:
            self._items.pop(0)
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pilha vazia")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Pilha vazia")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def to_list(self):
        return list(reversed(self._items))
