import time
import webbrowser
import pandas as pd
gdf1 = pd.read_table('gravity_vectors.tsv',sep='\t', header=None)
gdf1 = gdf1.T

g = []
for i in range(gdf1.shape[0]):
    g2 = []
    
    for j in range(gdf1.shape[1]):
        aaa = gdf1[j][i]
        print(type(aaa))
        if type(aaa) == type('str'):
            
            print(aaa)
            aaa = aaa[1:-1] 
            aaa = aaa.split(', ')
            aaa = list(map(float, aaa))
            g2.append(aaa)
            print(g2)
    g.append(g2)

webbrowser.open("http://localhost/ship/index.php"); #open web browser
from abnormalitytest3 import mainfunction
time.sleep(5)
mainfunction(g)

from abnormalitytest3 import mainfunction2
time.sleep(35)
mainfunction2(g)

from abnormalitytest3 import mainfunction3
time.sleep(5)
mainfunction3(g)