from TdP_collections.priority_queue.heap_priority_queue import HeapPriorityQueue

class MaxOrientedPriorityQueue(HeapPriorityQueue):

    class _Item(HeapPriorityQueue._Item):

        def __init__(self, k, v):
            self._key = v
            self._value = k

        def __lt__(self, other):
            return self._key > other._key    # compare items based on their keys

    def __init__(self, contents=()): 
        """Create a new priority queue. By default, queue will be empty. 
        If contents is given, it should be as an iterable sequence of (k,v) 
        tuples specifying the initial contents. """
        self._data = [ self._Item(k,v) for k,v in contents.items() ] # empty by default 
        if len(self._data) > 1:
            self._heapify()

    def _heapify(self):
        start = self._parent(len(self) - 1) 
        for j in range(start,-1,-1):
            self._downheap(j)

    def remove_max(self):
        return self.remove_min()

    def max(self):
        return self.min()