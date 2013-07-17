import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import VOTable as vt
import plot


index = 1

reader = None

class SpecButton :
    def __init__(self, indx,  spec):
        self.index = indx
        self.spec = spec
        self.active = False
        self.ps = None

    def plot(self, event) :
        if(self.active) :
            return
        plt.figure(self.index)
        plt.figure(self.index).canvas.mpl_connect('close_event', self.on_close)
        self.ps = plot.plotSpec(plt)
        for s in self.spec :
            self.ps.addSpec(s)
        self.active = True
        self.ps.show(self.index)

    def on_close(self, event) :
        global index
        self.active = False
        self.index = index
        index += 1
        self.ps = None


class ImageButton :
    def __init__(self,  indx) :
        pass


def assignButtons(reader) :
    global index
    plt.figure(0)
    specs = reader.getSpec()
    images = reader.getImages()

    print len(specs)
    print len(images)

    for spec in specs :
        #plotter.figure(index)
        ax = plt.axes([0.1, 0.05 + index * 0.1, 0.4, 0.075])
        bnext = Button(ax, "Spec1")
        sb = SpecButton(index, spec)
        bnext.on_clicked(sb.plot)
        index += 1
    plt.show()

def runit(xfile="new_spec.xml") :
    global reader
    reader = vt.VOTable()
    reader.read(xfile)
    assignButtons(reader)
