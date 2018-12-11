# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 19:44:37 2017

@author: Xianan
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 16:14:28 2017

@author: Xianan
"""

from numpy import array,random,exp,empty,mean
from pylab import title,xlabel,ylabel,plot
import math
import tkinter
try:
    import Image, ImageTk
except:
    try:
        from PIL import Image, ImageTk
    except:
        raise Error("PIL not installed")
    
from scipy import minimum,maximum
DefaultImageSize = (400,400)

root = tkinter.Tk()
root.withdraw()

class DynamicLattice (tkinter.Label):

    def __init__(self, shape, size=DefaultImageSize, mode='P', 
                 zmin=0.0, zmax=1.0):
        top = tkinter.Toplevel()
        top.title('DynamicLattice')
        tkinter.Label.__init__(self, top)
        self.shape = shape
        self.size = size
        self.mode = mode
        self.zmin = zmin
        self.zmax = zmax
        self.zrange = zmax-zmin
        self.canvas = tkinter.Canvas(top, 
				     width=self.size[0], height=self.size[1])
        tkinter.Widget.bind(self.canvas, "<Button-1>",
                           self.mouseDown)
        tkinter.Widget.bind(self.canvas, "<Button1-ButtonRelease>",
                           self.mouseUp)
        self.mousecoords = []
        self.im = Image.new(self.mode, self.shape)
        self.displayIm = self.im.resize(self.size)
        #self.displayIm = self.im
        if self.mode == '1':
            self.tkimage = \
                ImageTk.BitmapImage(self.displayIm,
                            foreground="white")
        else:
            self.tkimage = \
                ImageTk.PhotoImage(self.displayIm)
        self.canvas.create_image(0, 0, anchor=tkinter.NW, image=self.tkimage)
        self.canvas.pack()

    def setTitle(self, title):
        self.master.title(title)

    def mouseDown(self, event):
        x0 = self.canvas.canvasx(event.x)
        y0 = self.canvas.canvasx(event.y)
        sx0 = int(self.shape[0] * float(x0)/self.size[0])
        sy0 = int(self.shape[1] * float(y0)/self.size[1])
        self.mousecoords = [sx0, sy0]

    def mouseUp(self, event):
        sx0, sy0 = self.mousecoords
        x1 = self.canvas.canvasx(event.x)
        y1 = self.canvas.canvasx(event.y)
        sx1 = int(self.shape[0] * float(x1)/self.size[0])
        sy1 = int(self.shape[1] * float(y1)/self.size[1])
        X0, X1 = min(sx0, sx1), max(sx0, sx1)
        Y0, Y1 = min(sy0, sy1), max(sy0, sy1)
        self.mousecoords = [X0, Y0, X1, Y1]
    
    def IsBoxSelected(self):
        return len(self.mousecoords)==4

    def GetMouseBox(self):
        mc = self.mousecoords[:]
        self.mousecoords = []
        return mc
		
    def olddisplay(self, array, site=None):
        if site is not None:
            self.im.putpixel(site, self.grayscale(array[site]))
        else:
            for i in range(array.shape[0]):
                for j in range(array.shape[1]):
                    self.im.putpixel((i,j), self.grayscale(array[i,j]))
        self.displayIm = self.im.resize(self.size)
        self.tkimage.paste(self.displayIm)
        self.canvas.update()
		
    def fastdisplay(self, array):
        scaleddata=self.simpgrayscale(array.flatten())
        self.im.putdata(scaleddata)
        self.displayIm = self.im.resize(self.size)
        self.tkimage.paste(self.displayIm)
        self.canvas.update()
        
    def display(self, array, site=None):
        if site is not None:
            self.im.putpixel(site, self.grayscale(array[site]))
        else:
            scaleddata=self.simpgrayscale(array.transpose().flatten())
            self.im.putdata(scaleddata)
        self.displayIm = self.im.resize(self.size)
        self.tkimage.paste(self.displayIm)
        self.canvas.update()

    def simpgrayscale(self, value):
        sval = (value-self.zmin)/(self.zrange)
        sval=minimum(sval,1)
        sval=maximum(sval,0)
        sval=255.*(sval)
        return sval.astype(int)

    def grayscale(self, value):
        sval = (value-self.zmin)/(self.zrange)
        if sval < 0.: sval = 0.
        if sval > 1.: sval = 1.
        return int(255.*(sval))

    def set_zmin(self, zmin):
        self.zmin = zmin
        self.zrange = self.zmax - self.zmin
        
    def set_zmax(self, zmax):
        self.zmax = zmax
        self.zrange = self.zmax - self.zmin
        
N = 20
def findneighbor(latt,x,y):
    #Here defined the up, down, left, right neighbors are stored in below 
    #array, neighbor, from [0,0],[0,1],[1,0],[1,1]
    neighbor = empty([2,2],float)
    if (y==0):
        neighbor[1,0] = latt[x,N-1]
    else:
        neighbor[1,0] = latt[x,y-1]    
    if (y==(N-1)):
        neighbor[1,1] = latt[x,0]
    else:
        neighbor[1,1] = latt[x,y+1]
    if (x==0):
        neighbor[0,0] = latt[N-1,y]
    else:
        neighbor[0,0] = latt[x-1,y]
    if (x==(N-1)):
        neighbor[0,1] = latt[0,y]
    else:
        neighbor[0,1] = latt[x+1,y]
    return neighbor
def EnergyCalculator(latt,m,n):
    return sum(sum(-latt[m,n]*findneighbor(latt,m,n)))


#Initiate the lattice
dynlat = DynamicLattice((N, N))
latt = empty([N,N])
for m in range(N):
    for n in range(N):
        rd = random.random()
        if (rd<0.5):
            latt[m,n] = 1
        else:
            latt[m,n] = -1
dynlat.display(latt)
#Number of MC steps
Ns = 1000000
Spin = []
for k in range(Ns):
    rdx = int(N*random.random())
    rdy = int(N*random.random())
    deltaE = -2*EnergyCalculator(latt,rdx,rdy)
    p = exp(-deltaE/3)
    if(random.random()<p):
        latt[rdx,rdy] = -latt[rdx,rdy]
        #print(p)
    dynlat.display(latt)    

