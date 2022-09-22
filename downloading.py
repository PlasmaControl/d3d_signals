# -*- coding: utf-8 -*-

"""Example script to download MDSplus / PTDATA 

This script downloads a list of signals for a given shot.
The data is stored in HDF5 format with a layout compatible
with the data loading logic of the d3d loader."""

import h5py
import MDSplus as mds
import numpy as np
import os
from os.path import join

import logging


import yaml

# Set the environment variable to connect to the correct MDS server
# 
os.environ["main_path"] = "atlas.gat.com::"

# List of shots, taken from https://nomos.gat.com/DIII-D/physics/miniprop/mp_list.php?mpid=2017-24-89
shot_list = [178631]

# List of diagnostics to fetch. These are taken from https://doi.org/10.1088/1741-4326/abe08d (Abbate et al. 2021)
# and the path names are collected in https://nomos.gat.com/DIII-D/physics/miniprop/mp_list.php?mpid=2017-24-89

# Separate between three kinds of data. Each kind requires separate download logic, 
# to pull from from either MDS or PTDATA, and handle 0d vs 1d
# The first kind are profiles. These are 1d time series.
# Each entry is a dict with 
#   Tree - The name of the MDS tree the data is stored in
#   Node - The name of the MDS node the data is stored in
#   map_to - The group in the HDF5 file the data will be stored in

with open("signals_1d.yaml", "r") as stream:
    profile_dict = yaml.safe_load(stream)

# The second kind are scalar time series, i.e. 0d time series.
# Each entry is a dict with 
#   Tree - The name of the MDS tree the data is stored in
#   Node - The name of the MDS node the data is stored in
#   map_to - The group in the HDF5 file the data will be stored in
with open("signals_0d.yaml", "r") as stream:
    scalars_dict = yaml.safe_load(stream)

data_path = "/projects/EKOLEMEN/d3dloader/test"
for shotnr in shot_list:
    print(shotnr)
    log_fname = join(data_path, f"d3d_signal_{shotnr}.log")
    logging.basicConfig(filename=log_fname, 
                        format="%(asctime)s    %(message)s",
                        encoding="utf-8", 
                        level=logging.INFO)

    conn = mds.Connection("atlas.gat.com")

    # File mode needs to be append! Otherwise we delete the file contents every time we
    # execute this script.
    with h5py.File(join(data_path, f"{shotnr}.h5"), "a") as df:
        assert(df.mode == "r+")
        # Handle each of the three data kinds separately.
        # First profile data
        for key in profile_dict.keys():
            tree = profile_dict[key]["tree"]
            node = profile_dict[key]["node"]
            map_to = profile_dict[key]["map_to"]

            try:
                if df[map_to]["zdata"].size > 0:
                    logging.info(f"Signal {map_to} already exists. Skipping download")
                    continue
            except KeyError as err:
                pass

            try:
                logging.info(f"Trying to download {tree}::{node} from MDS")
                conn.openTree(tree, shotnr)
                zdata = conn.get(f"_s ={node}").data()
                zunits = conn.get('units_of(_s)').data()
                logging.info(f"Downloaded zdata. shape = {zdata.shape}, units = {zunits}")

                xdata = conn.get('dim_of(_s)').data()
                xunits = conn.get('units_of(dim_of(_s))').data()
                if zunits in ["", " "]:
                    xunits = conn.get('units(dim_of(_s))').data()
                logging.info(f"Downloaded xdata. shape = {xdata.shape}, units = {xunits}")

                ydata = conn.get('dim_of(_s,1)').data()
                yunits = conn.get('units_of(dim_of(_s,1))').data()
                if yunits in ["", " "]:
                    yunits = conn.get('units(dim_of(_s))').data()

                logging.info(f"Downloaded ydata. shape = {ydata.shape}, units = {yunits}")
            except Exception as err:
                logging.error(f"Failed to download {tree}::{node} from MDS: {err}")
                continue
            # The data is downloaded now. Next store them in HDF5
            try:
                grp = df.create_group(map_to)
                grp.attrs.create("origin", f"MDS {tree}::{node}")
                # Store data in arrays and set units as an attribute
                for ds_name, ds_data, u_name, u_data in zip(["xdata", "ydata", "zdata"],
                                                            [xdata, ydata, zdata],
                                                            ["xunits", "yunits", "zunits"],
                                                            [xunits, yunits, zunits]):
                    dset = grp.create_dataset(ds_name, ds_data.shape, dtype='f')
                    dset[:] = ds_data[:]
                    dset.attrs.create(u_name, u_data.encode())
            
            except Exception as err:
                logging.error(f"Failed to write {tree}::{node} to HDF5 group {grp} - {err}")
                raise(err)
            
            logging.info(f"Stored {tree}::{node} into {grp}")

        # Second scalar data
        for key in scalars_dict.keys():
            if scalars_dict[key]["type"] == "MDS":
                tree = scalars_dict[key]["tree"]
                node = scalars_dict[key]["node"]
                map_to = scalars_dict[key]["map_to"]

                # Skip the download if there already is data in the HDF5 file
                try:
                    if df[map_to]["zdata"].size > 0:
                        logging.info(f"Signal {map_to} already exists. Skipping download")
                        continue
                except KeyError:
                    pass

                try:
                    logging.info(f"Trying to download {tree}::{node} from MDS")
                    conn.openTree(tree, shotnr)

                    zdata = conn.get(f"_s ={node}").data()
                    zunits = conn.get('units_of(_s)').data()
                    logging.info(f"Downloaded zdata. shape={zdata.shape}")

                    xdata = conn.get('dim_of(_s)').data()
                    xunits = conn.get('units_of(dim_of(_s))').data()
                    logging.info(f"Downloaded xdata. shape={xdata.shape}")
                except Exception as err:
                    logging.error(f"Failed to download {tree}::{node} from MDS - {err}")
                    continue
                
                # Data is now downloaded. Store them in HDF5
                try:
                    grp = df.create_group(map_to)
                    grp.attrs.create("origin", f"MDS {tree}::{node}")
                    # Store data in arrays and set units as an attribute
                    for ds_name, ds_data, u_name, u_data in zip(["xdata", "zdata"],
                                                                [xdata, zdata],
                                                                ["xunits", "zunits"],
                                                                [xunits, zunits]):
                        dset = grp.create_dataset(ds_name, ds_data.shape, dtype='f')
                        dset[:] = ds_data[:]
                        dset.attrs.create(u_name, u_data.encode())      
                except Exception as err:
                    logging.error(f"Failed to write {tree}::{node} to HDF5 group {grp} - {err}")
                    raise(err)
                
                logging.info(f"Stored {tree}::{node} into {grp}")

            elif scalars_dict[key]["type"] == "PTDATA":

                # Finally PTDATA
                for key in scalars_dict.keys():
                    node = scalars_dict[key]["node"]
                    map_to = scalars_dict[key]["map_to"]
                    # Skip the download if there already is data in the HDF5 file
                    try:
                        if df[map_to]["zdata"].size > 0:
                            logging.info(f"Signal {map_to} already exists. Skipping download")
                            continue
                    except KeyError:
                        pass

                    try:
                        logging.info(f"Trying to download {node} from PTDATA")
                        zdata = conn.get(f"_s = ptdata2('{node}', {shotnr})").data()
                        xdata = conn.get("dim_of(_s)")
                        logging.info(f"Downloaded zdata. shape={zdata.shape}")
                        logging.info(f"Downloaded xdata. shape={xdata.shape}")
                    except Exception as err:
                        logging.error(f"Failed to download {node} from PTDATA - {err}")
                        continue

                    # Data is downloaded. Store them in HDF5
                    try:
                        grp = df.create_group(f"{scalars_dict[key]['map_to']}")
                        grp.attrs.create("origin", f"PTDATA {node}")
                        for ds_name, ds_data in zip(["xdata", "zdata"],
                                                    [xdata, zdata]):
                            dset = grp.create_dataset(ds_name, ds_data.shape, dtype='f')
                            dset[:] = ds_data[:]
                    except Exception as err:
                        logging.error(f"Failed to write {node} to HDF5 group {grp} - {err}")
                        raise(err)
                    
                    logging.info(f"Stored PTDATA {node} into {grp}")


# end of file downloading.py
