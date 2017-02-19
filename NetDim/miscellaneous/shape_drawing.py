# NetDim
# Copyright (C) 2016 Antoine Fourmy (antoine.fourmy@gmail.com)
# Released under the GNU General Public License GPLv3

from pythonic_tkinter.preconfigured_widgets import *

class Shape():
    
    class_type = 'shape'
    color = 'black'
    
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Label(Shape):
    
    subtype = 'label'
    
    def __init__(self, *args):
        self.text = args[-1]
        super().__init__(*args[:-1])        
        
    def __repr(self):
        return self.text
        
class Rectangle(Shape):
    
    subtype = 'rectangle'
    
    def __init__(self, *args):
        super().__init__(*args)        
        
    def __repr(self):
        return '{} {}'.format(self.subtype, self.id)
        
class Oval(Shape):
    
    subtype = 'oval'
    
    def __init__(self, *args):
        super().__init__(*args)        
        
    def __repr(self):
        return '{} {}'.format(self.subtype, self.id)

class LabelCreation(CustomTopLevel):
            
    def __init__(self, scenario, x, y):
        super().__init__()
        self.cs = scenario
        
        # labelframe
        lf_label_creation = Labelframe(self)
        lf_label_creation.text = 'Create a label'
        lf_label_creation.grid(0, 0)

        self.entry_label = Entry(self, width=20)
        
        OK_button = Button(self, width=20)
        OK_button.text = 'OK'
        OK_button.command = lambda: self.OK(x, y)
        
        lf_label_creation.grid(0, 0)
        self.entry_label.grid(0, 0, in_=lf_label_creation)
        OK_button.grid(1, 0, in_=lf_label_creation)

    def OK(self, x, y):
        label = Label(
                      self.cs.cvs.create_text(
                                            x, 
                                            y, 
                                            text = self.entry_label.text,
                                            font = ("Purisa", '12', 'bold'), 
                                            tag = ('shape',)
                                            ),
                      x, 
                      y,
                      self.entry_label.text
                      )
        self.cs.object_id_to_object[label.id] = label
        self.destroy()