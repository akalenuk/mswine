import mswine
import math
import time
import obj_io

#!/usr/bin/python2.5
#
# Copyright 2010 Alexandr Kalenuk.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


""" building surface using mswine.py.

Including triangulation of a spatial data set

"""

__authors__ = [
  '"Alexandr Kalenuk" <akalenuk@gmail.com>'
]

EPS = 1.0e-5


def d(a, b,  xs):
    return math.sqrt( math.pow(xs[a][0]-xs[b][0], 2) + math.pow(xs[a][1]-xs[b][1], 2) )


def sq(x1, y1, x2, y2, x3, y3):
    return abs(mswine.v_cross([ [x2-x1, x3-x1, 0], [y2-y1, y3-y1, 0] ])[2])


def in_tri(x, y, i,  tris, xs):
    x1=xs[tris[i][0]][0]
    y1=xs[tris[i][0]][1]
    x2=xs[tris[i][1]][0]
    y2=xs[tris[i][1]][1]
    x3=xs[tris[i][2]][0]
    y3=xs[tris[i][2]][1]
    if x<min(x1,x2,x3):
        return False
    if x>max(x1,x2,x3):
        return False
    if y<min(y1,y2,y3):
        return False
    if y>max(y1,y2,y3):
        return False
    S=sq(x1,y1, x2,y2, x3,y3);
    s1=sq(x,y, x2,y2, x3,y3);
    s2=sq(x1,y1, x,y, x3,y3);
    s3=sq(x1,y1, x2,y2, x,y);
    if abs(S-s1-s2-s3)<EPS:
        return True
    return False


def crosses(i1,i2, j1,j2,  xs):
    ta=(xs[i2][0]-xs[i1][0])*(xs[j1][1]-xs[j2][1]) - (xs[j1][0]-xs[j2][0])*(xs[i2][1]-xs[i1][1])
    tb=(xs[j1][0]-xs[j2][0])*(xs[i2][1]-xs[i1][1]) - (xs[i2][0]-xs[i1][0])*(xs[j1][1]-xs[j2][1])
    if ta==0 or tb==0:
        return False
    a=( (xs[j1][1]-xs[j2][1])*(xs[j1][0]-xs[i1][0]) - (xs[j1][0]-xs[j2][0])*(xs[j1][1]-xs[i1][1]) ) / ta
    b=( (xs[i2][1]-xs[i1][1])*(xs[j1][0]-xs[i1][0]) - (xs[i2][0]-xs[i1][0])*(xs[j1][1]-xs[i1][1]) ) / tb
    if 1>a>0 and 1>b>0:
        return True;
    return False;


def forma(i1, i2, i3,  xs):
    the_forma = abs( min(d(i1,i2, xs), d(i2,i3, xs)) / max(d(i1,i2, xs), d(i2,i3, xs)) )
    the_forma+= abs( min(d(i2,i3, xs), d(i3,i1, xs)) / max(d(i2,i3, xs), d(i3,i1, xs)) )
    the_forma+= abs( min(d(i3,i1, xs), d(i1,i2, xs)) / max(d(i3,i1, xs), d(i1,i2, xs)) )
    return the_forma


def triangulate(xs):
    tris=[[0,0,0]]
    icnt=0
    found=1
    xcnt=len(xs)

    while found>0:
        found=0
        for m in range(30,-1,-1):
            for i in range(xcnt-2):
                for j in range(i+1, xcnt-1) :
                    for k in range(j+1, xcnt):
                        tris[icnt][0]=i
                        tris[icnt][1]=j
                        tris[icnt][2]=k

                        is_simple=True
                        for l in range(0, xcnt):
                            if l!=i and l!=j and l!=k:
                                if in_tri(xs[l][0], xs[l][1], icnt,  tris, xs):
                                    is_simple=False

                        in_list=False
                        for l in range(icnt):
                            if tris[l][0]==i and tris[l][1]==j and tris[l][2]==k:
                                in_list=True

                        it_crosses=False
                        for l in range(icnt):
                            if(crosses(tris[l][0], tris[l][1],   tris[icnt][0], tris[icnt][1],  xs)): it_crosses=True
                            if(crosses(tris[l][1], tris[l][2],   tris[icnt][0], tris[icnt][1],  xs)): it_crosses=True
                            if(crosses(tris[l][2], tris[l][0],   tris[icnt][0], tris[icnt][1],  xs)): it_crosses=True

                            if(crosses(tris[l][0], tris[l][1],   tris[icnt][1], tris[icnt][2],  xs)): it_crosses=True
                            if(crosses(tris[l][1], tris[l][2],   tris[icnt][1], tris[icnt][2],  xs)): it_crosses=True
                            if(crosses(tris[l][2], tris[l][0],   tris[icnt][1], tris[icnt][2],  xs)): it_crosses=True

                            if(crosses(tris[l][0], tris[l][1],   tris[icnt][2], tris[icnt][0],  xs)): it_crosses=True
                            if(crosses(tris[l][1], tris[l][2],   tris[icnt][2], tris[icnt][0],  xs)): it_crosses=True
                            if(crosses(tris[l][2], tris[l][0],   tris[icnt][2], tris[icnt][0],  xs)): it_crosses=True

                        if not in_list and is_simple and not it_crosses:
                            if forma(tris[icnt][0], tris[icnt][1], tris[icnt][2],  xs)>=0.1*m:
                                icnt+=1
                                tris+=[[0,0,0]]
                                found+=1
    
    return tris[:-1]


if __name__ == '__main__':
    ''' testing and demonstration part '''
        
    # data for the surface
    xs = [[50.0, 302.0], [102.0, 454.0], [252.0,456.0], [208.0,358.0], [386.0,280.0], [452.0, 452.0]]         # coordinates
    ys = [50.0, 75.0, 65.0, 105.0, 35.0, 50.0]

    # data for deformation
    obasis = [[170, 300, 50], [370, 320, 50], [250, 450, 50]]
    nbasis = [[130, 270, 170], [400, 280, 180], [280, 490, 320]]

    from Tkinter import *   # initializing graphics
    root = Tk()
    canvas1 = Canvas(root, height = 512, width = 512, background = "white")

    # draw surface data set
    for i in range(len(xs)):
        x=xs[i]
        y=ys[i]
        canvas1.create_line(x[0]-5, x[1]+5, x[0], x[1], fill="#ee3333", arrow="last")
        canvas1.create_line(x[0]+5, x[1]-5, x[0], x[1], fill="#ee3333", arrow="last")
        canvas1.create_line(x[0]+5, x[1]+5, x[0], x[1], fill="#ee3333", arrow="last")
        canvas1.create_line(x[0]-5, x[1]-5, x[0], x[1], fill="#ee3333", arrow="last")
        canvas1.create_line(x[0], x[1], x[0], x[1]-y, fill="#3333ee")
    
    # triangulation
    tris=triangulate(xs)

    # draw simplicial complex
    for tri in tris:
        canvas1.create_line(xs[tri[0]][0], xs[tri[0]][1],  xs[tri[1]][0], xs[tri[1]][1], fill="#333333")
        canvas1.create_line(xs[tri[1]][0], xs[tri[1]][1],  xs[tri[2]][0], xs[tri[2]][1], fill="#333333")
        canvas1.create_line(xs[tri[2]][0], xs[tri[2]][1],  xs[tri[0]][0], xs[tri[0]][1], fill="#333333")

    # reformate to mswine simplices
    old_tris = [[n for n in tri] for tri in tris]
    for tri in tris:
        tri[0]+=1
        tri[1]+=1
        tri[2]+=1
   
    # draw deformation basis
    for i in range(len(obasis)):
        canvas1.create_line(obasis[i][0], obasis[i][1],  obasis[i][0], obasis[i][1]-obasis[i][2], fill="#FFAAAA")
        canvas1.create_line(nbasis[i][0], nbasis[i][1],  nbasis[i][0], nbasis[i][1]-nbasis[i][2], fill="#FFAAAA")
        canvas1.create_line(obasis[i][0], obasis[i][1]-obasis[i][2],  nbasis[i][0], nbasis[i][1]-nbasis[i][2], fill="#AA2222", arrow="last", width=2)

    # basis functions
    # for surface
    fs = mswine.get_linear_functions(xs, ys, tris)

    # for deformation
    fdx = mswine.get_constant_functions(obasis, [nbasis[i][0]-obasis[i][0] for i in range(len(obasis))], [])
    fdy = mswine.get_constant_functions(obasis, [nbasis[i][1]-obasis[i][1] for i in range(len(obasis))], [])
    fdz = mswine.get_constant_functions(obasis, [nbasis[i][2]-obasis[i][2] for i in range(len(obasis))], [])


    # quasi-isometric plot
    colors=["#880000","#008800","#000088","#888800","#008888","#880088"];

    def sk(x):   # common weight function
        if x>EPS:
            return 1/float(x*x)
        else:
            return 1/EPS  # to avoid zero division


    h1 = 257
    h2 = 481

    sq_mesh=[]
    

    for i in range(h1, h2+1,2):
        print '|',
        w1 = 1+(i/20)*2
        w2 = 440+(i/20)*2-1
        sq_mesh_line = []
        
        for j in range(w1, w2+1,2):

            dy = mswine.F_s([j, i], xs, tris, fs, sk)

            # deformation
            ox = [j, i, dy]
            ndx = mswine.F_w(ox, obasis, [], fdx, sk)
            ndy = mswine.F_w(ox, obasis, [], fdy, sk)
            ndz = mswine.F_w(ox, obasis, [], fdz, sk)
            nx = [j+ndx, i+ndy, dy+ndz]

            # export
            sq_mesh_line += [nx]
                            

            if dy!=None:
                canvas1.create_line(j, i-dy+1, j, i-dy, fill="#999999") # surface
                canvas1.create_line(nx[0], nx[1]-nx[2]+1, nx[0], nx[1]-nx[2], fill="#999999") # new surface
                for k in range(len(old_tris)):
                    if in_tri(float(j), float(i), k,  old_tris, xs):
                        canvas1.create_line(j, i-dy+1, j, i-dy, fill=colors[k])
                        canvas1.create_line(nx[0], nx[1]-nx[2]+1, nx[0], nx[1]-nx[2],  fill=colors[k])
                        break
    
        sq_mesh += [sq_mesh_line]

    obj_io.square_mesh_to_obj(sq_mesh, 'surface.obj')
    
    canvas1.pack({"side": "left"})
    root.mainloop()


