from collections import deque


class Queue:
    """Fila (FIFO) usada para enfileirar meteoritos na análise em lote."""

    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Fila vazia")
        return self._items.popleft()

    def peek(self):
        if self.is_empty():
            raise IndexError("Fila vazia")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def to_list(self):
        return list(self._items)
