from TdP_collections.map.red_black_tree import RedBlackTreeMap


class CompressedTrie:
    """Representation of a compressed trie structure.

        Attributes
        ----------
            _root : _Node
                Root node of the compressed trie.
    """

    __slots__ = '_root'

    #-------------------------- nested _Node class --------------------------
    class _Node:
        """Lightweight, nonpublic class for storing a node.

            Attributes
            ----------
                _children : dictionary
                    Dictionary containing.
                _parent : _Node
                    Reference to the parent node of the current node.
                _endNode : bool
                    Indicates if the node is an end node or not.
                _occurrenceList : RedBlackTreeMap
                    If the node is an end node then it owns an occurrence list.
        """

        __slots__ = '_children', '_parent', '_endNode' ,'_occurrenceList' # streamline memory usage

        def __init__(self, parent = None, endNode = False):
            """Creates a new node.

                Parameters
                ----------
                    parent : _Node | None
                        Optional reference to the parent node, defaults to None.
                    endNode : bool
                        Indicates if the node is an end node or not.
            """
            self._children = {}
            self._endNode = endNode
            self._parent = parent
            self._occurrenceList = RedBlackTreeMap()

    #-------------------------- utility methods --------------------------
    def _longestCommonPrefix(self, lable, word):
        """Return the index of the last matching character.
        
            Parameters
            ----------
                lable : str
                    Lable of a node.
                word : str
                    Word on which the match with the node's lable has to be done.

            Returns
            -------
                index : int
                    An integer representing the index of the last matching character between the two strings,
                    -1 if no match is found.
        """
        minLength = min(len(lable), len(word)) # O(n)
        index = -1 # O(1)
        for i in range(minLength): # O(n)
            if lable[i] == word[i]: # O(1)
                index += 1 # O(1)
            else:
                return index
        return index
        # Total time complexity: O(n)

    #-------------------------- trie constructor --------------------------
    def __init__(self):
        """Create an initially empty trie."""
        self._root = self._Node("")

    #-------------------------- private accessors -------------------------
    def _searchFromNode(self, node, word):
        """Search a given word into the trie.
        
            Parameters
            ----------
            node : _Node
                Node from which start searching.
            word : str
                Word to be searched in the trie.

            Returns
            -------
            v_child | None : _Node
                Return the node if the word is present, None otherwise.
        """
        index = -1
        for k_child, v_child in node._children.items():
            index = self._longestCommonPrefix(k_child, word)
            if index != -1 : break
        # let's check the index value!
        if index == len(word) - 1:
            # word completely matched in v_child
            return v_child._occurrenceList
        elif index == len(k_child) - 1:
            # lable completely matched in v_child
            return self._searchFromNode(v_child,word[index+1:])
        else:
            # partial match between lable and word until the computed index
            return None
    #-------------------------- public accessors --------------------------

    def searchWord(self, word):
        """Search a given word into the trie, starting from the root and return the end node if it is present, None otherwise.

            Parameters
            ----------
            word : str
                Word to search in the trie.

            Returns
            -------
            Returns the result of the _searchFromNode method.

        """
        return self._searchFromNode(self._root, word + '$')

    #-------------------------- private mutators -------------------------
    def _restructureNodes(self, oldNode, oldLable, index):
        """Given a node, its associated lable and the index, perform a restructure and return the new created node.

            Parameters
            ----------
            oldNode : _Node
                Node to be restructured.
            oldLable : str
                String representing the lable of the old node.
            index : int
                Index in which cut the lable, to create distinct two.

            Returns
            -------
            newNode : _Node
                New node to be created.
        """
        oldParent = oldNode._parent # get the parent of the old node
        newNode = self._Node(oldParent, False) # create the newNode
        del oldParent._children[oldLable] # remove the oldNode from the parent
        oldParent._children[oldLable[:index+1]] = newNode # connect the oldParent to the newNode
        newNode._children[oldLable[index+1:]] = oldNode # connect the newNode to the oldNode
        oldNode._parent = newNode # connect the oldNode to the newNode
        oldNode._endNode = True # add terminator to the oldNode
        return newNode

    def _restructureAndAddNode(self, oldNode, oldLable, index, newLable):
        """Restructure a given node and adds a new one with a given lable.
        
            Parameters
            ----------
            oldNode : _Node
                Node which has to be restructured.
            oldLable : str
                Lable of the old node which has to be restructured.
            index : int
                Index of the last matching character betwwen the lable and the word.
            newLable : str
                New lable to be inserted,
        """
        # get the node in which insert a new child node
        node = self._restructureNodes(oldNode, oldLable, index) # O(1)
        newNode = self._Node(node, True) # create the newNode, O(1)
        node._children[newLable] = newNode # link node to newNode O(1)

    def _insertFromNode (self, node, word):
        """Insert a given word into the trie, starting from node.

            Parameters
            ----------
                node : _Node
                    Is the node from which begin the insertion process.
                word : str
                    Is the word to insert in the compressed trie.
        """
        index = -1 # O(1)
        for k_child, v_child in node._children.items(): # worst case O(d) -> each node has at least two children and at most d (where d is the size of the alphabet) children
            index = self._longestCommonPrefix(k_child, word) # O(m)
            if index != -1 : break # O(1)
        # let's check the index value!
        if index == -1: # O(1)
            # no match found -> create a new node and link it to node, then return
            newNode = self._Node(node, True) # O(1)
            node._children[word] = newNode # O(1)
        elif index == len(word) - 1: # O(1)
            # word completely matched in v_child, add terminator to it and then return 
            v_child._endNode = True # O(1)
        elif index == len(k_child) - 1: # O(1)
            # lable completely matched in v_child, search for the remaining part of the word in v_child's children
            self._insertFromNode(v_child,word[index+1:]) # at most m, where m is the length of the word
        else:
            # partial match between lable and word until the computed index, restructure the node, add the new one and then return
            self._restructureAndAddNode(v_child, k_child, index, word[index+1:]) # O(1)
        # Total time complexity: O(d•m) in the worst case

    #-------------------------- public mutators --------------------------
    def insertWord(self, word):
        """Insert a given word into the trie, starting from the root.
        
        Parameters
        ----------
            word : str
                Word to be searched into the trie.
        """
        self._insertFromNode(self._root, word + '$')
