Illustris Python for Zoom-in Simulations
========================================

This is a modified version of the illustris_python package originally prepared for the Illustris and IllustrisTNG project.
See the [Illustris Website Data Access Page](http://www.illustris-project.org/data/) for details.

This updated version is prepared for the new generation of zoom-in simulations with similar architecture as the original Illustris project. 
These simulations include the Thesan-Zoom simulations, the Variant project, and the MIRACLE project.
We have included some useful functions to allow fast visualizations and analysis of galaxy properties in zoom-in simulations.

Requirements
------------
Please upgrade to `python3` to use.

### Python packages
+ `numpy`, required for the core numerical routines.
+ `h5py`, required for reading HDF5 output files.
+ `six`

### Optional
+ `swiftsimio`, required in the future for imaging tools.
+ `numba`

Installing
----------
```
git clone git@github.com:XuejianShen/illustris_python_zoom.git
cd illustris_python_zoom
pip install .
```

Citing
------
Information to be included.
