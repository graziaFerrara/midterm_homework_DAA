from TdP_collections.map.red_black_tree import RedBlackTreeMap
from TdP_collections.hash_table.chain_hash_map import ChainHashMap
from TdP_collections.hash_table.probe_hash_map import ProbeHashMap

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
                _endNode : bool
                    Indicates if the node is an end node or not.
                _occurrenceList : dictionary
                    If the node is an end node then it owns an occurrence list.
        """

        __slots__ = '_children', '_endNode' ,'_occurrenceList' # streamline memory usage

        def __init__(self, endNode = False):
            """Creates a new node.

                Parameters
                ----------
                    endNode : bool
                        Indicates if the node is an end node or not.
            """
            self._children = ProbeHashMap(57)
            self._endNode = endNode
            if self._endNode: self._occurrenceList = ProbeHashMap()

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
        self._root = self._Node()

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
            if k_child[0] == word[0]:
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
            if k_child[0] == word[0]:
                index = self._longestCommonPrefix(k_child, word) # O(m)
                if index != -1 : break # O(1)
        # let's check the index value!
        if index == -1: # O(1)
            # no match found -> create a new node and link it to node, then return
            newNode = self._Node(True) # O(1)
            node._children[word] = newNode # O(1)
        elif index == len(word) - 1: # O(1)
            # word completely matched in v_child, add terminator to it and then return 
            v_child._endNode = True # O(1)
        elif index == len(k_child) - 1: # O(1)
            # lable completely matched in v_child, search for the remaining part of the word in v_child's children
            self._insertFromNode(v_child,word[index+1:]) # at most m, where m is the length of the word
        else:
            # partial match between lable and word until the computed index, restructure the node, add the new one and then return
            newNode = self._Node(False) # create the newNode
            del node._children[k_child] # remove the oldNode from the parent
            node._children[k_child[:index+1]] = newNode # connect the oldParent to the newNode
            newNode._children[k_child[index+1:]] = v_child # connect the newNode to the oldNode
            v_child._endNode = True # add terminator to the oldNode
            anotherNode = self._Node(True) # create the node with the remaining part of the searched word
            newNode._children[word[index+1:]] = anotherNode # add the node to the newNode's children
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
