from tkinter import *
from tkinter.filedialog import *
from classes import *
import csv
import numpy as np
import matplotlib.pyplot as plt

#array of the layers
layer_objects = []


root = Tk()
root.geometry('500x500')
root.resizable(width = True, height = True)

def input_file(input_filename):
    '''
    Function for reading data from a file
    Returns an array of elements, each of which is a layer.
    input_filename - file
    '''
    sloi = []
    with open(input_filename) as File:
        reader = csv.reader(File, delimiter = ',')
        for row in reader:
            sloy = Layer()
            parse_parameters(row, sloy)
            sloi.append(sloy)
    return sloi

def save_file_dialog():
    '''
    Function that opens the file saving window
    '''
    out_filename = asksaveasfilename(filetypes=(("CSV Files", "*.csv"),))
    output_write(out_filename, layer_objects)

def output_write(output_filename, layer_objects):
    '''
    Function that writes data into a file
    output_filename - file
    layer_objects - layer list
    '''
    data = []
    for obj in layer_objects:
        line = [obj.number,obj.name,obj.permittivity,obj.thickness]
        data.append(line)
    with open(output_filename, 'w', newline='') as File:
        writer = csv.writer(File)
        writer.writerows(data)


def parse_parameters(row, Layer):
    '''
    Parsing the parameters of the layers, which are read from the file
    row - string of the file
    Layer - array element
    '''
    Layer.number = int(row[0])
    Layer.name = str(row[1])
    Layer.permittivity = complex(row[2])
    Layer.thickness = float(row[3])

def open_file_dialog():
    '''
    Function that opens a window to read the file
    '''
    global layer_objects
    #global perform_execution
    #perform_execution = False
    in_filename = askopenfilename(filetypes=(("CSV Files", "*.csv"),))
    layer_objects.extend(input_file(in_filename))


def Layer_list():
    '''
    Function that shows list of the layers on the screen
    '''
    for widget in flist.winfo_children():
        widget.destroy()

    lbox = Listbox(flist,width = 50, height = 50)

    for obj in layer_objects:
        line = '#' + str(obj.number) + '  ' + 'Name: ' + str(obj.name) + '  ' + 'Permittivity: ' +str(obj.permittivity) + '  ' + 'Thickness: ' + str(obj.thickness)
        lbox.insert(END, line)
    lbox.pack(side=LEFT)



def add_layer():
    '''
    Function that opens a window to add a layer

    '''

    def add_lay():
        '''
        Function that adds a layer

        '''
        number = 0
        transport = Layer()

        newlayer = Layer()

        newlayer.number=int(tnumber.get())

        newlayer.name=str(tname.get())

        newlayer.permittivity=complex(tpermittivity.get())

        newlayer.thickness=float(tthickness.get())
        layer_objects.append(newlayer)
        for i in range(len(layer_objects)-1):
            for j in range((len(layer_objects)-i-1)):
                if layer_objects[j].number >= layer_objects[j+1].number:
                    transport = layer_objects[j]
                    layer_objects[j] = layer_objects[j+1]
                    layer_objects[j+1] = transport
        for i in range(int(tnumber.get()), len(layer_objects)-1 ):
            layer_objects[i].number += 1
        layer_objects[-1].number += 1
        addlayerwindow.destroy()

    tnumber = StringVar()
    tname = StringVar()
    tthickness = StringVar()
    tpermittivity = StringVar()

    addlayerwindow = Toplevel(root)

    lnumber=Label(addlayerwindow,text='Номер слоя')
    lnumber.pack()
    enumber = Entry(addlayerwindow,width=50, textvariable = tnumber )
    enumber.pack()

    lname=Label(addlayerwindow,text='Имя слоя')
    lname.pack()
    ename = Entry(addlayerwindow,width=50, textvariable = tname)
    ename.pack()

    lpermittivity=Label(addlayerwindow,text='Проницаемость')
    lpermittivity.pack()
    epermittivity = Entry(addlayerwindow,width=50, textvariable = tpermittivity)
    epermittivity.pack()

    lthickness=Label(addlayerwindow,text='Толщина')
    lthickness.pack()
    ethickness = Entry(addlayerwindow,width=50, textvariable = tthickness)
    ethickness.pack()

    add = Button(addlayerwindow, text='Добавить слой',command=add_lay)
    add.pack()

def Builtgraph():
    '''
    Function that show graphs

    '''
    angle = np.arange(0, 90.1, 0.1)
    f = 0
    p = plt.subplot(111)
    for i in layer_objects:
        f = f + i.thickness*i.permittivity.real
    f = f/len(layer_objects)
    plt.plot(angle, angle*f)
    plt.show()

#Buttons
frame = Frame(root)
frame.pack(side=BOTTOM)
add_layer_button = Button(frame, text="Добавить слой", command=add_layer)
add_layer_button.pack(side=LEFT)
addgraph=Button(frame,text='Построить график',command=Builtgraph)
addgraph.pack()
flist = Frame(root)
flist.pack(side=LEFT)

#Main menu on the top of the window
mainmenu = Menu(root)
root.config(menu=mainmenu)
filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Открыть...", command =open_file_dialog)
filemenu.add_command(label="Сохранить файл как...", command = save_file_dialog)
mainmenu.add_cascade(label="Файл",
                     menu=filemenu)
mainmenu.add_command(label="Показать список слоёв", command = Layer_list)
mainmenu.add_command(label="Справка")






#testmenu=Mainmenu(root)

mainloop()



