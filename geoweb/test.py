from bokeh.io import output_notebook
from bokeh.io import show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from functools import partial
from os import path, listdir

import time  # lgtm [py/unused-import]
import json
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
from pywebio_battery import *
from pywebio import start_server
from pywebio.platform import config
from pywebio.session import local as session_local, info as session_info
import pandas as pd
import numpy as np


# Adaped frome PyWebIO's official Demo of bokeh_app.py, input_usage and doc_demo.py .
def t(eng, chinese):
    """return English or Chinese text according to the user's browser language"""
    return chinese if 'zh' in session_info.user_language else eng


here_dir = path.dirname(path.abspath(__file__))


def bkapp(doc):
    df = sea_surface_temperature.copy()
    source = ColumnDataSource(data=df)

    plot = figure(x_axis_type='datetime', y_range=(0, 25),
                  y_axis_label='Temperature (Celsius)',
                  title="Sea Surface Temperature at 43.18, -70.43")
    plot.line('time', 'temperature', source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            data = df.rolling('{0}D'.format(new)).mean()
        source.data = ColumnDataSource.from_df(data)

    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change('value', callback)

    doc.add_root(column([slider, plot], sizing_mode='stretch_width'))




def main():

    output_notebook(verbose=False, notebook_type='pywebio')

    if 'zh' in session_info.user_language:
        put_markdown("""# Bokeh Applications in PyWebIO
        [Bokeh Applications](https://docs.bokeh.org/en/latest/docs/user_guide/server.html) 支持向图表的添加按钮、输入框等交互组件，并向组件添加Python回调，从而创建可以与Python代码交互的可视化图表。

        在PyWebIO中，你也可以使用 `bokeh.io.show()` 来显示一个Bokeh App，和输出普通图表一样，只需要在会话开始时调用 `bokeh.io.output_notebook(notebook_type='pywebio')` 来设置PyWebIO输出环境。

        以下为一个 Bokeh App demo:
        """)
    else:
        put_markdown("""# Bokeh Applications in PyWebIO
        [Bokeh Applications](https://docs.bokeh.org/en/latest/docs/user_guide/server.html) can be built by starting the Bokeh server. The purpose of the Bokeh server is to make it easy for Python users to create interactive web applications that can connect front-end UI events to real, running Python code.

        In PyWebIO, you can also use bokeh.io.show() to display a Bokeh App.

        You can use `bokeh.io.output_notebook(notebook_type='pywebio')` in the PyWebIO session to setup Bokeh environment. Then you can use `bokeh.io.show()` to output a boken application.

        This is a demo of Bokeh App: 
        """)

    # Upload a file and save to server                      
    f = file_upload("Upload a file")                  
    open('asset/'+f['filename'], 'wb').write(f['content'])     
    
    raw_df=pd.DataFrame()

    if ('csv' in f['filename']):
        raw_df= pd.read_csv('asset/'+f['filename'], engine='python')
    elif ('xls' in f['filename']):
        raw_df= pd.read_excel('asset/'+f['filename'],engine='openpyxl')

    print(len(raw_df),'\n')
    if(len(raw_df)>0):
        res_table = put_html(raw_df.to_html(classes='table table-stripped',justify = 'center'))
        put_scrollable( res_table ,horizon_scroll=True,vertical_scroll=True,height=450)


    # imgs = file_upload("Select some pictures:", accept="image/*", multiple=True)
    # for img in imgs:
    #     put_image(img['content'])


    show(bkapp)


if __name__ == '__main__':
    start_server(main, port=8080, debug=True)
