[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)

[![CI with install](https://github.com/fusion-energy/regular_mesh_plotter/actions/workflows/ci_with_install.yml/badge.svg?branch=develop)](https://github.com/fusion-energy/regular_mesh_plotter/actions/workflows/ci_with_install.yml)

[![PyPI](https://img.shields.io/pypi/v/regular-mesh-plotter?color=brightgreen&label=pypi&logo=grebrightgreenen&logoColor=green)](https://pypi.org/project/regular-mesh-plotter/)

[![codecov](https://codecov.io/gh/fusion-energy/regular_mesh_plotter/branch/main/graph/badge.svg)](https://codecov.io/gh/fusion-energy/regular_mesh_plotter)

## A minimal Python package that plots 2D mesh tally results with the underlying DAGMC geometry

# Installation

```bash
pip install regular_mesh_plotter
```

Mesh results in the form of at OpenMC.tally objects can be plotted with a single API call.

A Matplotlib.pyplot object is returned by all functions so one can make changes
to the legend, axis, colour map etc. However some key options are accessible
in the function call directly.

There are additional options that allow

- rotation of the mesh tally results
- rotation of the DAGMC geometry slice
- saving the plot as an image file
- specifying contour lines TODO
- changing axis and colour bar labels
- changing colour scale applied
- truncation of values
- The plane_normal of the DAGMC geometry

The resulting plots can be used to show dose maps, activation, reaction rate
and other mesh tally results.

The examples below require a mesh tally that can be read in with OpenMC in the following way.

```python
import openmc

# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name="neutron_effective_dose_on_2D_mesh_xy")
```

Example 1 shows a OpenMC tally plotted
```python

import regular_mesh_plotter as rmp
import matplotlib.pyplot as plt

rmp.plot_regular_mesh_tally(
    tally=my_tally,
    std_dev_or_tally_value="tally_value",
    x_label="X [cm]",
    y_label="Y [cm]",
)

plt.savefig('openmc_mesh_tally_plot.png')
```

Example 4 shows a OpenMC tally plotted with an underlying DAGMC geometry
```python
plot_regular_mesh_tally_with_geometry(
    tally=my_tally,
    dagmc_file_or_trimesh_object='dagmc.h5m',
    std_dev_or_tally_value="tally_value",
    x_label="X [cm]",
    y_label="Y [cm]",
)
```

Example 5 shows how to rotate the underlying DAGMC geometry and mesh tally.
This is sometimes necessary as the slice and mesh can get out of alignment
when changing the plane normal
```python
plot_regular_mesh_tally_with_geometry(
    tally,
    dagmc_file_or_trimesh_object,
    std_dev_or_tally_value="tally_value",
    filename: Optional[str] = None,
    scale=None,  # LogNorm(),
    vmin=None,
    label="",
    x_label="X [cm]",
    y_label="Y [cm]",
    plane_origin: List[float] = None,
    plane_normal: List[float] = [0, 0, 1],
    rotate_mesh: float = 0,
    rotate_geometry: float = 0,
    required_units=None,
    source_strength: float = None,
)
```

Example 6 shows how to plot a dose tally with the underlying DAGMC geometry.
This also includes unit conversion from the base tally units to the requested
units.
```python
plot_regular_mesh_dose_tally_with_geometry(
    tally,
    dagmc_file_or_trimesh_object,
    filename: Optional[str] = None,
    scale=None,  # LogNorm(),
    vmin=None,
    label="",
    x_label="X [cm]",
    y_label="Y [cm]",
    plane_origin: List[float] = None,
    plane_normal: List[float] = [0, 0, 1],
    rotate_mesh: float = 0,
    rotate_geometry: float = 0,
    required_units="picosievert / source_particle",
    source_strength: float = None,
    std_dev_or_tally_value: str = "tally_value",
):
```

Additional examples can be found in the [examples folder in the GitHub repository](https://github.com/fusion-energy/regular_mesh_plotter/tree/main/examples)

# Related packages

If you want to plot the DAGMC geometry without a mesh tally then take a look at
the [dagmc_geometry_slice_plotter](https://github.com/fusion-energy/dagmc_geometry_slice_plotter) package
