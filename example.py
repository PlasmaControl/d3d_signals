# -*- coding: utf-8 -*-

import yaml
import MDSplus as mds
import matplotlib.pyplot as plt


with open("signals_0d.yaml", "r") as stream:
    signal_defs_0d = yaml.safe_load(stream)

signal_pinj = signal_defs_0d["pinj"]

c = mds.Connection("atlas.gat.com")
c.openTree("d3d", 142111)

x = c.get(f"DIM_OF({signal_pinj['node']})")
y = c.get(f"{signal_pinj['node']}")

plt.plot(x, y)

# end of file example.py
