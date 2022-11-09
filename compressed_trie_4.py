class CompressedTrie4:
    """
    A class to model a Compressed Trie. 

    Attributes
    ----------
    _root : _Node
        Root of the Compressed Trie.

    Methods
    -------
    _searchNode
        A utility method used by the search and insert methods, to retrieve the last node of the 
        word containing the occurrence list if it is present, or the node in which the 
        insertion has to be done otherwise.
    searchWord
        A public method to search a given word into the Compressed Trie.
    insertWord
        A public method to insert a given word into the Compressed Trie, if it is not present.
    """

    __slots__ = '_root' # streamline memory usage

    #-------------------------- nested _Node class --------------------------
    
    class _Node:
        """
        A class to model a node of the Compressed Trie.

        Attributes
        ----------
        _children : dictionary
            Collection of all the children of a node. It containes (key, value)
            pairs, where the key is the initial letter of the substring contained in
            the lable of the node and the value is the associated child node.
        _endNode : bool
            Indecates if the node is an end node or not.
        _occurrenceList : dictionary 
            Collection of all the pages (keys) and their occurrences of the given 
            word (values).
        _lable : str
            Content of the node, which is a substring of a word.
        """

        __slots__ = '_children', '_endNode' ,'_occurrenceList', '_lable' # streamline memory usage

        def __init__(self, lable, endNode = False):
            """Initialize the Node."""
            self._children = {}
            self._endNode = endNode
            self._lable = lable
            if self._endNode: self._occurrenceList = {}

    #-------------------------------------------------------------------------

    def __init__(self):
        """Initialize the Compressed Trie, creating an empty trie with just the root."""
        self._root = self._Node("")

    def _searchNode(self, word: str):
        """
        A utility method used by the search and insert methods, to retrieve the last node of the 
        word containing the occurrence list if it is present, or the node in which the 
        insertion has to be done otherwise.

        Parameters
        ----------
        word : str
            The word to be searched into the trie.

        Returns
        -------
        _Node
            The last node containing a substring of the given word. 
        int
            Index of the last character of the original word which is 
            also contained into the trie.

        TIME COMPLEXITY
        ---------------
        O(len(word)) expected and amortized
            In the worst case this method iterates all over the characters of the given word once and,
            since the accesses to the dictionary are O(1) expected and amortized, it is possible to 
            conclude that the time complexity is the one reported above.
        """
        node = self._root # starts from the root
        i = 0 # counter of the index of the last character of the word present into the trie
        length = len(word)
        while i < length:
            prev = node # previous node
            try:
                node = node._children[word[i]] # try to access the child with word[i] key
            except KeyError:
                # not existing key
                return prev, i
            # existing key
            lableLen = len(node._lable)
            if node._lable != word[i:i+lableLen]:
                # the lable differs from the word
                return prev, i
            i += lableLen # update the counter
        return node, i 

    def searchWord(self, word: str):
        """
        A public method to search a given word into the Compressed Trie.

        Parameters
        ----------
        word : str
            The word to be searched into the trie.

        Returns
        -------
        dictionary | None
            The _occurrenceList if it is present in the node, None otherwise.

        TIME COMPLEXITY
        ---------------
        O(len(word)) expected and amortized
            It is the same of the _searchNode method which is called inside.
        """
        word += '$'
        node = self._searchNode(word)[0]
        return node._occurrenceList if node._endNode else None

    def insertWord(self, word: str):
        """
        A public method to insert a given word into the Compressed Trie if it is not present.

        Parameters
        ----------
        word : str
            The word to be searched into the trie.

        TIME COMPLEXITY
        ---------------
        O(len(word)) expected and amortized
            This method calls the _searchNode method, which will not reach his maximum
            complexity if the other instructions of this methos are executed. In such a case, 
            in the worst case the remaining part of the word is iterated, so that it reaches 
            the complexity of O(len(word)). It is expected and amortized due to the O(1) 
            expected and amortixed operations in the _children dictionary.
        """
        word += '$'
        node, index = self._searchNode(word)
        if index < len(word) :
            prev = node # previous node
            try:
                node = node._children[word[index]]
            except KeyError:
                # not existing key
                node._children[word[index]] = self._Node(word[index:],True)
                return
            # already existing key, it is necessary to restructure!
            lable = node._lable
            i = 0
            # search for the index of the last common character between the lable and the word (strating from index)
            for c in word[index:]:
                if c != lable[i]: break
                i += 1
            # RESTRUCTURE
            newNode = self._Node(lable[:i]) # create the new node with the substring common to both the lable and the word
            prev._children[word[index]] = newNode # replace node with newNode in the children of node's parent
            newNode._children[lable[i]] = node # insert node in newNode's children
            node._lable = lable[i:] # change the lable of node
            anotherNode = self._Node(word[index+i:],True) # create another node with the remaining part of the word
            newNode._children[word[index+i]] = anotherNode # insert the last created node in newNode's children
