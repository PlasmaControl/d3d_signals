import importlib.resources
import yaml
import matplotlib.pyplot as plt
import MDSplus as mds

import d3d_signals

resource_path = importlib.resources.files("d3d_signals")

with open(join(resource_path, "signals_0d.yaml"), "r") as fp:
    signals_1d = yaml.safe_load(fp)


sig_ne = signals_1d["edensfit"]

c = mds.Connection("atlas.gat.com")
c.openTree(sig_ne["tree"], 142111)

zdata = c.get(f"_s={sig_ne['node']}").data()
zunits = c.get("units_of(_s)")

rank = zdata.ndim
# time-base
xdata = c.get("dim_of(_s)")
xunits = c.get("units_of(dim_of(_s))")
ydata = c.get("dim_of(_s, 1)")
yunits = c.get("units_of(dim_of(_s, 1))")
# space-base

#y = c.get(sig_ne['node']).data()
#y_units = c.get(f"""UNITS_OF({sig_ne['node']})""").data()
fig = plt.contourf(xdata, ydata, zdata)
plt.xlabel(xunits)
plt.ylabel(yunits)
plt.colorbar(label=zunits)
plt.title("edensfit (zipfit)")
plt.savefig("ne.png")