
from engine import *
from TdP_collections import *

i = InvertedIndex()

# read a text file from dataset
f = open("dataset/unisa4.txt","r") 
url = f.readline()
s = f.read()
f.close()

# ho il contenuto in una stringa s e l'url in url
page = Element(WebSite("www.unisa.it"), "auletta.html", s, url)
i.addPage(page)
i._trie.printTrie()
# list = i.getList('condanno')
# print(list[page])


