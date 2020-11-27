import tkinter as tk

class Layer():
    """
Layer of Material

number - layer number
thickness - layer thickness
permittivity - dielectric constant
"""
    def __init__(self):    
        self.number = 0
        thickness = 0
        permittivity = 0

    def get_number():
        number = int(input())

    def get_thickness():
        thickness = float(input())

    def get_permittivity():
        real = float(input())
        imagine = float(input())
        permittivity = complex(real, imagine)


class LayerWidget():
    """
Layer image on the screen

set_text - displays the layer name and its comment on the screen
"""
    def __init__(self, canvas, layer, x, y, width = 80, length = 100):
        """
        Parameters
        ----------
        canvas: tk.canvas - the canvas for image of layer
        layer: class Layer() - the layer;
        x, y: int - coordinates of the upper left corner of the layer;
        width: int - the width of the layer image (The default is 100);
        length: int - the length of the  layer image (The default is 100);
        rectangle: canvas.rectangle - the widget of the layer;
        name: str - layer name
        self.comment - comment on the image 
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.layer = layer
        self.width = width
        self.length = length
        self.rectangle = self.canvas.create_rectangle(x, y, x + length, y + width, fill = 'peach puff', width = 2)
        self.name = ''
        self.comment = ''
    
    def set_text(self, name = None, comment = []):
        """
        Creates text on layer image;
        
        Parameters
        ----------
        name: str - the name of layer (the default is None);
        comment: - the comment for the layer (the default is []);
        """
        if name == None:
            self.name = 'Layer №' + str(self.layer.number)
        else:
            self.name = name
        self.comment = comment    
        self.text_layer = self.canvas.create_text(self.x + self.length // 2, self.y + self.width // 2, 
                                                  text = self.name + '\n' + self.comment + '\n', font = '20')
        self.canvas.itemconfig(self.text_layer)
        
    def buttons(self):
        """
        creates a button.
        """
        self.button = tk.Button(self.canvas, text = '')
        self.button['text'] = 'Choose'
        self.button['activebackground'] = 'bisque3'
        self.button['activeforeground'] = 'bisque3'
        self.button['bg'] = 'bisque2'
        self.button.place(x = self.x - int(1.3 * self. length), y = self.y + int(0.25 * self.width), 
                          width = self.length, height = self.width // 2)
        
    
    def move(event):
        x = event.x
        y = event.y
        s = "Движение мышью {}x{}".format(x, y)
        root.title(s)



class GraphWidget:
    """
Graphics on the screen
x, y - coordinates of the upper left end of the image
name - graphic name
comment - comment on the image
"""

    x = 0

    y = 0

    name = ''

    comment = ''

    """def set_text(name, comment):
        canvas.create_text =()"""


