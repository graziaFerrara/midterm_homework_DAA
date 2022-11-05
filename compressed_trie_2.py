from TdP_collections.hash_table.probe_hash_map import ProbeHashMap
from TdP_collections.hash_table.chain_hash_map import ChainHashMap
from TdP_collections.map.red_black_tree import RedBlackTreeMap
from TdP_collections.map.avl_tree import AVLTreeMap

class CompressedTrie2:

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
        """Returns the node in which the word should end."""
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
        node = self._searchNode(word)[0]
        if node._endNode: return node._occurrenceList
        else: return None

    def insertWord(self, word):
        
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