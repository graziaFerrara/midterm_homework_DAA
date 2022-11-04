class CompressedTrie2:

    __slots__ = '_root' # streamline memory usage

    #-------------------------- nested _Node class --------------------------
    
    class _Node:

        __slots__ = '_children', '_endNode' ,'_occurrenceList' # streamline memory usage

        def __init__(self, endNode = False):
            self._children = {}
            self._endNode = endNode
            if self._endNode: self._occurrenceList = {}

    #------------------------------------------------------------------------

    def __init__(self):
        self._root = self._Node()

    def _isEmpty(self):
        return self._root == None

    def _lastCommonIndex(self, word, lable):
        minLength = min(len(lable), len(word)) 
        index = -1 
        for i in range(minLength): 
            if lable[i] == word[i]: 
                index += 1 
            else:
                return index
        return index

    def searchWord(self, word):
        word += '$'
        # search the word starting from the root
        searchNode = self._root
        while True:
            for k,v in searchNode._children.items():
                # check if one of the node's children has the first letter equal to the word's first letter
                if k[0] == word[0]:
                    # if it is equal I also check the other letters, otherwise I check the next children
                    index = self._lastCommonIndex(k, word)
                    # if a match is found then I check the value of the index in order to understand what to do next
                    if index == len(word) - 1 and v._endNode:
                        # completely matched the string in node v and v is an end node
                        return v._occurrenceList
                    elif index == len(k) - 1:
                        # matched the string in node v, so I have to check the remaining part in the children of node v
                        word = word[index+1:] 
                        searchNode = v
                        break
                    elif index != -1: 
                        # string partially matched in node v -> the word does not exist
                        return None

    def insertWord(self, word):
        word += '$'
        searchNode = self._root
        
        while True:
        # not empty trie  
            index = -1
            for k,v in searchNode._children.items():
                # check if one of the node's children has the first letter equal to the word's first letter
                if k[0] == word[0]:
                    # if it is equal I also check the other letters, otherwise I check the next children
                    index = self._lastCommonIndex(k, word)
                    # if a match is found then I check the value of the index in order to understand what to do next
                    if index == len(word) - 1 and v._endNode:
                        # completely matched the string in node v and v is an end node -> the word already exists
                        return
                    elif index == len(k) - 1:
                        # matched the string in node v, so I have to check the remaining part in the children of node v
                        word = word[index+1:] 
                        searchNode = v
                        break
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