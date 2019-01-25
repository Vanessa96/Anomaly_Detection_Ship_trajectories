import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as ptc
import pymysql.cursors
import statistics
import csv
import math
import pandas as pd
from gmplot import gmplot
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from dbscanfa import MyDBSCAN
from numpy import array
from sklearn.cluster import KMeans

datast = []
datamov = []
datamovlatactual = []
datamovlat = []

datamovspd = []


with open('danishdata.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    i=0
    
    for row in readCSV:
        if(i==0 or row[2]=='' or row[3]=='' or row[7]=='' or row[8]==''):
            i=1
        else:
            data = float(row[7])
            
            if(data > 0.5):
                datamov.append([row[0],row[2],float(row[3]),float(row[4]),float(row[7]),float(row[8])])
            else:
                datast.append([row[0],row[2],float(row[3]),float(row[4]),float(row[7]),float(row[8])])
                
            
            
    for r in datamov:
        datamovlatactual.append([r[2],r[3]])
        datamovspd.append([r[4],r[5]])
        
    datamovlat= StandardScaler().fit_transform(datamovlatactual)
        
print ("Running my implementation...")

#print(datamovlat)

list_labels = MyDBSCAN(datamovlat,datamovspd, eps=0.3, MinPts=5)









n_clusters_ = len(set(list_labels)) - (1 if -1 in list_labels else 0)
#print(type(db))

unique_labels = set(list_labels)

x = datamovlat[:, 0]
y = datamovlat[:, 1]

#for j in (range(len(unique_labels))):
   # print(j)


colors = [plt.cm.Spectral(each)

          for each in np.linspace(0, 1, len(unique_labels))]

        
for k, col in zip(unique_labels, colors):

    if k == -1:

        # Black used for noise.

        col = [0, 0, 0, 1]

    #plt.plot(datamovlat[:, 0], datamovlat[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=14)


#plt.title('Estimated number of clusters: %d' % n_clusters_)

#plt.show()
color_codes = [
   'darkmagenta'
   , 'yellow'
   ,'darkgreen'
   ,'black'
   ,'darkorange'
   ,'purple'
   ,'cornflowerblue'
   , 'orchid'
   ,'darkgray'
   ,'gold'
   ,'pink'
   ,'brown'
   ,'crimson'
   ,'coral'
   , 'navy'
   
   
]


gmap = gmplot.GoogleMapPlotter(57.423072, 8.690758,3 )
clustermat=[]
for i in range(1,max(list_labels)+1):
    clustermat.insert(i,[i])
for i in range(0,len(list_labels)):
    
    clustermat[list_labels[i]-1].append([datamovlatactual[i][0],datamovlatactual[i][1],datamovspd[i][0],datamovspd[i][1]])
colors=[]
import random
for i in range(0,max(list_labels)+1):
    r=lambda: random.randint(0,255)
    colors.append('#%02X%02X%02X'%(r(),r(),r()))
    
for i in range(0,len(list_labels)):
    if list_labels[i]!=-1:
        lats, lons = zip(datamovlatactual[i])
    
        gmap.scatter(lats, lons, colors[list_labels[i]], size=3000, marker=False)
gmap.draw("hack_dbscan_plot.html")  
gv=[]
for i in range(max(list_labels)):
    clustermat[i].pop(0)
gmapcl = gmplot.GoogleMapPlotter(-23.3011833333, 38.1240483333,8 ) 
   
cogw=[]
g=[]
for i in range(0,len(clustermat)):
    g.insert(i,[0])
for clustval in range(len(clustermat)):
    p=[]
    p=clustermat[clustval]
    pts=[]
    
    for i in p:
        pts.append((i[0],i[1]))
                   
        #gmapcl.scatter(lats, lons,'black', size=60, marker=False)
    distance = math.sqrt( ((pts[0][0]-pts[len(pts)-1][0])**2)+((pts[0][1]-pts[len(pts)-1][1])**2) )
    kpt=int(distance/2)
    kpt+=1
    
    kmeans = KMeans(n_clusters=kpt).fit(pts)
    clustar=kmeans.labels_
    clustercenter=kmeans.cluster_centers_
    sumcog=0.0
    sumsog=0.0
    for i in range(len(clustercenter)):
        mediancl=[]
        for j in range(len(p)):
            if clustar[j]==i:
                sumcog+=p[j][3]
                sumsog+=p[j][2]
                mediancl.append( math.sqrt( ((p[j][0]-clustercenter[i][0])**2)+((p[j][1]-clustercenter[i][1])**2) ))
    
        cnt=list(clustar).count(i)
        sumcog/=cnt
        sumsog/=cnt
        medianval=statistics.median(mediancl)
        if medianval==0:
            medianval=0.0000001
        g[clustval].append([clustercenter[i][0],clustercenter[i][1],sumsog,sumcog,medianval])
        
    lats, lons = zip(*clustercenter)
    
    gmapcl.scatter(lats, lons,color_codes[clustval%14], size=3500, marker=False)
for i in range(0,len(clustermat)):
    g[i].pop(0)

gmapcl.draw("hack_dbscan_plot_cluster.html")                  

gdf = pd.DataFrame(g)
gdf.to_csv('gravity_vectors.tsv',sep='\t', header=False, index=False)










