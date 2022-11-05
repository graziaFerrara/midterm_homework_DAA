from TdP_collections.hash_table.chain_hash_map import ChainHashMap
from TdP_collections.hash_table.probe_hash_map import ProbeHashMap
from TdP_collections.map.red_black_tree import RedBlackTreeMap

class Trie:

    __slots__ = '_root' # streamline memory usage

    #-------------------------- nested _Node class --------------------------
    
    class _Node:

        __slots__ = '_children', '_endNode' ,'_occurrenceList' # streamline memory usage

        def __init__(self, endNode = False):
            self._children = {}
            self._endNode = endNode
            if self._endNode: self._occurrenceList = ProbeHashMap()

    #------------------------------------------------------------------------

    def __init__(self):
        self._root = self._Node()

    def _searchNode(self, word):
        node = self._root
        i = 0
        length = len(word)
        while i < length:
            try:
                # letter found, let's search the next one
                node = node._children[word[i]]
            except KeyError:
                # letter not found
                return node, i
            i += 1
        return node, i

    def searchWord(self, word):
        word += '$'
        node = self._searchNode(word)[0]
        return node._occurrenceList if node._endNode else None

    def insertWord(self, word):
        word += '$'
        node, index = self._searchNode(word)
        length = len(word)
        if index < length  :
            i = index
            while i < length - 1:
                node._children[word[i]] = self._Node()
                node = node._children[word[i]]
                i += 1
            # the last node has to be a terminator
            node._children[word[i]] = self._Node(True)
