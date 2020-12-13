import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import csv
import matplotlib.pyplot as plt
import numpy as np

import classes as cl
import calculations as calc

# array of the layers
layers_list = []

# initial medium
initial_medium_refractive_index = 1
initial_medium_name = 'air'
# final medium
final_medium_refractive_index = 1
final_medium_name = 'air'

# wavelength of light in vacuum
vacuum_wavelength = 550

FRAME_WIDTH = 500
FRAME_HEIGHT = 500


def add_layer():
    global layers_list

    def ok_button_result(new_number, new_name: str, new_refractive_index: complex, new_thickness: float):
        global layers_list

        try:
            new_number = int(new_number)
        except:
            mb.showerror(title='Error',
                         message='Number of the layer should be integer in range from 0 (initial medium) to N (number of layers).')
            return

        if new_number < 0 or new_number > len(layers_list):
            mb.showerror(title='Error',
                         message='Number of the layer should be integer in range from 0 (initial medium) to N (number of layers).')
            return

        try:
            new_refractive_index = complex(new_refractive_index)
        except:
            mb.showerror(title='Error', message='Complex number should be inserted (without spaces).')
            return

        try:
            new_thickness = float(new_thickness)
        except:
            mb.showerror(title='Error', message='Real number should be inserted (without spaces).')
            return

        layers_list.insert(new_number, cl.Layer(new_number, new_name, new_refractive_index, new_thickness))
        for i in range(new_number, len(layers_list)):
            layers_list[i].number = layers_list[i].number + 1

        layer_widgets()
        adding_window.destroy()

    adding_window = tk.Toplevel(root)
    adding_window.geometry("+%d+%d" % (root.winfo_x() - FRAME_WIDTH // 2, root.winfo_y() + FRAME_HEIGHT // 2))
    adding_window.title('Add new layer')
    adding_window.iconbitmap('icon.ico')

    number_label = tk.Label(adding_window,
                            text='Number of the layer below which \n new layer will be added (0 = initial medium): ')
    number_combbox = ttk.Combobox(adding_window,
                                  values=list(range(0, len(layers_list) + 1)))
    number_combbox.current(len(layers_list))
    number_label.grid(row=0, column=0)
    number_combbox.grid(row=0, column=1)

    name_label = tk.Label(adding_window, text='Name of the additional layer: ')
    name_entry = tk.Entry(adding_window)
    name_entry.insert(0, 'air')
    name_label.grid(row=1, column=0)
    name_entry.grid(row=1, column=1)

    refractive_index_label = tk.Label(adding_window, text='Refractive index of the additional layer: ')
    refractive_index_entry = tk.Entry(adding_window)
    refractive_index_entry.insert(0, 1)
    refractive_index_label.grid(row=2, column=0)
    refractive_index_entry.grid(row=2, column=1)

    thickness_label = tk.Label(adding_window, text='Thickness of the additional layer: ')
    thickness_entry = tk.Entry(adding_window)
    thickness_entry.insert(0, 1000)
    thickness_label.grid(row=3, column=0)
    thickness_entry.grid(row=3, column=1)

    ok_button = tk.Button(adding_window, text='OK',
                          command=lambda: ok_button_result(number_combbox.get(), name_entry.get(),
                                                           refractive_index_entry.get(),
                                                           thickness_entry.get()))
    ok_button.grid(row=4, column=0, columnspan=2)


def change_layer(selected_layer: cl.Layer):
    global layers_list

    if len(layers_list) == 0:
        mb.showerror(title='Error', message='You have no layers. Firstly add one layer.')
        return

    def ok_button_result(new_number, new_name: str, new_refractive_index: complex, new_thickness: float):
        global layers_list

        try:
            new_number = int(new_number)
        except:
            mb.showerror(title='Error',
                         message='Number of the layer should be integer in range from 1 to N (number of layers).')
            return

        if new_number < 1 or new_number > len(layers_list):
            mb.showerror(title='Error',
                         message='Number of the layer should be integer in range from 1 to N (number of layers).')
            return

        try:
            new_refractive_index = complex(new_refractive_index)
        except:
            mb.showerror(title='Error', message='Complex number should be inserted (without spaces).')
            return

        try:
            new_thickness = float(new_thickness)
        except:
            mb.showerror(title='Error', message='Real number should be inserted (without spaces).')
            return

        layers_list[new_number - 1] = cl.Layer(new_number, new_name, new_refractive_index, new_thickness)

        layer_widgets()
        changing_window.destroy()

    changing_window = tk.Toplevel(root)
    changing_window.geometry("+%d+%d" % (root.winfo_x() - FRAME_WIDTH // 2, root.winfo_y() + FRAME_HEIGHT // 2))
    changing_window.title('Change the layer')
    changing_window.iconbitmap('icon.ico')

    number_label = tk.Label(changing_window, text='Number of the changing layer: ')
    number_combbox = ttk.Combobox(changing_window,
                                  values=list(range(1, len(layers_list) + 1)))
    number_combbox.current(selected_layer.number - 1)
    number_label.grid(row=0, column=0)
    number_combbox.grid(row=0, column=1)

    name_label = tk.Label(changing_window, text='Name of the changing layer: ')
    name_entry = tk.Entry(changing_window)
    name_entry.insert(0, selected_layer.name)
    name_label.grid(row=1, column=0)
    name_entry.grid(row=1, column=1)

    refractive_index_label = tk.Label(changing_window, text='Refractive index of the changing layer: ')
    refractive_index_entry = tk.Entry(changing_window)
    refractive_index_entry.insert(0, selected_layer.refractive_index)
    refractive_index_label.grid(row=2, column=0)
    refractive_index_entry.grid(row=2, column=1)

    thickness_label = tk.Label(changing_window, text='Thickness of the changing layer: ')
    thickness_entry = tk.Entry(changing_window)
    thickness_entry.insert(0, selected_layer.thickness)
    thickness_label.grid(row=3, column=0)
    thickness_entry.grid(row=3, column=1)

    ok_button = tk.Button(changing_window, text='OK',
                          command=lambda: ok_button_result(number_combbox.get(), name_entry.get(),
                                                           refractive_index_entry.get(),
                                                           thickness_entry.get()))
    ok_button.grid(row=4, column=0, columnspan=2)


def delete_layer(number: int):
    global layers_list

    if len(layers_list) == 0:
        mb.showerror(title='Error', message='You have no layers. Firstly add one layer.')
        return

    def ok_button_result(new_number):
        global layers_list

        try:
            new_number = int(new_number)
        except:
            mb.showerror(title='Error',
                         message='Number of the layer should be integer in range from 1 to N (number of layers).')
            return

        if new_number < 1 or new_number > len(layers_list):
            mb.showerror(title='Error',
                         message='Number of the layer should be integer in range from 1 to N (number of layers).')
            return

        layers_list.pop(new_number - 1)
        for i in range(new_number - 1, len(layers_list)):
            layers_list[i].number = layers_list[i].number - 1

        layer_widgets()
        deleting_window.destroy()

    deleting_window = tk.Toplevel(root)
    deleting_window.geometry("+%d+%d" % (root.winfo_x() - FRAME_WIDTH // 2, root.winfo_y() + FRAME_HEIGHT // 2))
    deleting_window.title('Delete the layer')
    deleting_window.iconbitmap('icon.ico')

    number_label = tk.Label(deleting_window, text='Number of the deleting layer: ')
    number_combbox = ttk.Combobox(deleting_window,
                                  values=list(range(1, len(layers_list) + 1)))
    number_combbox.current(number - 1)
    number_label.grid(row=0, column=0)
    number_combbox.grid(row=0, column=1)

    ok_button = tk.Button(deleting_window, text='OK',
                          command=lambda: ok_button_result(number_combbox.get()))
    ok_button.grid(row=1, column=0, columnspan=2)


def change_medium():
    pass


def plot_graph():
    pass


def read_data(input_filename: str):
    global vacuum_wavelength
    global initial_medium_name
    global initial_medium_refractive_index
    global final_medium_name
    global final_medium_refractive_index
    global layers_list

    layers_list = []
    with open(input_filename) as file:
        reader = csv.reader(file, delimiter=';')

        row1 = next(reader)
        vacuum_wavelength = float(row1[0])
        row2 = next(reader)
        initial_medium_name = row2[0]
        initial_medium_refractive_index = float(row2[1])
        row3 = next(reader)
        final_medium_name = row3[0]
        final_medium_refractive_index = float(row3[1])

        for row in reader:
            if len(row) == 4:
                number = int(row[0])
                name = row[1]
                refractive_index = complex(row[2])
                thickness = float(row[3])
                layers_list.append(cl.Layer(number, name, refractive_index, thickness))
            else:
                break

        layer_widgets()


def open_file_dialog():
    input_filename = fd.askopenfilename(filetypes=(("CSV Files", "*.csv"),))
    read_data(input_filename)


def write_data(output_filename: str):
    pass


def save_file_dialog():
    output_filename = fd.asksaveasfilename(filetypes=(("CSV Files", "*.csv"),))
    write_data(output_filename)


def info():
    info_window = tk.Toplevel(root)
    info_window.title('Help')
    info_window.iconbitmap('icon.ico')

    info_text = '''
        The program allows to calculate the reflection, refraction and absorption coefficients of light incident on a film consisting of several layers.

        The program plots the dependence of these coefficients and allows to read the data from the file, edit them and write them back to the file.

        Buttons

        File - menu for opening and saving files
        Add new layer - adding a layer to the list
        Change a layer - changing characteristics of a layer
        Delete a layer - deleting a layer from the list
        Change a medium - changing characteristics of a medium
        Plot the graph - plotting the graph of coefficients versus the angle
        '''
    info_label = tk.Label(info_window, text=info_text, justify=tk.LEFT)
    info_label.pack()


def layer_widgets():
    pass


root = tk.Tk()
root.geometry(
    '%dx%d+%d+%d' % (FRAME_WIDTH, FRAME_HEIGHT, root.winfo_screenwidth() // 3, root.winfo_screenheight() // 3))
root.resizable(width=True, height=True)
root.title('Simulation program for the analysis of multilayer media')
root.iconbitmap('icon.ico')

buttons_frame = tk.Frame(root)
buttons_frame.pack(side=tk.BOTTOM)
add_layer_button = tk.Button(buttons_frame, text="Add new layer", command=add_layer)
add_layer_button.pack(side=tk.LEFT)
change_layer_button = tk.Button(buttons_frame, text="Change a layer",
                                command=lambda: change_layer(cl.Layer(1, 'air', 1, 0)))
change_layer_button.pack(side=tk.LEFT)
delete_layer_button = tk.Button(buttons_frame, text="Delete a layer", command=lambda: delete_layer(1))
delete_layer_button.pack(side=tk.LEFT)
change_medium_button = tk.Button(buttons_frame, text="Change a medium", command=change_medium)
change_medium_button.pack(side=tk.LEFT)
plot_graph_button = tk.Button(buttons_frame, text='Plot the graph', command=plot_graph)
plot_graph_button.pack(side=tk.LEFT)

main_menu = tk.Menu(root)
root.config(menu=main_menu)
file_menu = tk.Menu(main_menu, tearoff=0)
file_menu.add_command(label="Open...", command=open_file_dialog)
file_menu.add_command(label="Save as...", command=save_file_dialog)
main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_command(label="Help", command=info)

layer_widgets()

root.mainloop()