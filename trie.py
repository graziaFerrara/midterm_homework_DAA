from TdP_collections.map.avl_tree import AVLTreeMap
from TdP_collections.hash_table.chain_hash_map import ChainHashMap
class CompressedTrie:

    __slots__ = '_root', '_size'

    #-------------------------- nested _Node class --------------------------
    class _Node:
        """Lightweight, nonpublic class for storing a node."""

        __slots__ = '_children', '_parent', '_lable', '_endNode' ,'_occurrenceList' # streamline memory usage

        def __init__(self, parent = None, endNode = False):
            """Creates a new node."""
            self._children = {}
            self._parent = parent
            self._endNode = endNode
            self._occurrenceList = AVLTreeMap()

    #-------------------------- nested Position class --------------------------
    class Position:

        __slots__ = '_container', '_node'

        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node

        def element(self):
            """Return the element stored at this Position."""
            return self._node

        def __eq__(self, other):
            """Return True if other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other):
            """Return True if other does not represent the same location."""
            return not (self == other)            # opposite of __eq__
        
    #------------------------------- utility methods -------------------------------s
    def _validate(self, p):
        """Return associated node, if position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:      # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """Return Position instance for given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None

    def _longestCommonPrefix(self, lable, word):
        """Return the index of the last character of the longest common prefix, -1 if it does not exist."""
        minLength = min(len(lable), len(word))
        index = -1
        for i in range(minLength):
            if lable[i] == word[i]:
                index += 1
            else:
                return index
        return index

    def printTrie(self):
        """Fornisce una stampa per livelli del TRIE """
        self._helpPrint(self._root, 0)

    def _helpPrint(self, node, level):
        if len(node._children) == 0:
            return
        for c,v in node._children.items():
            if(v._endNode):
                print((level * "---") + c + "\n")
                for item in v._occurrenceList.inorder():
                    print("Occorrenze = " + str(item.value()) + " Pagina= " + item.key()._name)
                print("\n")
            else:
                print((level * "---") + c)
            self._helpPrint(v, level + 1)

    #-------------------------- trie constructor --------------------------
    def __init__(self):
        """Create an initially empty trie."""
        self._root = self._Node("")

    #-------------------------- private accessors -------------------------
    def _searchFromNode(self, node, word):
        """Search a given word into the trie, starting from node and return the end node if it is present, None otherwise."""
        index = -1
        for k_child, v_child in node._children.items():
            index = self._longestCommonPrefix(k_child, word)
            if index != -1 : break
        # let's check the index value!
        if index == len(word) - 1:
            # word completely matched in v_child
            return v_child
        elif index == len(k_child) - 1:
            # lable completely matched in v_child
            return self._searchFromNode(v_child,word[index+1:])
        else:
            # partial match between lable and word until the computed index
            return None
    #-------------------------- public accessors --------------------------
    def root(self):
        """Return Position representing the trie's root (or None if empty)."""
        return self._make_position(self._root)

    def parent(self, p):
        """Return Position representing p's parent (or None if p is root)."""
        node = self._validate(p)
        return self._make_position(node._parent)

    def num_children(self, p):
        """Return the number of children that Position p has."""
        node = self._validate(p)
        return len(node._children)

    def children(self, p):
        """Generate an iteration of Positions representing p's children."""
        node = self._validate(p)
        return node._children

    def searchWord(self, word):
        """Search a given word into the trie, starting from the root and return the end node if it is present, None otherwise."""
        return self._searchFromNode(self._root, word + '$')

    #-------------------------- private mutators -------------------------
    def _restructureNodes(self, oldNode, oldLable, index):
        """Given a node, its associated lable and the index, perform a restructure and return the new created node."""
        oldParent = oldNode._parent # get the parent of the old node
        newNode = self._Node(oldParent, False) # create the newNode
        oldParent._children.pop(oldLable) # remove the oldNode from the parent
        oldParent._children[oldLable[:index+1]] = newNode # connect the oldParent to the newNode
        newNode._children[oldLable[index+1:]] = oldNode # connect the newNode to the oldNode
        oldNode._parent = newNode # connect the oldNode to the newNode
        oldNode._endNode = True # add terminator to the oldNode
        return newNode

    def _restructureAndAddNode(self, oldNode, oldLable, index, newLable):
        """Restructure a given node and adds a new one with a given lable."""
        # get the node in which insert a new child node
        node = self._restructureNodes(oldNode, oldLable, index)
        newNode = self._Node(node, True) # create the newNode
        node._children[newLable] = newNode # link node to newNode

    def _insertFromNode (self, node, word):
        """Insert a given word into the trie, starting from node."""
        index = -1
        for k_child, v_child in node._children.items():
            index = self._longestCommonPrefix(k_child, word)
            if index != -1 : break
        # let's check the index value!
        if index == -1:
            # no match found -> create a new node and link it to node, then return
            newNode = self._Node(node, True)
            node._children[word] = newNode
        elif index == len(word) - 1:
            # word completely matched in v_child, add terminator to it and then return 
            v_child._endNode = True
        elif index == len(k_child) - 1:
            # lable completely matched in v_child, search for the remaining part of the word in v_child's children
            self._insertFromNode(v_child,word[index+1:])
        else:
            # partial match between lable and word until the computed index, restructure the node, add the new one and then return
            self._restructureAndAddNode(v_child, k_child, index, word[index+1:])

    #-------------------------- public mutators --------------------------
    def insertWord(self, word):
        """Insert a given word into the trie, starting from the root."""
        self._insertFromNode(self._root, word + '$')
