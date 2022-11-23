from nicegui import ui
from nicegui.events import UploadEventArguments
import numpy as np
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
from functools import partial
import sys,re,os,csv
from io import StringIO,BytesIO


def handle_upload(e: UploadEventArguments) -> None:
    name = e.names
    content = e.files
    # print(f'{name=}, {len(content)=}', flush=True)    
    global file_name
    global file_content
    file_name = e.names[0]
    file_content = e.files[0]
    print(file_name,type(file_content))
    extract_data(file_name,file_content)


def extract_data(name = 'file_name', file_content =bytes() ):
    # string_content = str(file_content,'utf-8')
    # data = StringIO(string_content )
    # df = pd.read_csv(data)
    df = pd.DataFrame()
    bytes_data = file_content
    if type(name)=='str':
        print(name)
    if 'csv' in name:
        df = pd.read_csv(BytesIO(bytes_data))
    elif 'xls' in name:
        df = pd.read_excel(BytesIO(bytes_data),engine='openpyxl')
    else:
        pass
    
    table = ui.table({})
    table.view.load_pandas_frame(df)

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


def make_plot(x=[],y=[],color='green', marker='o', linestyle='dashed',linewidth=2, markersize=12,alpha=0.5,xlabel='x',ylabel='y'):
    diagram = ui.plot()
    plt.plot(x, y, color=color, marker=marker, linestyle=linestyle,linewidth=linewidth, markersize=markersize,alpha=alpha)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    diagram.view.set_figure(plt.gcf())
    img_tosave =plt.gcf()

    ui.button('Save IMG', on_click=saveIMG)


def saveIMG():
    plt.savefig('vector.svg')
    ui.link('Vector File', 'vector.svg')


def main():

    ui.upload(on_upload=handle_upload)
    ui.run()

main()