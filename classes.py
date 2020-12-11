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
        self.thickness = 0
        self.refractive_index = 0
        self.name = ''

    def get_number(self):
        return self.number

    def get_thickness(self):
        return self.thickness

    def get_permittivity(self):
        return self.refractive_index

    def set_number(self, number):
        self.number = number

    def set_thickness(self, thickness):
        self.thickness = thickness

    def set_permittivity(self, permittivity):
        self.permittivity = permittivity



class LayerWidget():
    """
Layer image on the screen

"""
    def __init__(self, screen, layers):
        """
        Parameters
        ----------
        screen: tk.root or tk.frame - the place, where will be Layers
        layers: list of class Layer() - the layer;
        """
        
        self.frame_pic = tk.Frame(screen)
        self.canv = tk.Canvas(self.frame_pic)
        self.menu_layers = tk.Frame(screen)
        self.layers = layers
        
    #def delete_lay(self, lay):
        
    """    
    def creat_menu(self, lay):
        tname = tk.StringVar()
        tthickness = tk.StringVar()
        tpermittivity = tk.StringVar()
        
        lnubmber = tk.Label(self.menu_layers, text = 'Поменяйте слой №' + str(lay.number))
        lnubmber.pack()
        
        lname = tk.Label(self.menu_layers, text = 'Имя слоя')
        lname.pack()
        ename = tk.Entry(self.menu_layers, width = 25, textvariable = tname)
        ename.pack()
        
        lpermittivity = tk.Label(self.menu_layers, text = 'Проницаемость')
        lpermittivity.pack()
        epermittivity = tk.Entry(self.menu_layers, width = 25, textvariable = tpermittivity)
        epermittivity.pack()
        
        lthickness = tk.Label(self.menu_layers, text='Толщина')
        lthickness.pack()
        ethickness = tk.Entry(self.menu_layers, width = 25, textvariable = tthickness)
        ethickness.pack()
        
        Будущие кнопочки, сейчас доработаю
        add = tk.Button(self.menu_layers, text='Внести изменения', command = self.change_lay(lay, tname, tthickness, tpermittivity))
        add.pack()
        
        up = tk.Button(self.menu_layers, text='Поднять слой', command = self.move_up(lay))
        up.pack()
        
        down = tk.Button(self.menu_layers, text='Опустить слой', command = self.move_down(lay))
        down.pack()
        
        dele = tk.Button(self.menu_layers, text='Удалить слой', command = self.delete_lay(lay))
        dele.pack()
          """  
        
    def create_button(self, lay, fr):
        """
        Creates button of Layer
        Parameters
        ----------
        lay : class Layer() - the certain layer
        fr: frame, where wil be layers
        
        Return button of layer
        """
        text_but = '#' + str(lay.number) + '. ' + lay.name + '\n'
        text_but += 'refractive_index: ' + str(lay.refractive_index) + '\n'
        text_but += 'Thickness: ' + str(lay.thickness)
        but = tk.Button(fr, text = text_but, width = 30, height = 4)
        but['activebackground'] = 'CadetBlue2'
        but['activeforeground'] = 'white'
        but['bg'] = 'CadetBlue1'
        return but
        
    def list_layers(self):
        """
        Creates picture of layers on the screen
        """
        scroll_y = tk.Scrollbar(self.frame_pic, orient = tk.VERTICAL, command = self.canv.yview)
        scrollable_frame = tk.Frame(self.canv)
        scrollable_frame.bind("<Configure>", lambda e: self.canv.configure(scrollregion = self.canv.bbox("all")))
        self.canv.create_window((0, 0), window = scrollable_frame, anchor = "nw")
        self.canv.configure(yscrollcommand = scroll_y.set)
        
        
        for obj in self.layers:
            button = self.create_button(obj, scrollable_frame)
            button.pack(side = tk.TOP)
            
        self.frame_pic.pack(side = tk.RIGHT, fill = tk.Y)
        scroll_y.pack(side = tk.LEFT, fill = tk.Y)  
        self.canv.pack(side = tk.RIGHT, fill = tk.Y)
         
        
    
    def result(self):
        self.menu_layers.pack(side = tk.LEFT, expand=True)
        self.list_layers()




