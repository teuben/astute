#!/usr/bin/env python
import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from pylab import *

class plotter:

    def __init__(self):
        
      
        builder = gtk.Builder()
        builder.add_from_file("AstuteGui.glade")
       
        self.window = builder.get_object("Astute")
        builder.connect_signals(self)
     
        self.canvas = FigureCanvasGTK(self.figure)
        self.canvas.show()
    
    def on_destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        self.window.show()
        gtk.main()
        
app = plotter()
gtk.main()
app.window.show()
    
