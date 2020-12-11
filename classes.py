import tkinter as tk


class Layer():
    """
    Layer of a material.
    """
    def __init__(self, number, name, refractive_index, thickness):
        """

        @param int number: number of the layer
        @param str name: name of the layer
        @param complex refractive_index: refractive index of the layer material
        @param float thickness: thickness of the layer
        """
        self.number = number
        self.name = name
        self.refractive_index = refractive_index
        self.thickness = thickness


class LayerWidget():
    """
    Layer image on the screen.
    """
    def __init__(self, canvas, layer, x, y, width=80, length=100):
        """

        @param tk.canvas canvas: the canvas for image of the layer
        @param class Layer() layer: the layer
        @param int x, int y: coordinates of the upper left corner of the layer
        @param int width: width of the layer image (The default is 80 pixels)
        @param int length: the length of the layer image (The default is 100 pixels)
        @param tk.canvas.rectangle rectangle: the widget of the layer
        @param name: str - layer name
        """
        self.canvas = canvas
        self.layer = layer
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.rectangle = self.canvas.create_rectangle(x, y, x + length, y + width, fill='peach puff', width=2)

    def set_text(self, name=None, comment=[]):
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
                                                  text=self.name + '\n' + self.comment + '\n', font='20')
        self.canvas.itemconfig(self.text_layer)

    def buttons(self):
        """
        creates a button.
        """
        self.button = tk.Button(self.canvas, text='')
        self.button['text'] = 'Choose'
        self.button['activebackground'] = 'bisque3'
        self.button['activeforeground'] = 'bisque3'
        self.button['bg'] = 'bisque2'
        self.button.place(x=self.x - int(1.3 * self.length), y=self.y + int(0.25 * self.width),
                          width=self.length, height=self.width // 2)

    def move(event):
        x = event.x
        y = event.y
        s = "Движение мышью {}x{}".format(x, y)
        tk.root.title(s)


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
