from TdP_collections.map.red_black_tree import RedBlackTreeMap
from engine import *

wb = WebSite("www.unisa.it")

e1 = Element(wb, "diem.html", "Dipartimento di Ingegneria dell'Informazione ed Elettrica e Matematica applicata")
e2 = Element(wb, "dipartimenti")
e3 = Element(wb, "diin.html", "Dipartimento di Ingegneria Industriale")
e4 = Element(wb, "diciv.html", "Dipartimento di Ingegneria Civile")
e5 = Element(wb, "diciv")
e6 = Element(wb, "profs")
e7 = Element(wb, "auletta.html", "AAAAAAA")
e8 = Element(wb, "ferraioli.html", "BBBBBB")

wb._root.insertElementIntoDir(e2)
wb._root.insertElementIntoDir(e6)
e2.insertElementIntoDir(e1)
e2.insertElementIntoDir(e3)
e2.insertElementIntoDir(e4)
e2.insertElementIntoDir(e5)
e6.insertElementIntoDir(e7)
e6.insertElementIntoDir(e8)

test = "getSiteString"

# Test __hasDir
if test == "hasDir":

    print("Cerco",e5.getName(),"in",e2.getName())
    dir = wb.hasDir(e5.getName(), e2)
    print("Trovata:",dir.getName())

    print("Cerco","diesel","in",e2.getName())
    dir = wb.hasDir("diesel", e2)
    print("Trovata:","diesel")

    print("Cerco",e4.getName(),"in",e2.getName())
    dir = wb.hasDir(e4.getName(), e2)
    print("Trovata:",e4.getName())

    print("Cerco",e4.getName(),"in",e1.getName())
    dir = wb.hasDir(e4.getName(), e1)
    print("Trovata:",e4.getName())

# Test __newDir
elif test == "newDir":
    
    print("Cerco",e5.getName(),"in",e2.getName())
    dir = wb.newDir(e5.getName(), e2)
    print("Trovata:",dir.getName())

    print("Cerco","diesel","in",e2.getName())
    dir = wb.newDir("diesel", e2)
    print("Trovata:","diesel")

    print("Cerco",e4.getName(),"in",e2.getName())
    dir = wb.newDir(e4.getName(), e2)
    print("Trovata:",e4.getName())

    print("Cerco",e4.getName(),"in",e1.getName())
    dir = wb.newDir(e4.getName(), e1)
    print("Trovata:",e4.getName())

# Test __hasPage
elif test == "hasPage":
    
    print("Cerco",e1.getName(),"in",e2.getName())
    dir = wb.hasPage(e1.getName(), e2)
    print("Trovata:",dir.getName())

    print("Cerco","diesel.html","in",e2.getName())
    dir = wb.hasPage("diesel.html", e2)
    print("Trovata:","diesel.html")

    print("Cerco",e5.getName(),"in",e2.getName())
    dir = wb.hasPage(e5.getName(), e2)
    print("Trovata:",e5.getName())

    print("Cerco",e4.getName(),"in",e1.getName())
    dir = wb.hasPage(e4.getName(), e1)
    print("Trovata:",e4.getName())

# Test __newPage
elif test == "newPage":
    
    print("Cerco",e1.getName(),"in",e2.getName())
    dir = wb.newPage(e1.getName(), e2)
    print("Trovata:",dir.getName())

    print("Cerco","diesel.html","in",e2.getName())
    dir = wb.newPage("diesel.html", e2)
    print("Trovata:","diesel.html")

    print("Cerco",e4.getName(),"in",e1.getName())
    dir = wb.newPage(e4.getName(), e1)
    print("Trovata:",e4.getName())

    print("Cerco",e4.getName(),"in",e1.getName())
    dir = wb.newPage(e4.getName(), e1)
    print("Trovata:",e4.getName())

# Test insertPage e getSiteFromPage
elif test == "insertPage":
    
    print("Voglio inserire una pagina in diciv")
    page = wb.insertPage("www.unisa.it/dipartimenti/diciv/ciao.html","non conosco i prof")
    print("Ho creato",page.getName(),"Contenuto:",page.getContent())
    print("--- NAVIGO LA GERARCHIA PER VEDERE SE LO TROVO ---")
    dir = e5.getContent()
    page2 = dir['ciao.html']
    print("Trovato", page2.getName(), page2.getContent())
    print("Hostname da host: ", wb.getSiteFromPage(page2)._root.getName())
    print("Hostname da pagina: ", page2.getWebSite()._root.getName()) 

    # print("Voglio inserire una pagina in diciv")
    # page = wb.insertPage("www.unina.it/dipartimenti/diciv/ciao.html","non conosco i prof")

# Test getHomePage
elif test == "getHomePage":

    # non esiste
    page = wb.getHomePage()

    # creo un index.html che però non si trova nella home directory quindi deve dirmi che non esiste
    page = wb.insertPage("www.unisa.it/diem/index.html","sono la home page ma in un'altra cartella")
    page = wb.getHomePage()
    print(page.getName(), page.getContent())

    # ora la creo in root ed esiste
    page = wb.insertPage("www.unisa.it/index.html","sono la home page")
    page = wb.getHomePage()
    print(page.getName(), page.getContent())
    
# Test getSiteString
elif test == "getSiteString":

    site = WebSite("www.unisa.it")
    site.insertPage("www.unisa.it/1zz.html", "")
    site.insertPage("www.unisa.it/aaa.html", "")
    site.insertPage("www.unisa.it/index.html", "")
    site.insertPage("www.unisa.it/AAAA.html", "")
    site.insertPage("www.unisa.it/diem/daa.html", "")
    site.insertPage("www.unisa.it/diem/profs/auletta.html", "")
    site.insertPage("www.unisa.it/diem/profs/ferraioli.html", "")
    site.insertPage("www.unisa.it/diem/profs/vinci.html", "")

    print("\n---STAMPA---\n")
    print(site.getSiteString())

