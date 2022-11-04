import os
from TdP_collections.map.red_black_tree import RedBlackTreeMap
from TdP_collections.hash_table.chain_hash_map import ChainHashMap
from max_oriented_heap import MaxOrientedPriorityQueue
from compressed_trie import CompressedTrie
from time import time

class Element:
    """ 
    A class used to model both directories and webpages. 
    """

    __slots__ = ['_name','_content','_website','_url']

    def __init__(self, website, name, content = None, url = None):

        self._name = name.swapcase()
        self._url = url

        if content is not None : 
            # page
            self._content = content 
        else:
            # directory
            self._content = RedBlackTreeMap()

        self._website = website

    def getWebSite(self):
        """ 
        Returns the website which the Element belongs to. 
        """
        return self._website

    def getName(self):
        """
        Returns the name of the Element.
        """
        return self._name

    def getUrl(self):
        """Returns the url"""
        return self._url

    def getContent(self):
        """
        Returns the content of the element which is:
        • a string containing the text if the Element is a page,
        • a RB tree if the Element is a directory.
        """
        return self._content

    def insertElementIntoDir(self, elem):
        """
        If the current Element is a directory, this method inserts a new Element into it.
        """
        if type(self.getContent()) == RedBlackTreeMap: self._content[elem._name.swapcase()] = elem
        else: raise NotADirectoryException(self._name + " is not a directory.")

    def setPageContent(self, content):
        """
        If the current Element is a page, this method updates its text content field.
        """
        if type(self.getContent()) == str: self._content = content
        else: raise NotAPageException(self._name, + " is not a page.")

    def setUrl(self, url):
        self._url = url

    def __eq__(self,other):
        return self._url == other._url

    def __ne__(self,other):
        return not (self == other)

    def __lt__(self,other):
        return self._url < other._url

    def __le__(self,other):
        return self._url <= other._url

    def __gt__(self,other):
        return self._url > other._url

    def __ge__(self,other):
        return self._url >= other._url

class IndexNotFoundException(Exception):
    pass

class NotADirectoryException(Exception):
    pass

class NotAPageException(Exception):
    pass

class DirectoryNotFoundException(Exception):
    pass

class PageNotFoundException(Exception):
    pass

class NotValidURLException(Exception):
    pass

class NOOccurrenceListException(Exception):
    pass

class WebSite:

    __slots__ = ['_root', '_index']

    def __init__(self, host):
        """
        Creates a new WebSite object for saving the website hosted at host, 
        where host is a string.
        """
        self._root = Element(self, host) # the root Element is a directory whose name is host
        self._index = None # index.html page

    def __isDir(self, elem): 
        """
        Given an element, returns True if it is a directory, False otherwise.
        """
        return type(elem.getContent()) == RedBlackTreeMap

    def __isPage(self, elem):
        """
        Given an element, returns True if it is a page, False otherwise.
        """
        return type(elem.getContent()) == str

    def __hasDir(self, ndir, cdir):
        """
        If in the current directory cdir there is a directory whose name is ndir, 
        then it returns a reference to this directory, otherwise it throws an exception. 
        An exception must be thrown even if the cdir is not a directory.
        """
        if not self.__isDir(cdir): 
            raise NotADirectoryException(cdir.getName() + " is not a directory!")
        try:
            currCont = cdir.getContent()
            dir = currCont[ndir]
        except KeyError as k: 
            raise DirectoryNotFoundException("Directory " + ndir + " not found!")
        if not self.__isDir(dir): 
            raise NotADirectoryException(dir.getName() + " is not a directory!")
        return dir

    def __newDir(self, ndir, cdir):
        """
        If in the current directory cdir there is a directory whose name is ndir, 
        then it returns a reference to this directory, otherwise it creates such a 
        directory and returns a reference to it. An exception must be thrown even 
        if the cdir is not a directory.
        """
        try:
            dir = self.__hasDir(ndir, cdir)
        except DirectoryNotFoundException:
            dir = Element(self, ndir)
            cdir.insertElementIntoDir(dir)
        return dir

    def __hasPage(self, npag, cdir):
        """
        If in the current directory cdir there is a webpage whose name is npage, 
        then it returns a reference to this page, otherwise it throws an exception. 
        An exception must be thrown even if the cdir is not a directory.
        """
        if not self.__isDir(cdir): 
            raise NotADirectoryException(cdir.getName() + " is not a directory!")
        try:
            currCont = cdir.getContent()
            pag = currCont[npag]
        except KeyError as k:
            raise PageNotFoundException("Page " + npag + " not found!")
        if not self.__isPage(pag): 
            raise NotAPageException(pag.getName() + " is not a page!")
        return pag

    def __newPage(self, npag, cdir):
        """
        If in the current directory cdir there is a webpage whose name is npage, then it returns a 
        reference to this page, otherwise it creates such a page and returns a reference to it. An 
        exception must be thrown even if the cdir is not a directory. 
        """
        try:
            pag = self.__hasPage(npag, cdir)
        except PageNotFoundException:
            pag = Element(self, npag, "")
            cdir.insertElementIntoDir(pag)
        return pag

    def getHomePage(self):
        """
        Returns the home page of the website at which the current object refers or it throws 
        an exception if an home page does not exist.
        """
        if self._index is None: raise IndexNotFoundException("There's no index.html page!")
        else: return self._index

    def __composeSiteString(self, cdir, n):
        s = ""
        iter = cdir.getContent().inorder()
        for p in iter:
            s += '-' * n
            el = p.value()
            s += ' ' + el.getName() + '\n'
            if self.__isDir(el): 
                s += self.__composeSiteString(el, n+3)
        return s

    def getSiteString(self):
        """
        Returns a string showing the structure of the website.
        """ 
        return self._root.getName().swapcase() + '\n' + self.__composeSiteString(self._root, 3)

    def insertPage(self, url, content):
        """
        It saves and returns a new page of the website, where url is a string representing the url of 
        the page, and content is a string representing the text contained in the page.
        """
        path = url.swapcase().split('/') # split the path of the page
        # the url hostname is not the one of the website
        if path[0] != self._root.getName(): 
            raise NotValidURLException(url + " is not valid for this host.")
        # the page to be inserted is the homepage
        elif path[1] == 'index.html' and len(path) == 2:
            page = Element(self, path[len(path)-1], content, url)
            self._root.insertElementIntoDir(page)
            self._index = page
        # search/create parent folders along the way and create + insert the page
        else:
            searchDir = self._root 
            for p in path[1:len(path)-1]:
                searchDir = self.__newDir(p, searchDir)
            page = self.__newPage(path[len(path)-1],searchDir)
            page.setUrl(url)
            page.setPageContent(content)
        return page

    def getSiteFromPage(self, page):
        """
        Given an Element page returns the WebSite object that page belongs to.
        """
        return page.getWebSite()

class InvertedIndex:

    __slots__ = ['_trie']

    def __init__(self):
        """
        Creates a new empty InvertedIndex.
        """
        self._trie = CompressedTrie()

    def addWord(self, keyword):
        """
        Adds the string keyword into the InvertedIndex.
        """
        self._trie.insertWord(keyword)

    def addPage(self, page):
        """
        It processes the Element page, and for each word in its content, this word is inserted in the inverted index if it is not present, 
        and the page is inserted in the occurrence list of this word. The occurrence list also saves the number of occurrences of the word in the page.
        """
        text = page.getContent().split()
        for word in text:
            self.addWord(word) # adds the word to the trie    
            list = self.getList(word) # returns the occurrence list
            try:
                # already exists
                list[page] += 1
            except KeyError:
                # not existing yet
                list[page] = 1

    def getList(self, keyword):
        """
        It takes in input the string keyword, and it returns the corresponding occurrence list. 
        It throws an Exception if there is no occurrence list associated with the string keyword
        """
        node = self._trie.searchWord(keyword) 
        if not node._endNode or node is None : raise NOOccurrenceListException("Occurrence list not found!")
        return node._occurrenceList 

class SearchEngine:

    __slots__ = ['_invertedIndex', '_database']

    def __init__(self, namedir):
        """
        Initializes the SearchEngine, by taking in input a directory in which there are multiple files each representing a different webpage. 
        Each file contains in the first line the URL (including the hostname) and in the next lines the content of the webpage. This function 
        populates the database of the search engine, by initializing and inserting values in all the necessary data structures.
        """
        self._invertedIndex = InvertedIndex()
        self._database = ChainHashMap()

        currDir = os.getcwd()
        os.chdir(namedir)

        for file in os.listdir():
            if file.endswith(".txt"):
                with open (file, 'r') as f:
                    firstLine = f.readline()
                    content = f.read()
                    splittedLine = firstLine.split('/')
                    hostname = splittedLine[0]
                    try:
                        page = self._database[hostname].insertPage(firstLine[:-1], content)
                    except KeyError:
                        self._database[hostname] = WebSite(hostname)
                        page = self._database[hostname].insertPage(firstLine[:-1], content)
                    self._invertedIndex.addPage(page)

        os.chdir(currDir)

    def search(self, keyword, k):
        """
        Searches the k web pages with the maximum number of occurrences of the searched keyword. It returns a string s built as follows: for 
        each of these k pages sorted in descending order of occurrences, the site strings (as defined above) of the site hosting that page is 
        added to s, unless this site has been already inserted.
        """
        dict = {}                                   # O(1)
        s = ""
        list = self._invertedIndex.getList(keyword) # O(m)
        maxHeap = MaxOrientedPriorityQueue(list)    # O(n•log(k))
        for i in range(k):       #
            k,v = maxHeap.remove_max()              # O(k•log(k))
            site = v.getWebSite()
            try:
                if dict[site] > 1: 
                    dict[site] += 1
            except KeyError:
                dict[site] = 1
                s += site.getSiteString()
        return s[:-1]
        


    