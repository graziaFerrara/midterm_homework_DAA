from TdP_collections.hash_table.probe_hash_map import ProbeHashMap

class Trie:
    """
    A class to model a Standard Trie.
    
    Attributes
    ----------
    _root : _Node
        Root node of the Standard Trie.
    """

    __slots__ = '_root' # streamline memory usage

    #-------------------------- nested _Node class --------------------------
    
    class _Node:
        """
        A class to model the node of a Standard Trie.
        
        Attributes
        ----------
        _children : dict
            Collection containing the children of a _Node.
        _endNode : bool
            It is True if the _Node is an end node, False otherwise.
        _occurrenceList : dict
            Collection containing the pages in which the word occurs.
        """

        __slots__ = '_children', '_endNode' ,'_occurrenceList' # streamline memory usage

        def __init__(self, endNode = False):
            self._children = {}
            self._endNode = endNode
            if self._endNode: self._occurrenceList = ProbeHashMap()

    #------------------------------------------------------------------------

    def __init__(self):
        """Initialize the Standard Trie, creating an empty trie with just the root."""
        self._root = self._Node()

    def _searchNode(self, word):
        """
        Method to search the end node of the word if exists, or the last present node.

        Parameters
        ----------
        word : str
            the word to be searched in the Trie

        Returns
        -------
        _Node
            the node containing the last character of the word present in the trie
        int
            the index of the first character of the word not present in the trie
        """
        node = self._root
        i = 0
        for c in word:
            try:
                # letter found, let's search the next one
                node = node._children[c]
                i += 1
            except KeyError:
                # letter not found
                return node, i
        if not node._endNode :
            node._endNode = True
            node._occurrenceList = ProbeHashMap()
        return node, i

    def searchWord(self, word):
        """
        Method to search a given word into the Trie.

        Parameters
        ----------
        word : str
            word to be searched in the trie

        Returns
        -------
        dict | None
            depending on the node having an occurrence list or not
        """
        node = self._searchNode(word)[0]
        return node._occurrenceList if node._endNode else None

    def insertWord(self, word):
        """
        Inserts a given word into the trie.

        Parameters
        ----------
        word : str
            The word to be inserted in the Trie.
        """
        node, index = self._searchNode(word)
        if index < len(word) :
            for c in word[index:-1]:
                node._children[c] = self._Node()
                node = node._children[c]
            # the last node has to be a terminator
            node._children[word[-1]] = self._Node(True)