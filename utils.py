import heapq


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._insert_ctr = 0

    def push(self, item):
        heapq.heappush(self._queue, (self._insert_ctr, item))
        self._insert_ctr += 1

    def pop(self):
        return heapq.heappop(self._queue)[1]

    def peek(self):
        return self._queue[0][1]

    def size(self):
        return len(self._queue)

    def empty(self):
        return len(self._queue) == 0
