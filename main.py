import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import csv
import plotly.graph_objs as go
from plotly.offline import iplot
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

# number of points for graph
number_of_points = 1000

# sizes of the main frame
FRAME_WIDTH = 500
FRAME_HEIGHT = 500


def change_wavelength():
    '''
    Changes the wavelength of light in vacuum.

    @return: None
    '''
    global vacuum_wavelength

    new_wavelength = wavelength_entry.get()

    try:
        new_wavelength = float(new_wavelength)
    except:
        mb.showerror(title='Error',
                     message='Wavelength of light in vacuum should be a real number.')
        wavelength_entry.delete(0, tk.END)
        wavelength_entry.insert(0, vacuum_wavelength)
        return

    vacuum_wavelength = new_wavelength
    root.focus_set()


def change_number_of_points():
    '''
    Changes number of points for graph.

    @return: None
    '''
    global number_of_points

    new_number_of_points = number_of_points_entry.get()

    try:
        new_number_of_points = int(new_number_of_points)
    except:
        mb.showerror(title='Error',
                     message='Number of points for graph should be an integer number.')
        number_of_points_entry.delete(0, tk.END)
        number_of_points_entry.insert(0, number_of_points)
        return

    number_of_points = new_number_of_points
    root.focus_set()


def add_layer():
    '''
    Adds new layer after chosen layer with its characteristics via settings window.

    @return: None
    '''
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
    '''
    Changes characteristics of the selected layer via settings window.

    @param cl.Layer selected_layer: the layer that has to be changed
    @return: None
    '''
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
    '''
    Deletes the selected layer.

    @param int number: number of the layer to delete
    @return: None
    '''
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
    '''
    Changes characteristics of the selected medium (initial or final) via settings window.

    @return: None
    '''
    global initial_medium_name
    global initial_medium_refractive_index

    def ok_button_result(medium: str, new_name: str, new_refractive_index: float):
        global initial_medium_name
        global initial_medium_refractive_index
        global final_medium_name
        global final_medium_refractive_index

        try:
            new_refractive_index = float(new_refractive_index)
        except:
            mb.showerror(title='Error', message='Complex number should be inserted (without spaces).')
            return

        if medium == 'initial medium':
            initial_medium_name = new_name
            initial_medium_refractive_index = new_refractive_index

        if medium == 'final medium':
            final_medium_name = new_name
            final_medium_refractive_index = new_refractive_index

        layer_widgets()
        changing_window.destroy()

    changing_window = tk.Toplevel(root)
    changing_window.geometry("+%d+%d" % (root.winfo_x() - FRAME_WIDTH // 2, root.winfo_y() + FRAME_HEIGHT // 2))
    changing_window.title('Change the medium')
    changing_window.iconbitmap('icon.ico')

    number_label = tk.Label(changing_window, text='The changing medium: ')
    number_combbox = ttk.Combobox(changing_window,
                                  values=['initial medium', 'final medium'], state='readonly')
    number_combbox.current(0)
    number_label.grid(row=0, column=0)
    number_combbox.grid(row=0, column=1)

    name_label = tk.Label(changing_window, text='Name of the changing layer: ')
    name_entry = tk.Entry(changing_window)
    name_entry.insert(0, initial_medium_name)
    name_label.grid(row=1, column=0)
    name_entry.grid(row=1, column=1)

    refractive_index_label = tk.Label(changing_window, text='Refractive index of the changing layer: ')
    refractive_index_entry = tk.Entry(changing_window)
    refractive_index_entry.insert(0, initial_medium_refractive_index)
    refractive_index_label.grid(row=2, column=0)
    refractive_index_entry.grid(row=2, column=1)

    ok_button = tk.Button(changing_window, text='OK',
                          command=lambda: ok_button_result(number_combbox.get(), name_entry.get(),
                                                           refractive_index_entry.get()))
    ok_button.grid(row=3, column=0, columnspan=2)


def plot_graph(TE_var1, TE_var2, TE_var3, TM_var1, TM_var2, TM_var3):
    '''
    Plots a graph in a new window.

    @return: None
    '''
    if (TE_var1 or TE_var2 or TE_var3 or TM_var1 or TM_var2 or TM_var3) == False:
        mb.showerror(title="Error", message="Please, choose the value to plot.")
        return

    new_calc = calc.Calculations(layers_list, initial_medium_refractive_index, final_medium_refractive_index,
                                 vacuum_wavelength)
    theta = np.linspace(0, np.pi / 2, number_of_points)
    figure = go.Figure()
    if TE_var1: figure.add_trace(go.Scatter(x=theta, y=new_calc.TE_reflectance()(theta), name="TE reflectance"))
    if TE_var2: figure.add_trace(go.Scatter(x=theta, y=new_calc.TE_transmittance()(theta), name="TE transmittance"))
    if TE_var3: figure.add_trace(
        go.Scatter(x=theta, y=new_calc.TE_absorption_coefficient()(theta), name="TE absorption coefficient"))
    if TM_var1: figure.add_trace(go.Scatter(x=theta, y=new_calc.TM_reflectance()(theta), name="TM reflectance"))
    if TM_var2: figure.add_trace(go.Scatter(x=theta, y=new_calc.TM_transmittance()(theta), name="TM transmittance"))
    if TM_var3: figure.add_trace(
        go.Scatter(x=theta, y=new_calc.TM_absorption_coefficient()(theta), name="TM absorption coefficient"))

    figure.update_xaxes(title="angle, rad")
    figure.update_yaxes(title="coefficient, 1")
    figure.show()


def read_data(input_filename: str):
    '''
    Reads data from the file and parses it.

    @param str input_filename: path to the file to read data
    @return: None
    '''
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

        wavelength_entry.delete(0, tk.END)
        wavelength_entry.insert(0, vacuum_wavelength)

        layer_widgets()


def open_file_dialog():
    '''
    Opens file .csv to read the data of multilayer media.

    @return: None
    '''
    input_filename = fd.askopenfilename(filetypes=(("CSV Files", "*.csv"),))
    read_data(input_filename)


def write_data(output_filename: str):
    '''
    Writes parameters of multilayer media and calculated data.

    @param str output_filename: path to the file to write data
    @return: None
    '''
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')

        writer.writerow([vacuum_wavelength])
        writer.writerow([initial_medium_name, initial_medium_refractive_index])
        writer.writerow([final_medium_name, final_medium_refractive_index])

        layers = []
        for layer in layers_list:
            layers.append([layer.number, layer.name, layer.refractive_index, layer.thickness])
        writer.writerows(layers)


def save_file_dialog():
    '''
    Saves parameters of multilayer media and calculated data to .csv file.

    @return: None
    '''
    output_filename = fd.asksaveasfilename(filetypes=(("CSV Files", "*.csv"),))
    write_data(output_filename)


def info():
    '''
    Displays a window with helpful information.

    @return: None
    '''
    info_window = tk.Toplevel(root)
    info_window.title('Help')
    info_window.iconbitmap('icon.ico')

    info_text = '''
        The program allows to calculate the reflection, refraction and absorption coefficients of light incident on a film consisting of several layers.

        The program plots the dependence of these coefficients and allows to read the data from the file, edit them and write them back to the file.

        Buttons:

        File - menu for opening and saving files
        Add new layer - adding a layer to the list
        Change a layer - changing characteristics of a layer
        Delete a layer - deleting a layer from the list
        Change a medium - changing characteristics of a medium
        Plot the graph - plotting the graph of the chosen coefficients versus the angle
        '''
    info_label = tk.Label(info_window, text=info_text, justify=tk.LEFT)
    info_label.pack()


def layer_widgets():
    '''
    Displays the stack of layers in the main window.
    Use it to refresh displayed layers.

    @return: None
    '''
    global scrollable_frame

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    label_initial_medium = tk.Label(scrollable_frame,
                                    text='Initial medium: ' + initial_medium_name + '\n Refractive index: {}'.format(
                                        initial_medium_refractive_index),
                                    font='Arial 10', bg='light blue', width=55, borderwidth=1, relief='solid')
    label_initial_medium.pack(side=tk.TOP)

    for layer in layers_list:
        label_layer = tk.Label(scrollable_frame, text='Layer №{}'.format(layer.number) + ': ' + layer.name +
                                                      '\n Refractive index: {}'.format(
                                                          layer.refractive_index) + '\n Thickness: {}'.format(
            layer.thickness), font='Arial 10', width=55, borderwidth=1, relief='solid')
        label_layer.pack(side=tk.TOP)

    label_final_medium = tk.Label(scrollable_frame,
                                  text='Final medium: ' + final_medium_name + '\n Refractive index: {}'.format(
                                      final_medium_refractive_index),
                                  font='Arial 10', bg='white', width=55, borderwidth=1, relief='solid')
    label_final_medium.pack(side=tk.TOP)


# Root frame
root = tk.Tk()
root.geometry(
    '%dx%d+%d+%d' % (FRAME_WIDTH, FRAME_HEIGHT, root.winfo_screenwidth() // 3, root.winfo_screenheight() // 3))
root.resizable(width=True, height=True)
root.title('Simulation program for the analysis of multilayer media')
root.iconbitmap('icon.ico')

# Checkbuttons
TM_checkbuttons_frame = tk.Frame(root)
TM_checkbuttons_frame.pack(side=tk.BOTTOM)

TM_var1 = tk.BooleanVar()
TM_var1.set(False)
TM_c1 = tk.Checkbutton(TM_checkbuttons_frame, text="TM reflectance",
                       variable=TM_var1,
                       onvalue=True, offvalue=False)
TM_c1.pack(side=tk.LEFT)
TM_var2 = tk.BooleanVar()
TM_var2.set(False)
TM_c2 = tk.Checkbutton(TM_checkbuttons_frame, text="TM transmittance",
                       variable=TM_var2,
                       onvalue=True, offvalue=False)
TM_c2.pack(side=tk.LEFT)
TM_var3 = tk.BooleanVar()
TM_var3.set(False)
TM_c3 = tk.Checkbutton(TM_checkbuttons_frame, text="TM absorption coefficient",
                       variable=TM_var3,
                       onvalue=True, offvalue=False)
TM_c3.pack(side=tk.LEFT)

TE_checkbuttons_frame = tk.Frame(root)
TE_checkbuttons_frame.pack(side=tk.BOTTOM)

TE_var1 = tk.BooleanVar()
TE_var1.set(False)
TE_c1 = tk.Checkbutton(TE_checkbuttons_frame, text="TE reflectance",
                       variable=TE_var1,
                       onvalue=True, offvalue=False)
TE_c1.pack(side=tk.LEFT)
TE_var2 = tk.BooleanVar()
TE_var2.set(False)
TE_c2 = tk.Checkbutton(TE_checkbuttons_frame, text="TE transmittance",
                       variable=TE_var2,
                       onvalue=True, offvalue=False)
TE_c2.pack(side=tk.LEFT)
TE_var3 = tk.BooleanVar()
TE_var3.set(False)
TE_c3 = tk.Checkbutton(TE_checkbuttons_frame, text="TE absorption coefficient",
                       variable=TE_var3,
                       onvalue=True, offvalue=False)
TE_c3.pack(side=tk.LEFT)

# Buttons
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
plot_graph_button = tk.Button(buttons_frame, text="Plot a graph",
                              command=lambda: plot_graph(TE_var1.get(), TE_var2.get(), TE_var3.get(), TM_var1.get(),
                                                         TM_var2.get(), TM_var3.get()))
plot_graph_button.pack(side=tk.LEFT)

# Entry for wavelength
wavelength_frame = tk.Frame(root)
wavelength_frame.pack(side=tk.TOP)
wavelength_label = tk.Label(wavelength_frame, text="Wavelength of light in vacuum: ", width=30)
wavelength_label.pack(side=tk.LEFT)
wavelength_entry = tk.Entry(wavelength_frame)
wavelength_entry.insert(0, vacuum_wavelength)
wavelength_entry.pack(side=tk.LEFT)
wavelength_button = tk.Button(wavelength_frame, text="OK", command=change_wavelength)
wavelength_button.pack(side=tk.LEFT)

# Entry for number of points
number_of_points_frame = tk.Frame(root)
number_of_points_frame.pack(side=tk.TOP)
number_of_points_label = tk.Label(number_of_points_frame, text="Number of points for the graph: ", width=30)
number_of_points_label.pack(side=tk.LEFT)
number_of_points_entry = tk.Entry(number_of_points_frame)
number_of_points_entry.insert(0, number_of_points)
number_of_points_entry.pack(side=tk.LEFT)
number_of_points_button = tk.Button(number_of_points_frame, text="OK", command=change_number_of_points)
number_of_points_button.pack(side=tk.LEFT)

# Main menu on the top of the window
main_menu = tk.Menu(root)
root.config(menu=main_menu)
file_menu = tk.Menu(main_menu, tearoff=0)
file_menu.add_command(label="Open...", command=open_file_dialog)
file_menu.add_command(label="Save as...", command=save_file_dialog)
main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_command(label="Help", command=info)

# Environment for scrolling layers
main_frame = tk.Frame(root)
canvas = tk.Canvas(main_frame)
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)

scrollable_frame = tk.Frame(canvas)
scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)

main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Imaging of multilayer medium
layer_widgets()

root.mainloop()
