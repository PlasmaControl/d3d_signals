# -*- coding: utf-8 -*-

import yaml
import MDSplus as mds
import matplotlib.pyplot as plt


with open("signals_0d.yaml", "r") as stream:
    signal_defs_0d = yaml.safe_load(stream)

signal_pinj = signal_defs_0d["pinj"]

c = mds.Connection("atlas.gat.com")
c.openTree("d3d", 142111)

x = c.get(signal_pinj['node']).dim_of().data()
x_units = c.get(signal_pinj['node']).dim_of().units_of().data()
if x_units == " ":
    x_units = "ms"

y = c.get(signal_pinj['node']).data()
y_units = c.get(f"""UNITS_OF({signal_pinj['node']})""").data()
plt.plot(x, y)
plt.xlabel(x_units)
plt.ylabel(y_units)
plt.title("pinj")

# end of file example.py
