from spectrum_class import *
from matplotlib.widgets import Button
from matplotlib.widgets import CheckButtons
import matplotlib.pyplot as plt

class plotSpec :
    def __init__(self, plotter) :
        self.spec = []
        self.boxes = []
        self.plt = plotter
        self.ax = self.plt.subplot(111)
        self.rax = self.plt.axes([0.01, 0.2, 0.1, 0.15])
        self.check = None
        self.checkLabel = []
        self.checkChecked = []
        self.ax.xaxis.get_major_formatter().set_powerlimits((-3, 6))
        self.ax.xaxis.get_major_formatter().set_scientific(False)

    def addSpec(self, spec) :
        self.spec.append(spec)
        self.checkLabel.append(spec.name)
        self.checkChecked.append(True)
        box,  = self.ax.plot(spec.freq,  spec.data,  visible = True)
        self.boxes.append(box)

    def display(self, label) :
        for i in range(0, len(self.spec)) :
            if(label == self.spec[i].name) :
                self.boxes[i].set_visible(not self.boxes[i].get_visible())
                self.plt.draw()
                return

    def show(self, index) :
        self.check = CheckButtons(self.rax, self.checkLabel, self.checkChecked)
        self.check.on_clicked(self.display)
        plt.figure(index)
        plt.gcf().canvas.set_window_title('Test')
        plt.figure(index).show()



