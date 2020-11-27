from tkinter import *

class Layer():
    '''
    Layer of Material

    number - layer number
    thickness - layer thickness
    permittivity - dielectric constant
    '''

    def __init__(self):
        self.number = 0
        self.thickness = 0
        self.permittivity = 0

    def get_number(self):
        return self.number

    def get_thickness(self):
        return self.thickness

    def get_permittivity(self):
        return self.permittivity

    def set_number(self, number):
        self.number = number

    def set_thickness(self, thickness):
        self.thickness = thickness

    def set_permittivity(self, permittivity):
        self.permittivity = permittivity


class LayerWidget(Layer):
    '''
    Layer image on the screen

    x, y - coordinates of the upper left corner of the layer
    name - layer name
    comment - comment on the image

    set_text - displays the layer name and its comment on the screen
    '''
    def __init__(self):
        self.x = 0
        self.y = 0
        self.name = ''
        self.comment = ''

    def set_text(self, name, comment):
        self.name = name
        self.comment = comment

    def rectangle(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.x + 200, self.y + 100, fill ='red', outline = 'black', width =1 )
        Text = Label(text = '#1 '+'/n'+ self.name + '/n' + self.comment, font = 14)
        Text.place(self.x, self.y)


class GraphWidget():
    '''
    Graphics on the screen
    x, y - coordinates of the upper left end of the image
    name - graphic name
    comment - comment on the image

    '''


    def __init__(self):
        self.x = 0
        self.y = 0
        self.name = ''
        self.comment = ''

    def set_text(self, name, comment):
        self.name = name
        self.comment = comment

class Mainmenu(Menu):

    def __init__(self, root):
        root.config(menu = self)
        filemenu = Menu(self, tearoff = 0)
        filemenu.add_command(label = 'Открыть...')
        filemenu.add_command(label = 'Сохранить файл как...')
        self.add_cascade(label= 'Файл', menu = filemenu)
        self.add_command(label = 'Справка')

