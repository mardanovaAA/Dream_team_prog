import tkinter as tk
import Layer

class LW():
    """
Layer image on the screen

set_text - displays the layer name and its comment on the screen
"""
    def __init__(self, canvas, layer, x, y, width = 80, length = 100):
        """
        Parameters
        ----------
        canvas: tk.canvas - the canvas for image of layer
        layer: class Layer.L() - the layer;
        x, y: int - coordinates of the upper left corner of the layer;
        width: int - the width of the layer image (The default is 100);
        length: int - the length of the  layer image (The default is 100);
        rectangle: canvas.rectangle - the widget of the layer;
        name: str - layer name
        comment - comment on the image 
        activation - is 1 if the layer is choosen, else is 0 
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
        self.actovation = ''
    
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
        
    def activate(self):
        '''
        Change the flag activation to 1, if the button is clicked
        '''
        self.activation = 1
    
    def button(self):
        """
        creates a button.
        """
        self.button = tk.Button(self.canvas, text = '')
        self.button['text'] = 'Choose'
        self.button['activebackground'] = 'bisque3'
        self.button['activeforeground'] = 'bisque3'
        self.button['bg'] = 'bisque2'
        self.button['command'] = self.activate
        self.button.place(x = self.x - int(0.8 * self. length), y = self.y + int(0.25 * self.width), 
                          width = 5 * self.length // 9, height = self.width // 2)
        
    
    def move(event):
        x = event.x
        y = event.y
        s = "Движение мышью {}x{}".format(x, y)
        root.title(s)


