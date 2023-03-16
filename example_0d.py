# -*- coding: utf-8 -*-


import importlib.resources
import yaml
import matplotlib.pyplot as plt
import MDSplus as mds

import d3d_signals

resource_path = importlib.resources.files("d3d_signals")

with open(join(resource_path, "signals_0d.yaml"), "r") as fp:
    signals_0d = yaml.safe_load(fp)

sig_pinj = signals_0d["pinj"]

c = mds.Connection("atlas.gat.com")
c.openTree(sig_pinj["tree"], 142111)

z = c.get(f"_s={sig_pinj['node']}").data()
z_units = c.get("units_of(dim_of(_s))")

x = c.get(sig_pinj['node']).dim_of().data()
x_units = c.get(f"""UNITS_OF({sig_pinj['node']})""").data()
plt.plot(x, z)
plt.xlabel(x_units)
plt.ylabel(z_units)
plt.title("pinj")
plt.savefig("pinj.png")

# end of file example.py
