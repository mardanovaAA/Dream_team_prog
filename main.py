import tkinter as tk
import classes


root = tk.Tk()
SIZE = [800, 600]
root.geometry(str(SIZE[0]) + 'x' + str(SIZE[1]))

"""
Это заготовка будующей программы main, сюда я уже импортировала классы для удобства.
Следующие строчки можно спокойно убирать, они нужны были для отладки работы
"""
canvas = tk.Canvas(root, bg='white')
canvas.pack(fill=tk.BOTH, expand=1)
lay_1 = classes.Layer()
lay = classes.LayerWidget(canvas, lay_1, 200, 10)
lay.set_text(name = 'Hi', comment = 'Rrrrr')
lay.buttons()
canvas.update()


root.mainloop()