from TdP_collections.hash_table.probe_hash_map import ProbeHashMap
from TdP_collections.hash_table.chain_hash_map import ChainHashMap

class CompressedTrie2:
    """
    A class to model a compressed Trie.

    Attributes
    ----------
    _root : _Node
        Root node of the Trie.
    """

    __slots__ = '_root' # streamline memory usage

    #-------------------------- nested _Node class --------------------------
    
    class _Node:
        """
        A class to model a node of the compressed trie.

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
            if self._endNode: self._occurrenceList = {}

    #------------------------------------------------------------------------

    def __init__(self):
        """Initialize the Standard Trie, creating an empty trie with just the root."""
        self._root = self._Node()

    def _lastCommonIndex(self, word, lable):
        minLength = min(len(lable), len(word)) 
        index = -1 
        for i in range(minLength): 
            if lable[i] == word[i]: 
                index += 1 
            else:
                return index
        return index

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
        word += '$'
        node = self._root
        length = len(word)
        last = ""
        while True:
            i = 0
            while i < length:
                if word[:i] in node._children:
                    last = word[:i]
                    break
                i += 1
            if i == length and word not in node._children:
                return node, last
            elif i == length:
                return node._children[word], last
            else:
                node = node._children[word[:i]]
                word = word[i:]
                last = word
                length = len(word) 

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
        if node._endNode: return node._occurrenceList
        else: return None

    def insertWord(self, word):
        """
        Inserts a given word into the trie.

        Parameters
        ----------
        word : str
            The word to be inserted in the Trie.
        """
        
        searchNode, last = self._searchNode(word)

        if last != "": word = last
        else: word += '$'
        wordLen = len(word)
        index = -1

        for k, v in searchNode._children.items():
            if k[0] == word[0]:
                index = self._lastCommonIndex(k,word)
                if index == wordLen - 1:
                    return 
                elif index == len(k) -1:
                    searchNode._children[word[index+1:]] = self._Node(True)
                    return
                elif index != -1:
                    # string partially matched in node v -> I have to restructure the node
                    newNode = self._Node(False) # create the newNode
                    del searchNode._children[k] # remove the oldNode from the parent
                    searchNode._children[k[:index+1]] = newNode # connect the oldParent to the newNode
                    newNode._children[k[index+1:]] = v # connect the newNode to the oldNode
                    anotherNode = self._Node(True) # create the node with the remaining part of the searched word
                    newNode._children[word[index+1:]] = anotherNode # add the node to the newNode's children
                    return
        if index == -1:
            searchNode._children[word] = self._Node(True)
            return