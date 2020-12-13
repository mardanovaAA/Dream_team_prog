import tkinter as tk


class Layer():
    """
    Layer of a material.
    """

    def __init__(self, number: int, name: str, refractive_index: complex, thickness: float):
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

    def __str__(self):
        return "№ " + str(self.number) + ", " + self.name + ",n = " + str(self.refractive_index) + ", h = " + str(
            self.thickness)


class LayerWidget():
    """
    Layer image on the screen.
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
        but = tk.Button(fr, text=text_but, width=30, height=4)
        but['activebackground'] = 'CadetBlue2'
        but['activeforeground'] = 'white'
        but['bg'] = 'CadetBlue1'
        return but

    def list_layers(self):
        """
        Creates picture of layers on the screen
        """
        scroll_y = tk.Scrollbar(self.frame_pic, orient=tk.VERTICAL, command=self.canv.yview)
        scrollable_frame = tk.Frame(self.canv)
        scrollable_frame.bind("<Configure>", lambda e: self.canv.configure(scrollregion=self.canv.bbox("all")))
        self.canv.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.canv.configure(yscrollcommand=scroll_y.set)

        for obj in self.layers:
            button = self.create_button(obj, scrollable_frame)
            button.pack(side=tk.TOP)

        self.frame_pic.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_y.pack(side=tk.LEFT, fill=tk.Y)
        self.canv.pack(side=tk.RIGHT, fill=tk.Y)

    def result(self):
        self.menu_layers.pack(side=tk.LEFT, expand=True)
        self.list_layers()
