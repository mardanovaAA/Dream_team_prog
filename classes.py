

class Layer:
'''
Layer of Material

number - layer number
thickness - layer thickness
permittivity - dielectric constant
'''
    number = 0

    thickness = 0

    permittivity =

    def get_number():
        number = int(input())

    def get_thickness():
        thickness = float(input())

    def get_permittivity():
        real = float(input())
        imagine = float(input())
        permittivity = complex(real, imagine)


class LayerWidget:
'''
Layer image on the screen

x, y - coordinates of the upper left corner of the layer
name - layer name
comment - comment on the image

set_text - displays the layer name and its comment on the screen
'''

    x = 0

    y = 0

    rectangle = canvas.create_rectagle(x, y, x + 100, y+100)

    name = ''

    comment = ''

    def set_text(name, comment):
        canvas.create_text = (x, y, text = name + '\n' + comment + '\n')


    def move(event):
        x = event.x
        y = event.y
        s = "Движение мышью {}x{}".format(x, y)
        root.title(s)



class GraphWidget:
'''
Graphics on the screen
x, y - coordinates of the upper left end of the image
name - graphic name
comment - comment on the image

'''
     x = 0

     y = 0

     name = ''

     comment = ''

     def set_text(name, comment):
         canvas.create_text =()


