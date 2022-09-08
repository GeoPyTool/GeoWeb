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
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')  # required, use a non-interactive backend
import io
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


def bkapp(doc,df = sea_surface_temperature.copy()):
    df = df
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


def tas(df = pd.DataFrame()):
    df = df
    
    columns_list= df.columns.tolist()

    Label_list = df['Label'].to_list()
    Color_list = df['Color'].to_list()

    SiO2= df['SiO2(wt%)'].to_list()
    Na2O= df['Na2O(wt%)'].to_list()
    K2O = df['K2O(wt%)'] .to_list()  
    
    Alkali = np.array(Na2O)+np.array(K2O)
    Silica = np.array(SiO2)

    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.scatter(Silica , Alkali)  # Plot some data on the axes.


    title= 'TAS (total alkali–silica) diagram Volcanic/Intrusive (Wilson et al. 1989)'

    xlabel = r'$SiO_2 wt\%$'
    ylabel = r'$Na_2O + K_2O wt\%$'

    itemstocheck = ['SiO2', 'K2O', 'Na2O']
    reference = 'Reference: Maitre, R. W. L., Streckeisen, A., Zanettin, B., Bas, M. J. L., Bonin, B., and Bateman, P., 2004, Igneous Rocks: A Classification and Glossary of Terms: Cambridge University Press, v. -1, no. 70, p. 93–120.'



    ItemNames = ['Foidolite',
                 'Peridotgabbro',
                 'Foid Gabbro',
                 'Foid Monzodiorite',
                 'Foid Monzosyenite',
                 'Foid Syenite',
                 'Gabbro Bs',
                 'Gabbro Ba',
                 'Monzogabbro',
                 'Monzodiorite',
                 'Monzonite',
                 'Syenite',
                 'Quartz Monzonite',
                 'Gabbroic Diorite',
                 'Diorite',
                 'Granodiorite',
                 'Granite',
                 'Quartzolite',
                 ]


    Labels = [u'F', u'Pc', u'U1', u'Ba', u'Bs', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3',
                u'T',
                u'Td', u'R', u'Q', u'T/U/I']

    Locations = [(39, 10), (43, 1.5), (44, 6), (47.5, 3.5), (49.5, 1.5), (49, 5.2), (49, 9.5), (54, 3), (53, 7),
                    (53, 12),
                    (60, 4),
                    (57, 8.5), (57, 14), (67, 5), (65, 12), (67, 9), (75, 9), (85, 1), (55, 18.5)]
    X_offset = -6
    Y_offset = 3


    TagNumber = min(len(Labels), len(Locations))
    for k in range(TagNumber):
        ax.annotate(Labels[k], Locations[k], xycoords='data', xytext=(X_offset, Y_offset), textcoords='offset points',fontsize=9, color='grey', alpha=0.8)


    LocationAreas = [[[41, 3], [37, 3], [35, 9], [37, 14], [52.5, 18], [52.5, 14],  [48.4, 11.5], [45, 9.4], [41, 7]],
                     [[41, 0], [41, 3], [45, 3], [45, 0]],
                     [[41, 3], [41, 7], [45, 9.4], [49.4, 7.3], [45, 5], [45, 3]],
                     [[45, 9.4], [48.4, 11.5], [53, 9.3], [49.4, 7.3]],
                     [[48.4, 11.5], [52.5, 14], [57.6, 11.7], [53, 9.3]],
                     [[52.5, 14], [52.5, 18], [57, 18], [63, 16.2], [61, 13.5], [57.6, 11.7]],
                     [[45, 0], [45, 2], [52, 5], [52, 0]],
                     [[45, 2], [45, 5], [52, 5]],
                     [[45, 5], [49.4, 7.3], [52, 5]],
                     [[49.4, 7.3], [53, 9.3], [57, 5.9], [52, 5]],
                     [[53, 9.3], [57.6, 11.7], [61, 8.6], [63, 7], [57, 5.9]],
                     [[57.6, 11.7], [61, 13.5], [63, 16.2], [71.8, 13.5], [61, 8.6]],
                     [[61, 8.6], [71.8, 13.5], [69, 8], [63, 7]],
                     [[52, 0], [52, 5], [57, 5.9], [57, 0]],
                     [[57, 0], [57, 5.9], [63, 7], [63, 0]],
                     [[63, 0], [63, 7], [69, 8], [77.3, 0]],
                     [[77.3, 0], [69, 8], [71.8, 13.5], [85.9, 6.8], [87.5, 4.7]],
                     [[77.3, 0], [87.5, 4.7], [90, 4.7], [90, 0]],
                     ]


    tas_line_List=[
        [(41, 0), (41, 3), (45, 3)],
        [(45, 0), (45, 3), (45, 5), (49.4, 7.3), (53, 9.3), (57.6, 11.7), (61, 13.5), (63, 16.2)],
        [(52, 5), (57, 5.9), (63, 7), (69, 8), (71.8, 13.5), (61, 8.6)],
        [(45, 2), (45, 5), (52, 5), (45, 2)],
        [(69, 8), (77.3, 0), (87.5, 4.7), (85.9, 6.8), (71.8, 13.5), (63, 16.2), (57, 18), (52.5, 18), (37, 14), (35, 9), (37, 3), (41, 3)],
        [(63, 0), (63, 7), (57.6, 11.7), (52.5, 14), (52.5, 18)],
        [(57, 0), (57, 5.9), (53, 9.3), (48.4, 11.5)],
        [(52, 0), (52, 5), (49.4, 7.3), (45, 9.4)],
        [(41, 3), (41, 7), (45, 9.4)],
        [(45, 9.4), (48.4, 11.5), (52.5, 14)]
        ]

    for k in tas_line_List:
        x = []
        y = []
        for i in k:
            x.append(i[0])
            y.append(i[1])
        ax.plot(x, y, color='grey', alpha=0.8)
    
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.set_xticks([30,40,50,60,70,80,90])
    ax.set_xticklabels([30,40,50,60,70,80,90])

    ax.set_yticks([0, 5, 10, 15, 20])
    ax.set_yticklabels([0, 5, 10, 15, 20])

    # ax.set_xlim(bottom=0)
    # ax.set_ylim(bottom=0)

    buf = io.BytesIO()
    fig.savefig(buf)
    put_image(buf.getvalue())


def main():
    output_notebook(verbose=False, notebook_type='pywebio')
    # if 'zh' in session_info.user_language:pass
    # else:pass
    put_markdown("""# GeoWeb Applications by PyWebIO
        This is based on a [Bokeh Application](https://docs.bokeh.org/en/latest/docs/user_guide/server.html) which can be built by starting the Bokeh server. The purpose of the Bokeh server is to make it easy for Python users to create interactive web applications that can connect front-end UI events to real, running Python code.

        With PyWebIO + Pandas + Bokeh, GeoWeb allow user to upload a csv or excel file and then ploted below.
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

    # show(bkapp)
    tas(df = raw_df)


if __name__ == '__main__':
    start_server(main, port=8080, debug=True)
