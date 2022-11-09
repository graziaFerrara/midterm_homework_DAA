from TdP_collections.hash_table.probe_hash_map import ProbeHashMap
from TdP_collections.hash_table.chain_hash_map import ChainHashMap

class CompressedTrie3:
    """
    A class to model a Compressed Trie. 

    Attributes
    ----------
    _root : _Node
        Root of the Compressed Trie.

    Methods
    -------
    _searchNode
        A utility method for the search and insert methods, to retrieve the last node of the 
        word containing the occurrence list if it is present, or the node in which the 
        insertion has to be done otherwise.
    searchWord
        A public method to search a given word into the Compressed Trie.
    insertWord
        A public method to insert a given word into the Compressed Trie if it is not present.
    """

    __slots__ = '_root' # streamline memory usage

    #-------------------------- nested _Node class --------------------------
    
    class _Node:
        """
        A class to model a node of the Compressed Trie.

        Attributes
        ----------
        _edges : dictionary
            Collection of all the edges starting from a node, where the key is the 
            initial letter of the content of the edge's lable.
        _endNode : bool
            Indecates if the node is an end node or not.
        _occurrenceList : dictionary 
            Collection of all the pages and their occurrences of the given word.
        """

        __slots__ = '_edges', '_endNode' ,'_occurrenceList' # streamline memory usage

        def __init__(self, endNode = False):
            """Initialize the Node."""
            self._edges = {}
            self._endNode = endNode
            if self._endNode: self._occurrenceList = {}

    #-------------------------- nested _Edge class --------------------------

    class _Edge:
        """
        A class to model an edge of the Compressed Trie.

        Attributes
        ----------
        _targetNode : _Node
            The node which the edge connect to its parent.
        _lable : str
            A substring of a word.
        """
        
        __slots__ = '_targetNode', '_lable'

        def __init__ (self, targetNode, lable):
            """Initialize the Edge."""
            self._targetNode = targetNode
            self._lable = lable

    #-------------------------------------------------------------------------

    def __init__(self):
        """Initialize the Compressed Trie, creating an empty trie with just the root."""
        self._root = self._Node()

    def _searchNode(self, word):
        """
        A utility method for the search and insert methods, to retrieve the last node of the 
        word containing the occurrence list if it is present, or the node in which the 
        insertion has to be done otherwise.

        Parameters
        ----------
        word : str
            The word to be searched into the trie.

        Returns
        -------
        _Node
            The last node composing the word or the last node linked to an edge having the lable 
            belonging to the word.
        int
            Index of the last character of the original word present into the trie.

        TIME COMPLEXITY
        ---------------
        O(len(word)) expected and amortized
            In the worst case this method iterates all over the characters of the given word once and
            since the accesses to the dictionary are O(1) expected and amortized, we can conclude the 
            time complexity is the one reported above.

        """
        node = self._root
        i = 0
        length = len(word)
        while i < length:
            try:
                edge = node._edges[word[i]]
            except KeyError:
                # not existing key
                return node, i
            # existing key
            lable = edge._lable
            lableLen = len(lable)
            if edge._lable != word[i:i+lableLen]:
                # the lable differs from the word
                return node, i
            node = edge._targetNode
            i += lableLen
        return node, i 

    def searchWord(self, word):
        """
        A public method to search a given word into the Compressed Trie.

        Parameters
        ----------
        word : str
            The word to be searched into the trie.

        Returns
        -------
        dictionary | None
            Returns the _occurrenceList if it is present in the node, None otherwise.

        TIME COMPLEXITY
        ---------------
        O(len(word)) expected and amortized
            It is the same of the _searchNode method which is called inside.
        """
        word += '$'
        node = self._searchNode(word)[0]
        return node._occurrenceList if node._endNode else None

    def insertWord(self, word):
        """
        A public method to insert a given word into the Compressed Trie if it is not present.

        Parameters
        ----------
        word : str
            The word to be searched into the trie.

        TIME COMPLEXITY
        ---------------
        O(len(word)) expected and amortized
            It is the same of the _searchNode method which is called inside.

        """
        word += '$'
        node, index = self._searchNode(word)
        if index < len(word) :
            try:
                edge = node._edges[word[index]]
            except KeyError:
                # not existing key
                node._edges[word[index]] = self._Edge(self._Node(True),word[index:])
                return
            # already existing key, it is necessary to restructure!
            lable = edge._lable
            i = 0
            for c in word[index:]:
                if c != lable[i]: break
                i += 1
            newEdge = self._Edge(self._Node(),lable[:i]) # create the new edge leading to a new Node
            node._edges[word[index]] = newEdge # connect the node to the new edge
            newEdge._targetNode._edges[lable[i]] = edge # connect the old edge to the new node
            edge._lable = lable[i:] # change the lable of the old edge
            if not edge._targetNode._endNode: # make the old node a terminator
                edge._targetNode._endNode = True 
                edge._targetNode._occurrenceList = {}
            anotherEdge = self._Edge(self._Node(True), word[index+i:]) # create a new edge with the remaining part of the word
            newEdge._targetNode._edges[word[index+i]] = anotherEdge # connect the new edge to the new node
