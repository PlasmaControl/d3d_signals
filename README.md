# D3D signals
Defines mapping of D3D MDS/PTdata signals to local storage on PU systems as yaml files

These definitions come in handy when we want to work with D3D signals and require 
* A handy way of accessing them, for example in a locally cached data file
* Quickly pulling data from MDS or PTDATA without having to remember where this data is stored

The signals used in the repository can be used like this:
```python
import yaml
import MDSplus as mds
import matplotlib.pyplot as plt


with open("signals_0d.yaml", "r") as stream:
    signal_defs_0d = yaml.safe_load(stream)

signal_pinj = signal_defs_0d["pinj"]

c = mds.Connection("atlas.gat.com")
c.openTree("d3d", 142111)

x = c.get(sig_pinj['node']).dim_of().data()
x_units = c.get(sig_pinj['node']).dim_of().units_of().data()
if x_units == " ":
    x_units = "ms"

y = c.get(sig_pinj['node']).data()
y_units = c.get(f"""UNITS_OF({sig_pinj['node']})""").data()
plt.plot(x, y)
plt.xlabel(x_units)
plt.ylabel(y_units)
plt.title("pinj")
```

![Result](pinj.png)

The [d3d_loader](https://github.com/PlasmaControl/d3d_loaders/tree/main/d3d_loaders) repository
uses the signal nodes and `map_to` values to load the MDS signals in locally cached hdf5 files.

To create such a cache, use the `downloading.py` script provided in this repository.



