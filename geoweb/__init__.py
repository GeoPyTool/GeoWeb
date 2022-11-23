from nicegui import ui
from nicegui.events import UploadEventArguments
import numpy as np
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
from functools import partial
import sys,re,os,csv
from io import StringIO,BytesIO

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

def handle_upload(e: UploadEventArguments) -> None:
    name = e.names
    content = e.files
    # print(f'{name=}, {len(content)=}', flush=True)    
    global file_names
    global file_content
    file_names = e.names[0]
    file_content = e.files[0]
    x = np.linspace(0.0, 5.0)
    y = np.cos(2 * np.pi * x) * np.exp(-x)

    # string_content = str(file_content,'utf-8')
    # data = StringIO(string_content )
    # df = pd.read_csv(data)
    bytes_data = file_content
    print(name[0])
    if 'csv' in name[0]:
        df = pd.read_csv(BytesIO(bytes_data))
    elif 'xls' in name[0]:
        df = pd.read_excel(BytesIO(bytes_data),engine='openpyxl')
    else:
        pass

    columns_list= df.columns.tolist()
    Label_list = df['Label'].to_list()
    Color_list = df['Color'].to_list()

    SiO2= df['SiO2(wt%)'].to_list()
    Na2O= df['Na2O(wt%)'].to_list()
    K2O = df['K2O(wt%)'] .to_list()  
    
    Alkali = np.array(Na2O)+np.array(K2O)
    Silica = np.array(SiO2)

    print(df)
    make_plot(x= Alkali, y= Silica)


def make_plot(x=[],y=[],color='green', marker='o', linestyle='dashed',linewidth=2, markersize=12,alpha=0.5):
    diagram = ui.plot()
    # diagram.figsize=(2.5, 1.8)
    x = x
    y = y
    plt.plot(x, y, color=color, marker=marker, linestyle=linestyle,linewidth=linewidth, markersize=markersize,alpha=alpha)
    plt.xlabel('x')
    plt.ylabel('y')
    diagram.view.set_figure(plt.gcf())
    img_tosave =plt.gcf()
    ui.button('Save IMG', on_click=saveIMG)


def saveIMG():
    plt.savefig("vector.svg")

def main():

    ui.upload(on_upload=handle_upload)
    ui.run()


main()