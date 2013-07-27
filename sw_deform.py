import mswine
import sw_curve
import time


def deform(xb, xnb, xpo, j,  k, b_func=mswine.get_constant_functions, F=mswine.F_w):
    xdb=[xnb[i][j]-xb[i][j] for i in range(len(xb))]
    fxi=b_func(xb,xdb_x,[])
    xo=[]
    for x in xpo:
        xo+=[x[j]+F(x, xb, [], fxi, k)]
    return xo


if __name__ == '__main__':
    ''' testing and demonstration part '''

    # data for 2d deformation
    xpo = [[100, 200], [300, 300], [200,100]]         # coordinates
    xb = [[100,100], [400,100], [400,400], [100,400]]
    xnb = [[50,50], [450,50], [450,450], [50,450]]


    def k(x):   # common weight function
        if x!=0:
            return 1/float(x)
        else:
            return 1.0e10  # to avoid zero division



    from Tkinter import *   # initializing graphics
    root = Tk()
    canvas1 = Canvas(root, height = 512, width = 512, background = "white")

    for i in range(len(xb)):
        canvas1.create_line(xb[i][0], xb[i][1], xnb[i][0], xnb[i][1], fill="#880000", arrow="last")

    draw_closed_curve(canvas1, [x[0] for x in xpo], [y[1] for y in xpo], px_per_segment=30, fill="#cccccc")
    xo=deform(xb, xnb, xpo, 0, k)
    yo=deform(xb, xnb, xpo, 1, k)
    draw_closed_curve(canvas1, xo, yo, px_per_segment=30)


    canvas1.pack({"side": "left"})
    root.mainloop()


