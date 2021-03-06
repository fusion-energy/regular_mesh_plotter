from typing import List, Optional

import dagmc_geometry_slice_plotter as dgsp
import matplotlib.pyplot as plt
import numpy as np
import openmc_tally_unit_converter as otuc
from matplotlib import transforms

from .utils import (
    get_std_dev_or_value_from_tally,
    get_tally_extent,
    get_values_from_tally,
    reshape_values_to_mesh_shape,
)


def plot_regular_mesh_values(
    values: np.ndarray,
    filename: Optional[str] = None,
    label="",
    title=None,
    extent=None,
    x_label="X [cm]",
    y_label="Y [cm]",
    rotate_plot: float = 0,
    **kwargs
):

    if rotate_plot != 0:
        x_center = sum(extent[:2]) / 2
        y_center = sum(extent[2:]) / 2
        base = plt.gca().transData
        rot = transforms.Affine2D().rotate_deg_around(x_center, y_center, rotate_plot)

        image_map = plt.imshow(
            values, extent=extent, transform=rot + base, origin="lower", **kwargs
        )
    else:
        image_map = plt.imshow(values, extent=extent, origin="lower", **kwargs)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if title:
        plt.title(title)

    # image_map = fig.imshow(values, norm=scale, vmin=vmin)
    plt.colorbar(image_map, label=label)
    if filename:  # TODO should we not let the users do that?
        plt.savefig(filename, dpi=300)


def plot_regular_mesh_values_with_geometry(
    values: np.ndarray,
    dagmc_file_or_trimesh_object,
    filename: Optional[str] = None,
    label="",
    title=None,
    extent=None,
    x_label="X [cm]",
    y_label="Y [cm]",
    plane_origin: List[float] = None,
    plane_normal: List[float] = [0, 0, 1],
    rotate_mesh: float = 0,
    rotate_geometry: float = 0,
    **kwargs
):

    slice = dgsp.plot_slice_of_dagmc_geometry(
        dagmc_file_or_trimesh_object=dagmc_file_or_trimesh_object,
        plane_origin=plane_origin,
        plane_normal=plane_normal,
        rotate_plot=rotate_geometry,
    )

    plot_regular_mesh_values(
        values=values,
        filename=filename,
        label=label,
        title=title,
        extent=extent,
        x_label=x_label,
        y_label=y_label,
        rotate_plot=rotate_mesh,
        **kwargs
    )


def plot_regular_mesh_tally_with_geometry(
    tally,
    dagmc_file_or_trimesh_object,
    std_dev_or_tally_value="tally_value",
    filename: Optional[str] = None,
    label="",
    title=None,
    x_label="X [cm]",
    y_label="Y [cm]",
    plane_origin: List[float] = None,
    plane_normal: List[float] = [0, 0, 1],
    rotate_mesh: float = 0,
    rotate_geometry: float = 0,
    required_units=None,
    source_strength: float = None,
    **kwargs
):

    if required_units is not None:
        values = otuc.process_tally(
            tally=tally, required_units=required_units, source_strength=source_strength
        )
    else:
        values = get_values_from_tally(tally)

    value = get_std_dev_or_value_from_tally(tally, values, std_dev_or_tally_value)

    extent = get_tally_extent(tally)

    dgsp.plot_slice_of_dagmc_geometry(
        dagmc_file_or_trimesh_object=dagmc_file_or_trimesh_object,
        plane_origin=plane_origin,
        plane_normal=plane_normal,
        rotate_plot=rotate_geometry,
    )

    plot_regular_mesh_values(
        values=value,
        filename=filename,
        label=label,
        title=title,
        extent=extent,
        x_label=x_label,
        y_label=y_label,
        rotate_plot=rotate_mesh,
        **kwargs
    )


def plot_regular_mesh_tally(
    tally,
    filename: Optional[str] = None,
    label="",
    title=None,
    x_label="X [cm]",
    y_label="Y [cm]",
    rotate_plot: float = 0,
    required_units: str = None,
    source_strength: float = None,
    std_dev_or_tally_value="tally_value",
    **kwargs
):

    if required_units is not None:
        values = otuc.process_tally(
            tally=tally, required_units=required_units, source_strength=source_strength
        )
    else:
        values = get_values_from_tally(tally)

    value = get_std_dev_or_value_from_tally(tally, values, std_dev_or_tally_value)

    value = reshape_values_to_mesh_shape(tally, value)

    extent = get_tally_extent(tally)

    plot_regular_mesh_values(
        values=value,
        filename=filename,
        label=label,
        title=title,
        extent=extent,
        x_label=x_label,
        y_label=y_label,
        rotate_plot=rotate_plot,
        **kwargs
    )


def plot_regular_mesh_dose_tally(
    tally,
    filename: Optional[str] = None,
    label="",
    title=None,
    x_label="X [cm]",
    y_label="Y [cm]",
    rotate_plot: float = 0,
    required_units="picosievert / source_particle",
    source_strength: float = None,
    std_dev_or_tally_value: str = "tally_value",
    **kwargs
):

    if required_units is not None:
        values = otuc.process_dose_tally(
            tally=tally, required_units=required_units, source_strength=source_strength
        )
    else:
        values = get_values_from_tally(tally)

    value = get_std_dev_or_value_from_tally(tally, values, std_dev_or_tally_value)

    value = reshape_values_to_mesh_shape(tally, value)

    extent = get_tally_extent(tally)

    plot_regular_mesh_values(
        values=value,
        filename=filename,
        label=label,
        title=title,
        extent=extent,
        x_label=x_label,
        y_label=y_label,
        rotate_plot=rotate_plot,
        **kwargs
    )


def plot_regular_mesh_dose_tally_with_geometry(
    tally,
    dagmc_file_or_trimesh_object,
    filename: Optional[str] = None,
    label="",
    title=None,
    x_label="X [cm]",
    y_label="Y [cm]",
    plane_origin: List[float] = None,
    plane_normal: List[float] = [0, 0, 1],
    rotate_mesh: float = 0,
    rotate_geometry: float = 0,
    required_units="picosievert / source_particle",
    source_strength: float = None,
    std_dev_or_tally_value: str = "tally_value",
    **kwargs
):

    dgsp.plot_slice_of_dagmc_geometry(
        dagmc_file_or_trimesh_object=dagmc_file_or_trimesh_object,
        plane_origin=plane_origin,
        plane_normal=plane_normal,
        rotate_plot=rotate_geometry,
    )

    plot_regular_mesh_dose_tally(
        tally=tally,
        filename=filename,
        label=label,
        title=title,
        x_label=x_label,
        y_label=y_label,
        rotate_plot=rotate_mesh,
        required_units=required_units,
        source_strength=source_strength,
        std_dev_or_tally_value=std_dev_or_tally_value,
        **kwargs
    )
