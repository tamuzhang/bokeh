#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 19:19:19 2018

@author: shuaizhang
"""

from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource,GMapOptions,LinearColorMapper,ColorBar, Whisker
from bokeh.plotting import figure, output_file, show
from bokeh.plotting import gmap,curdoc
import re
import pandas as pd
from bokeh.palettes import Viridis256


def load_data(lake_id):
    fname = '../data/'+str(lake_id)+'_dates_bue_1.csv'
    data = pd.read_csv(fname)
    return data

map_options = GMapOptions(lat=71.25, lng=-156.5, map_type="terrain", zoom=5)
name_bue = r'../data/bue_small_1_copy.csv'
lat = []
lon=[]
bue_day=[]
fus_day=[]
bue_uc=[]
fus_uc=[]
bue_p=[]
bue_id = []


fin_bue = open(name_bue,'r')
line_tmp = fin_bue.readline()
while line_tmp:
    line_tmp = line_tmp.replace(',',' ')
    list_tmp = re.split('[ ]',line_tmp)
    lat.append(float(list_tmp[2]))
    lon.append(float(list_tmp[4]))
    bue_day.append(float(list_tmp[6]))
    bue_uc.append(float(list_tmp[8]))
    bue_p.append(float(list_tmp[7]))
    line_tmp = fin_bue.readline()
    bue_id.append(int(list_tmp[0]))
fin_bue.close()

x = lon
y = lat
z = bue_id

mapper = LinearColorMapper(palette=Viridis256, low=-1, high=1)
s1 = ColumnDataSource(data=dict(x=x, y=y,z=z,bue_day = bue_day))
p1 = figure(plot_width=400, plot_height=400, tools="lasso_select", title="Select Here")
p1 = gmap("AIzaSyDvmp13WTFUXKEPLlYKV8rp8EoHIw73Q30&language=en", map_options, title="Trends of lake breakup dates in Alaska (days/year)",tools = "wheel_zoom,pan,lasso_select,tap")
p1.circle('x', 'y', source=s1, alpha=0.9,fill_color={'field': 'bue_day', 'transform': mapper},line_color=None)
color_bar = ColorBar(color_mapper=mapper,location=(5,5),label_standoff=12, border_line_color=None,)
p1.add_layout(color_bar,'right')
#p1.circle('x', 'y', source=s1, alpha=0.9,fill_color={'field': 'bue_day', 'transform': mapper},line_color=None)
#color_bar = ColorBar(color_mapper=mapper)

s2 = ColumnDataSource(data=dict(Type = [], Year=[], Days=[],UC=[]))
p2 = figure(plot_width=400, plot_height=300,tools="", title="Breakup dates (day of year)")
p2.line('Year', 'Days', source=s2, alpha=0.9)

s3 = ColumnDataSource(data=dict(x=[], yerr=[]))
p2.multi_line('x','yerr',source=s3,color='red',legend = 'Uncertainty')
p2.legend.location = "top_left"
p2.xaxis.axis_label = 'Year'
p2.yaxis.axis_label = 'Breakup dates'


def selection_change(attrname, old, new):
    data = s1.data
    selected = s1.selected['1d']['indices']
    a = (data['z'][selected[0]])
    data_bue = load_data(a)
    s2.data = s2.from_df(data_bue[['Type', 'Year', 'Days', 'UC']])
    s3.data['base'] = s2.data['Days'].tolist()
    a = s2.data['Days']
    b = s2.data['UC']
    s3.data['x'] = zip(s2.data['Year'],s2.data['Year'])
    s3.data['yerr'] = zip([x - y for x, y in zip(a,b)],[x + y for x, y in zip(a,b)])


s1.on_change('selected', selection_change)

layout = gridplot([p1],[p2])

curdoc().add_root(layout)
#show(layout)
