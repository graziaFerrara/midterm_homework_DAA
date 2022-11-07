from TdP_collections.hash_table.probe_hash_map import ProbeHashMap
from TdP_collections.hash_table.chain_hash_map import ChainHashMap

class CompressedTrie3:

    __slots__ = '_root' # streamline memory usage

    #-------------------------- nested _Node class --------------------------
    
    class _Node:

        __slots__ = '_edges', '_endNode' ,'_occurrenceList' # streamline memory usage

        def __init__(self, endNode = False):
            self._edges = {}
            self._endNode = endNode
            if self._endNode: self._occurrenceList = ProbeHashMap()

    #-------------------------- nested _Edge class --------------------------

    class _Edge:
        
        __slots__ = '_targetNode', '_lable'

        def __init__ (self, targetNode, lable):
            self._targetNode = targetNode
            self._lable = lable

    #-------------------------------------------------------------------------

    def __init__(self):
        """Initialize the Compressed Trie, creating an empty trie with just the root."""
        self._root = self._Node()

    def _searchNode(self, word):
        node = self._root
        i = 0
        length = len(word)
        while i < length:
            try:
                edge = node._edges[word[i]]
            except KeyError:
                return node, i
            lable = edge._lable
            lableLen = len(lable)
            if edge._lable != word[i:i+lableLen]:
                return node, i
            node = edge._targetNode
            i += lableLen
        return node, i 

    def searchWord(self, word):
        word += '$'
        node = self._searchNode(word)[0]
        return node._occurrenceList if node._endNode else None

    def insertWord(self, word):
        word += '$'
        node, index = self._searchNode(word)
        if index < len(word) :
            try:
                edge = node._edges[word[index]]
            except KeyError:
                node._edges[word[index]] = self._Edge(self._Node(True),word[index:])
                return
            lable = edge._lable
            i = 0
            for c in word[index:]:
                if c != lable[i]: break
                i += 1
            newEdge = self._Edge(self._Node(),lable[:i]) # create the new edge leading to a new Node
            node._edges[word[index]] = newEdge # connect the node to the new edge
            newEdge._targetNode._edges[lable[i]] = edge # connect the old edge to the new node
            edge._lable = lable[i:] # change the lable of the old edge
            if not edge._targetNode._endNode: # make the old node terminator
                edge._targetNode._endNode = True
                edge._targetNode._occurrenceList = {}
            anotherEdge = self._Edge(self._Node(True), word[index+i:]) # create a new edge with the remaining part of the word
            newEdge._targetNode._edges[word[index+i]] = anotherEdge # connect the new edge to the new node
