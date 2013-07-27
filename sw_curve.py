import mswine
import time

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


""" drawing curves using mswine.py.

This are the routines to draw curves using mswine and Tkinter.

"""

__authors__ = [
  '"Alexandr Kalenuk" <akalenuk@gmail.com>'
]

def draw_curve(the_canvas, the_x, the_y, fill="black", px_per_segment=100, width=1):
    ''' Draws closed curve based on simplicial weight interpolation
        with linear basis functions and hyperbolic weights 

        Args:
            the_canvas: Canvas to write on.
            the_x, the_y: Lists of coordinates.
            fill: Color of the curve.
            px_per_segment: Number of points calculated with mswine per segment.
            width: Witdh of the curve. 

        Returns:
            Nothing
    ''' 
    def k(x):   # curve weight function
        if x!=0:
            return 1/float(x)
        else:
            return 1.0e10  # to avoid zero division

    if len(the_x)<3 or len(the_x)!=len(the_y):
        return
    
    x = the_x
    y = the_y
    t = [[i+1] for i in range(len(x))]
    s1 = [[i,i+1] for i in range(1,len(x))]
    fxi = mswine.get_linear_functions(t, x, s1)    # basis functions
    fyi = mswine.get_linear_functions(t, y, s1)    # basis functions
    ox='none'
    oy='none'
    for i in xrange(len(s1)):    # for all simplexes
        for j in xrange(px_per_segment+1):
            ti1 = t[s1[i][0]-1][0]
            ti2 = t[s1[i][1]-1][0]
            ti = ti1 + j*float(ti2 - ti1)/px_per_segment
            F_x=mswine.F_s([ti], t, s1, fxi, k)
            F_y=mswine.F_s([ti], t, s1, fyi, k)
            if ox!='none' and oy!='none':
                the_canvas.create_line(F_x, F_y, ox, oy, fill=fill, width=width)
            ox = F_x
            oy = F_y

                
def draw_closed_curve(the_canvas, the_x, the_y, fill="black", px_per_segment=100, width=1):
    ''' Draws closed curve based on simplicial weight interpolation
        with linear basis functions and hyperbolic weights 

        Args:
            the_canvas: Canvas to write on.
            the_x, the_y: Lists of coordinates.
            fill: Color of the curve.
            px_per_segment: Number of points calculated with mswine per segment.
            width: Witdh of the curve. 

        Returns:
            Nothing
    ''' 
    def k(x):   # curve weight function
        if x!=0:
            return 1/float(x)
        else:
            return 1.0e10  # to avoid zero division

    if len(the_x)<3 or len(the_x)!=len(the_y):
        return
    
    x = the_x+[the_x[i] for i in range(3)]
    y = the_y+[the_y[i] for i in range(3)]
    t = [[i+1] for i in range(len(x))]
    s1 = [[i,i+1] for i in range(1,len(x))]
    fxi = mswine.get_linear_functions(t, x, s1)    # basis functions
    fyi = mswine.get_linear_functions(t, y, s1)    # basis functions
    ox='none'
    oy='none'
    for i in xrange(len(s1)):    # for all simplexes
        if i>0 and i<len(s1)-1: # these simplexes are to grant smoothness only
            for j in xrange(px_per_segment+1):
                ti1 = t[s1[i][0]-1][0]
                ti2 = t[s1[i][1]-1][0]
                ti = ti1 + j*float(ti2 - ti1)/px_per_segment
                F_x=mswine.F_s([ti], t, s1, fxi, k)
                F_y=mswine.F_s([ti], t, s1, fyi, k)
                if ox!='none' and oy!='none':
                    the_canvas.create_line(F_x, F_y, ox, oy, fill=fill, width=width)
                ox = F_x
                oy = F_y



if __name__ == '__main__':
    ''' testing and demonstration part '''
        
    # data for line drawing
    xs = [[100, 200], [400, 100], [400,400], [100,400], [200,100]]         # coordinates


    def k(x):   # common weight function
        if x!=0:
            return 1/float(x)
        else:
            return 1.0e10  # to avoid zero division



    from Tkinter import *   # initializing graphics
    root = Tk()
    canvas1 = Canvas(root, height = 512, width = 512, background = "white")

    draw_closed_curve(canvas1, [x[0] for x in xs], [y[1] for y in xs], px_per_segment=30, fill="#222288")
    draw_curve(canvas1, [x[0] for x in xs], [y[1] for y in xs], px_per_segment=30, fill="#228822")
    for x in xs:
        canvas1.create_line(x[0]-5, x[1]+5, x[0], x[1], fill="#ee3333", arrow="last")
        canvas1.create_line(x[0]+5, x[1]-5, x[0], x[1], fill="#ee3333", arrow="last")
        
    canvas1.pack({"side": "left"})
    root.mainloop()


