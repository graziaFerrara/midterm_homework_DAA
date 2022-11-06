import os
from TdP_collections.map.red_black_tree import RedBlackTreeMap
from TdP_collections.hash_table.chain_hash_map import ChainHashMap
from TdP_collections.hash_table.probe_hash_map import ProbeHashMap
from max_oriented_heap import MaxOrientedPriorityQueue
from compressed_trie import CompressedTrie
from compressed_trie_2 import CompressedTrie2
from trie import Trie

class Element:
    """ 
    A class used to model both directories and webpages. 

    Attributes
    ----------
    _name : str
        Name of the Element.
    _content : str | RedBlackTreeMap
        Content of the Element.
    _website : WebSite
        Website to which the Element belongs to.
    _url : str | None
        URL of the Element.

    Methods
    -------
    getWebSite()
        Returns the WebSite the Element belongs to.
    getName()
        Returns the name of the Element.
    getUrl()
        Returns the url of the Element if specified.
    getContent()
        Returns the content of the Element.
    insertElementIntoDir()
        Inserts a given element into the current directory (if the Element is a directory).
    setPageContent()
        Inserts a content into the current Element, if the current Element is a page.
    setUrl()
        Sets the url of the current element.
    """

    __slots__ = ['_name','_content','_website','_url']

    def __init__(self, website, name, content = None, url = None):
        """
        Initializes an Element. 

        Parameters
        ----------
        website : WebSite
            The WebSite which the Element belongs to.
        name : str
            Name of the Element.
        content : str | None
            Content of the page, if passed as parameter.
        url : str | None
            URL of the page, if passed as parameter.
        """

        self._name = name
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
        Public accessor method.

        Returns
        -------
        WebSite 
            The WebSite the current Element belongs to.
        """
        return self._website

    def getName(self):
        """
        Public accessor method.

        Returns
        -------
        str
            The name of the current Element.
        """
        return self._name

    def getUrl(self):
        """
        Public accessor method.

        Returns
        -------
        str
            The url of the current Element.

        Raises
        ------
        URLNotFoundException
            If the url is None.
        """
        if self._url is None: 
            raise URLNotFoundException("There's no URL in the current Element")
        return self._url 

    def getContent(self):
        """
        Public accessor method.

        Returns 
        -------
        str | RedBlackTreeMap
            The content of the Element.
        """
        return self._content

    def insertElementIntoDir(self, elem):
        """
        Public mutator method.
        If the current Element is a directory, this method inserts a new Element into it.

        Parameters
        ----------
        elem : Element
            Element to insert into the current directory.

        Raises
        ------
        NotADirectoryException
            If the current Element is not a directory.
        """
        if type(self.getContent()) == RedBlackTreeMap: self._content[elem._name.swapcase()] = elem
        else: raise NotADirectoryException(self._name + " is not a directory.")

    def setPageContent(self, content):
        """
        Public mutator method.
        If the current Element is a page, this method updates its text content field.

        Parameters
        ----------
        content : str
            Sets the content of the current Element if it is a page.

        Raises
        ------
        NotAPageException
            If the current Element is not a page.
        """
        if type(self.getContent()) == str: self._content = content
        else: raise NotAPageException(self._name + " is not a page.")

    def setUrl(self, url):
        """
        Public mutator method.

        Parameters
        ----------
        url : str
            Sets the url of the current Element.
        """
        self._url = url

    # ----------------- Elements comparison methods -----------------

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

    # --------------------------- hash -------------------------------
    def __hash__(self) -> int:
        return hash(self._url)

# ---------------------- Exception classes ---------------------------

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

class URLNotFoundException(Exception):
    pass

class NOOccurrenceListException(Exception):
    pass

# --------------------------------------------------------------------

class WebSite:
    """
    A class used to model a structured collection of webpages that reside on the same host.

    Attributes
    ----------
    _root : Element
        Element representing the root directory of the WebSite.
    _index : Element
        Element representing the home page of the WebSite.

    Methods
    -------
    __isDir
        Checks if a given Element is a directory.
    __isPage
        Checks if a given Element is a page.
    __hasDir
        Checks if a given directory is contained in the current directory.
    __hasPage
        Checks if a given page is contained in the current directory.
    __newDir
        Inserts a new directory in the current directory.
    __newPage
        Inserts a new page into the current directory.
    __composeSiteString
        Utility recursive method to build the site description string.
    getHomePage
        Returns the home page (Element) of the WebSite.
    getSiteString
        Returns a string showing the structure of the website.
    insertPage
        Saves and returns a new page Element of the WebSite.
    getSiteFromPage
        Returns the WebSite which a given page Element belongs to.
    """

    __slots__ = ['_root', '_index']

    def __init__(self, host):
        """
        Creates a new WebSite object for saving the website hosted at host, where host is a string.
    
        Parameters
        ----------
        host : str
            Represents the host of the current WebSite.

        TIME COMPLEXITY 
        ---------------
        O(1)
        """
        self._root = Element(self, host) 
        self._index = None 

    def __isDir(self, elem): 
        """
        If the object Element referenced by elem is a directory returns True, 
        otherwise it returns False. The format of elem is not constrained.

        Parameters
        ----------
        elem : Element
            Element on which the type check has to be done.

        Returns
        -------
        bool
            Is True if the given Element is a directory, False otherwise.
        
        TIME COMPLEXITY 
        ---------------
        O(1)
        """
        return type(elem.getContent()) == RedBlackTreeMap

    def __isPage(self, elem):
        """
        If the object Element referenced by elem is a web page returns True, 
        otherwise it returns False. The format of elem is not constrained.

        Parameters
        ----------
        elem : Element
            Element on which the type check has to be done.

        Returns
        -------
        bool
            Is True if the given Element is a page, False otherwise.
        
        TIME COMPLEXITY
        ---------------
        O(1)
        """
        return type(elem.getContent()) == str

    def __hasDir(self, ndir, cdir):
        """
        If in the current directory cdir there is a directory whose name is ndir, 
        then it returns a reference to this directory, otherwise it throws an exception. 
        An exception must be thrown even if the cdir is not a directory. Here ndir is 
        a string, while cdir and the return value are objects of the class Element.

        Parameters
        ----------
        ndir : str
            Name of the directory to be searched.
        cdir : Element
            Directory in which search the given directory.

        Returns
        -------
        Element
            Reference to the directory that has been found.

        Raises
        ------
        NotADirectoryException
            If the parameter cdir is not a directory or the new found Element is 
            not a directory.
        DirectoryNotFoundException
            If no directory named ndir has been found.

        TIME COMPLEXITY 
        ---------------
        O(log(k)) 
            Since the content of the Element cdir is a RedBlackTreeMap, the search is proportional 
            to the logarithm of the number of nodes of the tree, which is k.
        """
        if not self.__isDir(cdir): 
            raise NotADirectoryException(cdir.getName() + " is not a directory!")
        try:
            currCont = cdir.getContent()
            dir = currCont[ndir.swapcase()]
        except KeyError: 
            raise DirectoryNotFoundException("Directory " + ndir + " not found!")
        if not self.__isDir(dir): 
            raise NotADirectoryException(dir.getName() + " is not a directory!")
        return dir

    def __newDir(self, ndir, cdir):
        """
        If in the current directory cdir there is a directory whose name is ndir, 
        then it returns a reference to this directory, otherwise it creates such a 
        directory and returns a reference to it. An exception must be thrown even 
        if the cdir is not a directory. Here ndir is a string, while cdir and the 
        return value are objects of the class Element.

        Parameters
        ----------
        ndir : str
            Name of the directory to be created if not already existing.
        cdir : Element  
            Directory in which search the given directory.

        Returns
        -------
        Element
            Reference to the directory which has been found or created.

        Raises
        ------
        NotADirectoryException
            Through the call to the previous defined method __hasDir.

        TIME COMPLEXITY 
        ---------------
        O(log(k)) 
            In both the possible situations (the directory already exists | the 
            directory does not exist yet) the call to the _hasDir function is executed.
            This call takes time O(log(k)). Then, if the dir has been found, it returns it, 
            otherwise the directory is created O(1) and inserted in cdir's content (RedBlackTreeMap) 
            in O(log(k)).
            The total amount of time spent is in the O(log(k)) order.
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
        An exception must be thrown even if the cdir is not a directory. Here npage 
        is a string, while cdir and the return value are objects of the class Element.

        Parameters
        ----------
        npag : str
            Name of the page to be searched.
        cdir : Element
            Directory in which search the given directory.

        Returns
        -------
        Element
            Reference to the page that has been found.

        Raises
        ------
        NotADirectoryException
            If the parameter cdir is not a directory.

        PageNotFoundException
            If the page named npag has not been found.

        NotAPageException
            If the Element which has been found is not a page.

        TIME COMPLEXITY 
        ---------------
        O(log(k)) 
            Since the content of the Element cdir is a RedBlackTreeMap, the search is proportional 
            to the logarithm of the number of nodes of the tree, which is k.
        """
        if not self.__isDir(cdir): 
            raise NotADirectoryException(cdir.getName() + " is not a directory!")
        try:
            currCont = cdir.getContent()
            pag = currCont[npag.swapcase()]
        except KeyError:
            raise PageNotFoundException("Page " + npag + " not found!")
        if not self.__isPage(pag): 
            raise NotAPageException(pag.getName() + " is not a page!")
        return pag

    def __newPage(self, npag, cdir):
        """
        If in the current directory cdir there is a webpage whose name is npage, 
        then it returns a reference to this page, otherwise it creates such a page 
        and returns a reference to it. An exception must be thrown even if the cdir 
        is not a directory. Here ndir is a string, while cdir and the return value 
        are objects of the class Element.

        Parameters
        ----------
        npag : str
            Name of the page to be searched.
        cdir : Element
            Directory in which search the given directory.

        Returns
        -------
        Element
            Reference to the page which has been found or created.

        Raises
        ------
        NotADirectoryException
            If the parameter cdir is not a directory.

        NotAPageException
            If the Element which has been found or created is not a page.

        TIME COMPLEXITY 
        ---------------
        O(log(k)) 
            In both the possible situations (the page already exists | the 
            page does not exist yet) the call to the _hasPage function is executed.
            This call takes time O(log(k)). Then, if the page has been found, it returns it, 
            otherwise the page is created O(1) and inserted in cdir's content (RedBlackTreeMap) 
            in O(log(k)).
            The total amount of time spent is in the O(log(k)) order.
        """
        try:
            pag = self.__hasPage(npag, cdir)
        except PageNotFoundException:
            pag = Element(self, npag, "")
            cdir.insertElementIntoDir(pag)
        return pag

    def __composeSiteString(self, cdir, n):
        """
        Recursive utility method whose aim is to build the string which describes the 
        structure of the site.

        Parameters
        ----------
        cdir : Elem
            Directory of which describing the content.
        n : int
            Number of dashes to be inserted in a level.

        Returns
        -------
        str 
            String describing the structure of the WebSite.

        TIME COMPLEXITY 
        ---------------
        O(n)
            Each node of each directory's content is only visited once, so the total amount 
            of time spent is proportional to the number of nodes.
        """
        s = ""
        iter = cdir.getContent().inorder()
        for p in iter:
            s += '-' * n
            el = p.value()
            s += ' ' + el.getName() + '\n'
            if self.__isDir(el): 
                s += self.__composeSiteString(el, n+3)
        return s

    def getHomePage(self):
        """
        Returns the home page of the website at which the current object refers or it throws 
        an exception if an home page does not exist.

        Returns
        -------
        Element
            The home page Element of the site.

        Raises
        ------
        IndexNotFoundException
            If the home page has not been found.

        TIME COMPLEXITY 
        ---------------
        O(1)
            Only accesses the _index WebSite's attribute.
        """
        if self._index is None: raise IndexNotFoundException("There's no index.html page!")
        else: return self._index

    def getSiteString(self):
        """
        Returns a string showing the structure of the website.

        Returns
        -------
        str
            The string showing the structure of the WebSite.

        TIME COMPLEXITY 
        ---------------
        O(n)
            It calls the __composeSiteString utility method, which takes time O(n) and
            then appends the resulting string to the hostname O(1). So the total amount of time 
            spent is in the O(n) order.
        """ 
        return self._root.getName() + '\n' + self.__composeSiteString(self._root, 3)

    def insertPage(self, url, content):
        """
        It saves and returns a new page of the website, where url is a string representing the url of 
        the page, and content is a string representing the text contained in the page.

        Parameters
        ----------
        url : str
            The url of the page to save in the WebSite.
        content : str
            The content of the page to save in the WebSite.

        Returns
        -------
        Element
            The just created page.

        Raises
        ------
        NotValidURLException
            If the given URL is not equal to the one of the current WebSite.

        TIME COMPLEXITY 
        ---------------
        O(l•log(k))
            In the home page insertion case, the total time amount spent
            is O(log(k)). While in a general case, first it is necessary to search/create
            all the new Element's parent directories and then insert the new page.
            This requires l (number of anchestors of the page) times a logarithmic
            time proportional to the content of each directory, which is k.
        """
        path = url.split('/') 
        length = len(path) - 1
        if path[0] != self._root.getName(): 
            raise NotValidURLException(url + " is not valid for this host.")
        # the page to be inserted is the homepage
        elif path[1] == 'index.html' and length == 1:
            page = self.__newPage('index.html',self._root)
            page.setUrl(url)
            page.setPageContent(content)
            self._index = page
        # search/create parent folders along the way and create + insert the page
        else:
            searchDir = self._root 
            for p in path[1:length]:
                searchDir = self.__newDir(p, searchDir)
            page = self.__newPage(path[length],searchDir)
            page.setUrl(url)
            page.setPageContent(content)
        return page

    @staticmethod
    def getSiteFromPage(page):
        """
        Given an Element page returns the WebSite object that page belongs to.

        Return
        ------
        WebSite
            The website the given page belongs to.

        TIME COMPLEXITY
        ---------------
        O(1)
            Only accesses the WebSite Element's attribute.
        """
        return page.getWebSite()

# --------------------------------------------------------------------

class InvertedIndex:
    """
    A class to model an inverted index which contains the core information stored by a 
    search engine.

    Attributes
    ----------
    _trie : Trie
        Trie storing all the words.

    Methods
    -------
    addWord
        Adds a word to the inverted index.
    addPage
        Adds the words of a given page's content to the Inverted Index.
    getList
        Returns the occurrence list associated to a given word.
    """

    __slots__ = ['_trie']

    def __init__(self):
        """
        Creates a new empty InvertedIndex.

        TIME COMPLEXITY
        ---------------
        O(1)
        """
        self._trie = Trie()

    def addWord(self, keyword):
        """
        Adds the string keyword into the InvertedIndex.

        Parameters
        ----------
        keyword : str
            String to be inserted into the InvertedIndex.

        TIME COMPLEXITY
        ---------------
        O(len(keyword))
            The insertion in the standard Trie, takes an expected and amortized time 
            proportional to the length of the word to be inserted.
        """
        self._trie.insertWord(keyword)

    def addPage(self, page):
        """
        It processes the Element page, and for each word in its content, this word is inserted 
        in the inverted index if it is not present, and the page is inserted in the occurrence 
        list of this word. The occurrence list also saves the number of occurrences of the 
        word in the page.

        Parameters
        ----------
        page : Element
            Page of which processing the words.

        TIME COMPLEXITY
        ---------------
        O(len(word))
            Since the expected time to add a word to the InvertedIndex is O(len(word)) and so it
            is the expected time to get the occurrence list of the given word, and the time to insert
            something in the occurrence list (implemented as a hash table) is expected and amortized  
            O(1), the total amount of required time is in the order of O(len(word)).
        """
        text = page.getContent().split()
        for word in text:
            self.addWord(word) 
            list = self.getList(word) 
            try:
                # already exists
                list[page] += 1
            except KeyError:
                # not existing yet
                list[page] = 1

    def getList(self, keyword):
        """
        It takes in input the string keyword, and it returns the corresponding occurrence list. 
        It throws an Exception if there is no occurrence list associated with the string keyword.

        Parameters
        ----------
        keyword : str
            The word of which return the occurrence list.

        Returns
        -------
        list : dictionary
            The occurrence list

        Raises
        ------
        NOOccurrenceListException
            if there's no occurrence list associated to the given keyword.

        TIME COMPLEXITY
        ---------------
        O(len(keyword))
            The expected and amortized to return the occurrence list associated to a given keyword, 
            which is the time spent by the search method in the standard trie, is proportional to 
            the length of the keyword.
        """
        list = self._trie.searchWord(keyword) 
        if list is None : raise NOOccurrenceListException("Occurrence list not found!")
        return list

# --------------------------------------------------------------------

class SearchEngine:
    """
    A class to model a search engine, which allows users to retrieve relevant information from
    the collected webpages.

    Attributes
    ----------
    _invertedIndex : InvertedIndex
        Inverted Index of the search engine.
    _database : dictionary
        Collection of the WebSites.

    Methods
    -------
    search
        searches the k web pages with the maximum number of occurrences of a keyword, and resturns
        the concatenation of the string description of all the possible sites.
    """

    __slots__ = ['_invertedIndex', '_database']

    def __init__(self, namedir):
        """
        Initializes the SearchEngine, by taking in input a directory in which there are multiple files each representing a different webpage. 
        Each file contains in the first line the URL (including the hostname) and in the next lines the content of the webpage. This function 
        populates the database of the search engine, by initializing and inserting values in all the necessary data structures.

        Parameters
        ----------
        namedir : str
            Name of the directory from which read all the files.
        """
        self._invertedIndex = InvertedIndex()
        self._database = {}

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

        Parameters
        ----------
        keyword : str
            word to be searched in the different pages
        k : int
            number of pages to search

        Returns
        -------
        str
            concatenation of the string description of the structure of all the websites with the higher number of occurrences of the given word
            in order of number of occurrences and without duplicates.
        """                  
        s = ""
        list = self._invertedIndex.getList(keyword) 
        maxHeap = MaxOrientedPriorityQueue(list)  
        length = min(len(maxHeap),k)
        map = {}
        while length > 0:       
            k,v = maxHeap.remove_max()              
            site = WebSite.getSiteFromPage(v)
            try:
                if map[site] > 1: 
                    map[site] += 1
            except KeyError:
                map[site] = 1
                s += site.getSiteString()
            length -= 1
        return s[:-1]
        


    