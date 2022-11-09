from TdP_collections.hash_table.probe_hash_map import ProbeHashMap

class Trie:
    """
    A class to model a Standard Trie.
    
    Attributes
    ----------
    _root : _Node
        Root of the Standard Trie.

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
        A class to model a node of a Standard Trie.
        
        Attributes
        ----------
        _children : dictionary
            Collection containing the children of a _Node.
        _endNode : bool
            It is True if the _Node is an end node, False otherwise.
        _occurrenceList : dictionary
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
        node, index = self._searchNode(word)
        if index < len(word) :
            for c in word[index:-1]:
                node._children[c] = self._Node()
                node = node._children[c]
            # the last node has to be a terminator
            node._children[word[-1]] = self._Node(True)