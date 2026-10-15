class Node:
    def __init__(self, horse):
        self.horse = horse
        self.next = self
        self.previous = self


class CircularDoublyLinkedList:
    """A circular doubly linked list that stores Horse objects."""

    def __init__(self):
        self.head = None
        self.current = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def add(self, horse):
        new_node = Node(horse)

        if self.head is None:
            self.head = new_node
            self.current = new_node
        else:
            tail = self.head.previous
            new_node.next = self.head
            new_node.previous = tail
            tail.next = new_node
            self.head.previous = new_node

        self.size += 1
        return new_node

    def find_node(self, query):
        if self.head is None:
            return None

        query = str(query).strip().lower()
        node = self.head
        for _ in range(self.size):
            if node.horse.horse_id.lower() == query or node.horse.name.lower() == query:
                return node
            node = node.next
        return None

    def remove(self, query):
        node = self.find_node(query)
        if node is None:
            return False

        if self.size == 1:
            self.head = None
            self.current = None
        else:
            node.previous.next = node.next
            node.next.previous = node.previous

            if node is self.head:
                self.head = node.next
            if node is self.current:
                self.current = node.next

        self.size -= 1
        return True

    def next_horse(self):
        if self.current is not None:
            self.current = self.current.next
        return self.current.horse if self.current else None

    def previous_horse(self):
        if self.current is not None:
            self.current = self.current.previous
        return self.current.horse if self.current else None

    def set_current(self, query):
        node = self.find_node(query)
        if node is not None:
            self.current = node
            return node.horse
        return None

    def update_horse(self, query, name, breed, age, health_status, activity):
        node = self.find_node(query)
        if node is None:
            return False
        node.horse.update(name, breed, age, health_status, activity)
        return True

    def get_all(self):
        horses = []
        if self.head is None:
            return horses

        node = self.head
        for _ in range(self.size):
            horses.append(node.horse)
            node = node.next
        return horses
