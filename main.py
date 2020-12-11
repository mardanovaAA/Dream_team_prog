import tkinter as tk
from tkinter import filedialog as fd
import classes as cl
import csv
import numpy as np
import matplotlib.pyplot as plt
import calculations as cal

# array of the layers
layer_objects = []

root = tk.Tk()
root.geometry('1000x500')
root.resizable(width=True, height=True)


def input_file(input_filename):
    '''
    Function for reading data from a file
    Returns an array of elements, each of which is a layer.
    input_filename - file
    '''
    sloi = []
    with open(input_filename) as File:
        reader = csv.reader(File, delimiter=',')
        for row in reader:
            sloy = cl.Layer()
            parse_parameters(row, sloy)
            sloi.append(sloy)
    return sloi


def save_file_dialog():
    '''
    Function that opens the file saving window
    '''
    out_filename = fd.asksaveasfilename(filetypes=(("CSV Files", "*.csv"),))
    output_write(out_filename, layer_objects)


def output_write(output_filename, layer_objects):
    '''
    Function that writes data into a file
    output_filename - file
    layer_objects - layer list
    '''
    data = []
    for obj in layer_objects:
        line = [obj.number, obj.name, obj.refractive_index, obj.thickness]
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
    Layer.refractive_index = complex(row[2])
    Layer.thickness = float(row[3])


def open_file_dialog():
    '''
    Function that opens a window to read the file
    '''
    global layer_objects
    # global perform_execution
    # perform_execution = False
    in_filename = fd.askopenfilename(filetypes=(("CSV Files", "*.csv"),))
    layer_objects.clear()
    layer_objects.extend(input_file(in_filename))


def Layer_list():
    '''
    Function that shows list of the layers on the screen
    '''
    for widget in flist.winfo_children():
        widget.destroy()
    # frames for scrollers
    flist_top = tk.Frame(flist)
    flist_bot = tk.Frame(flist)
    flist_top.pack()
    flist_bot.pack()

    scroll_x = tk.Scrollbar(flist_top, orient=tk.HORIZONTAL)
    scroll_y = tk.Scrollbar(flist_bot, orient=tk.VERTICAL)
    lbox = tk.Listbox(flist_bot, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set,
                      width=50, height=50)

    for obj in layer_objects:
        line = '#' + str(obj.number) + '  ' + 'Name: ' + str(obj.name) + '  ' + 'Refractive index: ' + str(
            obj.refractive_index) + '  ' + 'Thickness: ' + str(obj.thickness)
        lbox.insert(tk.END, line)

    lbox.pack(side=tk.LEFT)
    scroll_x.config(command=lbox.xview)
    scroll_y.config(command=lbox.yview)
    scroll_x.pack(fill=tk.X)
    scroll_y.pack(side=tk.LEFT, fill=tk.Y)


def add_layer():
    '''
    Function that opens a window to add a layer

    '''

    def add_lay():
        '''
        Function that adds a layer

        '''
        number = 0
        transport = cl.Layer()

        newlayer = cl.Layer()

        newlayer.number = int(tnumber.get())

        newlayer.name = str(tname.get())

        newlayer.permittivity = complex(tpermittivity.get())

        newlayer.thickness = float(tthickness.get())
        '''Imp'''
        layer_objects.append(newlayer)
        for i in range(len(layer_objects) - 1):
            for j in range((len(layer_objects) - i - 1)):
                if layer_objects[j].number >= layer_objects[j + 1].number:
                    transport = layer_objects[j]
                    layer_objects[j] = layer_objects[j + 1]
                    layer_objects[j + 1] = transport
        for i in range(int(tnumber.get()), len(layer_objects) - 1):
            layer_objects[i].number += 1
        layer_objects[-1].number += 1
        addlayerwindow.destroy()
        for i in range(len(layer_objects)):
            layer_objects[i].number = i + 1

    tnumber = tk.StringVar()
    tname = tk.StringVar()
    tthickness = tk.StringVar()
    tpermittivity = tk.StringVar()

    addlayerwindow = tk.Toplevel(root)

    lnumber = tk.Label(addlayerwindow, text='Номер слоя')
    lnumber.pack()
    enumber = tk.Entry(addlayerwindow, width=50, textvariable=tnumber)
    enumber.pack()

    lname = tk.Label(addlayerwindow, text='Имя слоя')
    lname.pack()
    ename = tk.Entry(addlayerwindow, width=50, textvariable=tname)
    ename.pack()

    lpermittivity = tk.Label(addlayerwindow, text='Проницаемость')
    lpermittivity.pack()
    epermittivity = tk.Entry(addlayerwindow, width=50, textvariable=tpermittivity)
    epermittivity.pack()

    lthickness = tk.Label(addlayerwindow, text='Толщина')
    lthickness.pack()
    ethickness = tk.Entry(addlayerwindow, width=50, textvariable=tthickness)
    ethickness.pack()

    add = tk.Button(addlayerwindow, text='Добавить слой', command=add_lay)
    add.pack()


def change_layer():
    for widget in flist.winfo_children():
        lbox = widget
    line = str(lbox.curselection())
    obj = line.split()
    number_x = int(obj[0][1:])
    name_x = str(obj[2])
    thickness_x = int(obj[7])
    permittivity_x = complex(obj[5])

    def change_lay():
        '''
        Function that change a layer

        '''

        oldnumber = number_x
        changed = layer_objects[number_x - 1]
        number_x = int(tnumber.get())
        name_x = str(tname.get())
        thickness_x = complex(tpermittivity.get())
        permittivity_x = float(tthickness.get())
        '''Imp'''
        changed.number = number_x
        changed.name = name_x
        changed.thickness = thickness_x
        changed.refractive_index = permittivity_x
        layer_objects[oldnumber - 1] = changed
        for i in range(len(layer_objects) - 1):
            for j in range((len(layer_objects) - i - 1)):
                if layer_objects[j].number >= layer_objects[j + 1].number:
                    transport = layer_objects[j]
                    layer_objects[j] = layer_objects[j + 1]
                    layer_objects[j + 1] = transport
        for i in range(int(tnumber.get()), len(layer_objects) - 1):
            layer_objects[i].number += 1
        layer_objects[-1].number += 1
        addlayerwindow.destroy()
        for i in range(len(layer_objects)):
            layer_objects[i].number = i + 1

    changelayerwindow = tk.Toplevel(root)
    tnumber = tk.StringVar()
    tname = tk.StringVar()
    tthickness = tk.StringVar()
    tpermittivity = tk.StringVar()

    addlayerwindow = tk.Toplevel(root)

    lnumber = tk.Label(addlayerwindow, text='Номер слоя')
    lnumber.pack()
    enumber = tk.Entry(addlayerwindow, width=50, textvariable=tnumber)
    enumber.pack()

    lname = tk.Label(addlayerwindow, text='Имя слоя')
    lname.pack()
    ename = tk.Entry(addlayerwindow, width=50, textvariable=tname)
    ename.pack()

    lpermittivity = tk.Label(addlayerwindow, text='Проницаемость')
    lpermittivity.pack()
    epermittivity = tk.Entry(addlayerwindow, width=50, textvariable=tpermittivity)
    epermittivity.pack()

    lthickness = tk.Label(addlayerwindow, text='Толщина')
    lthickness.pack()
    ethickness = tk.Entry(addlayerwindow, width=50, textvariable=tthickness)
    ethickness.pack()

    add = tk.Button(addlayerwindow, text='Добавить слой', command=change_lay)
    add.pack()


def Builtgraph():
    '''
    Function that show graphs

    '''
    cal.layers_list = layer_objects
    cal.BuiltGraph()


def info():
    showinfowindow = tk.Toplevel(root)
    text = '''
    The program allows to calculate the reflection, refraction and absorption coefficients of light incident on a film consisting of several layers.

    The program plots the dependence of these coefficients and allows to read the data from the file, edit them and write them back to the file.

    Buttons

    Файл - menu for opening and saving files
    Добавить слой - adding a layer to the list
    Построить график - builds the graph of coefficients dependence on the angle


    '''
    infolabel = tk.Label(showinfowindow, text=text, justify=tk.LEFT)
    infolabel.pack()


def clear_list():
    layer_objects.clear()


# Buttons
frame = tk.Frame(root)
frame.pack(side=tk.BOTTOM)
add_layer_button = tk.Button(frame, text="Добавить слой", command=add_layer)
add_layer_button.pack(side=tk.LEFT)
changelayer = tk.Button(frame, text="Изменить слой", command=change_layer)
'''changelayer.pack(side=tk.LEFT)'''
clearlist = tk.Button(frame, text="Очистить", command=clear_list)
clearlist.pack(side=tk.LEFT)
addgraph = tk.Button(frame, text='Построить график', command=Builtgraph)
addgraph.pack(side=tk.LEFT)
flist = tk.Frame(root)
flist.pack(side=tk.LEFT)
# Main menu on the top of the window
mainmenu = tk.Menu(root)
root.config(menu=mainmenu)
filemenu = tk.Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Открыть...", command=open_file_dialog)
filemenu.add_command(label="Сохранить файл как...", command=save_file_dialog)
mainmenu.add_cascade(label="Файл", menu=filemenu)
mainmenu.add_command(label="Показать список слоёв", command=Layer_list)
mainmenu.add_command(label="Справка", command=info)

# testmenu=Mainmenu(root)

tk.mainloop()
