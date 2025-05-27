import numpy as np
from scipy.spatial import Delaunay
from collections import UserList
import random

class DPoint(UserList):
    def __init__(self,point=[], weight=0):
        super().__init__(point)
        self.weight=weight
    def x(self):
        return self[0]
    def y(self):
        return self[1]

raw_points=[DPoint(p,random.randint(0,100)) for p in [[0, 0], [1, 1], [1, 0], [0, 1]]]

points = np.array(raw_points)
tri = Delaunay(points)

def barycentric_weights(v,p):
    Wv1=((v[1].y()-v[2].y())*(p.x()-v[2].x()) +  \
        (v[2].x()-v[1].x())*(p.y()-v[2].y())) /  \
        ((v[1].y()-v[2].y())*(v[0].x()-v[2].x())+\
        (v[2].x()-v[1].x())*(v[0].y()-v[2].y()))

    Wv2=((v[2].y()-v[0].y())*(p.x()-v[2].x()) +   \
         (v[0].x()-v[2].x())*(p.y()-v[2].y())) /  \
         ((v[1].y()-v[2].y())*(v[0].x()-v[2].x())+\
          (v[2].x()-v[1].x())*(v[0].y()-v[2].y()))

    Wv3=1-Wv1-Wv2

    return (Wv1,Wv2,Wv3)

# Check if point is inside
yp =[
    DPoint([0,0]),
    DPoint([0.25,0.5]),
    DPoint([6,6]),
    DPoint([0.75,0.75])
]

idx=0
for i in tri.find_simplex(yp):
    # print(tri.simplices[i]) # raw point indexes
    dpoints=[raw_points[i] for i in tri.simplices[i]]
    print(str(dpoints),yp[idx],barycentric_weights(dpoints, yp[idx]))
    idx=idx+1
