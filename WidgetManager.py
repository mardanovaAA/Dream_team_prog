import tkinter as tk
import LayerWidget

class WM():
    """
    This class is responsible for the program interface.
    """
    def __init__(self, root, SIZE):
        """
        Parameters
        ----------
        root : class tkinter.Tk() - the screen of the program 
        """
        self.root = root
        self.SIZE = SIZE
        self.canvas = tk.Canvas(root, width = SIZE[0], height = SIZE[1], bg='white')
        self.canvas.pack()
    
    def many_layers(self):
        """
        Prints the text, if the are too many layers to display on the screen
        """
        Text = self.canvas.create_text(self.SIZE[0] // 4, self.SIZE[1], 
                                       text = 'Too many layers for picture' + '\n' + 'You may use a manual input', font = '20')
        self.canvas.itemconfig(Text)
        
    def no_layers(self):
        """
        Prints the text, if the aren't any layers to display on the screenю
        """
        Text = self.canvas.create_text(self.SIZE[0] // 4, self.SIZE[1], 
                                       text = 'There are not any layers' + '\n' + 'Please, input some layers', font = '20')
        self.canvas.itemconfig(Text)
        
    def set_layers(self, Layers = []):
        """
        Creates layers on screen.
        if there aren't any layers, or too many - prints the text;  
        Parameters
        ----------
        Layers : the list of the class Layer.L() - thi list off all layers (the default is []).
        """
        self.Layers = Layers
        self.Layer_widget_list = []
        self.number_layers = len(self.Layers)
        if self.number_layers != 0:
            if (2 * self.SIZE[1] // 3) // self.number_layers < 30:
                self.many_layers()
            else:
                width_layer = (2 * self.SIZE[1] // 3) // self.number_layers
                for i, lay in enumerate(self.Layers):
                    lay_widget = LayerWidget.LW(self.canvas, lay, self.SIZE[0] // 6,
                                                                 (3 * self.SIZE[1] // 10) + lay.number * width_layer, width_layer, 5 * self.SIZE[0] // 24)
                    lay_widget.button()
                    self.Layer_widget_list.append(lay_widget)             
        else:
            self.no_layers()
                
            
        
        
        
        
        
       
        
    
    
    
    
    
    
    
    
    
    

