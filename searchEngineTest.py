from engine import * 
from time import time

# for i in range(50):
#     start = time()
#     s = SearchEngine("dataset")
#     end=time()-start
#     print(end,'s')
start = time()
s = SearchEngine("dataset")
str = s.search('soppressa', 10)
end=time()-start
print(end,'s')
print(str)