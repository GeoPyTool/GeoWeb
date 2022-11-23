from nicegui import ui
import numpy as np
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
from functools import partial

# table = ui.table({
#     'columnDefs': [
#         {'headerName': 'Name', 'field': 'name'},
#         {'headerName': 'Age', 'field': 'age'},
#     ],
#     'rowData': [
#         {'name': 'Alice', 'age': 18},
#         {'name': 'Bob', 'age': 21},
#         {'name': 'Carol', 'age': 42},
#     ],
# }).classes('max-h-40')

# with ui.plot(figsize=(2.5, 1.8)):
#     x = np.linspace(0.0, 5.0)
#     y = np.cos(2 * np.pi * x) * np.exp(-x)
#     plt.plot(x, y, '-')
#     plt.xlabel('time (s)')
#     plt.ylabel('Damped oscillation')

# def update():
#     table.options.rowData[0].age += 1
#     table.update()



# ui.button('Update', on_click=update)

diagram = ui.plot()
diagram.figsize=(2.5, 1.8)
x = np.linspace(0.0, 5.0)
y = np.cos(2 * np.pi * x) * np.exp(-x)
plt.plot(x, y, '-')
plt.xlabel('time (s)')
plt.ylabel('Damped oscillation')
diagram.view.set_figure(plt.gcf())
img_tosave =plt.gcf()

def saveIMG():
    plt.savefig("vector.svg")

ui.button('Save IMG', on_click=saveIMG)

d = 0
ui.upload(on_upload=lambda e: exec("return e"))
print(d)

ui.run()
