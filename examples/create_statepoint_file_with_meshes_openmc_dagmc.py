# This minimal example makes a 3D volume and exports the shape to a stp file
# A surrounding volume called a graveyard is needed for neutronics simulations

import openmc
import openmc_dagmc_wrapper as odw
import openmc_plasma_source as ops
from stl_to_h5m import stl_to_h5m
from dagmc_bounding_box import DagmcBoundingBox

# code used to create example.stl
# import paramak
# my_shape = paramak.ExtrudeStraightShape(
#     points=[(1, 1), (1, 200), (600, 200), (600, 1)],
#     distance=180,
# )
# my_shape.export_stl("example.stl")

# This script converts the CAD stl files generated into h5m files that can be
# used in DAGMC enabled codes. h5m files created in this way are imprinted,
# merged, faceted and ready for use in OpenMC. One of the key aspects of this
# is the assignment of materials to the volumes present in the CAD files.

stl_to_h5m(
    files_with_tags=[("example.stl", "mat1")],
    h5m_filename="dagmc.h5m",
)

my_corners = DagmcBoundingBox("dagmc.h5m").corners()

# makes use of the previously created neutronics geometry (h5m file) and assigns
# actual materials to the material tags. Sets simulation intensity and specifies
# the neutronics results to record (know as tallies).

geometry = odw.Geometry(
    h5m_filename="dagmc.h5m",
)

materials = odw.Materials(
    h5m_filename="dagmc.h5m", correspondence_dict={"mat1": "FLiNaK"}
)

tally1 = odw.MeshTally2D(
    tally_type="neutron_effective_dose",
    plane="xy",
    mesh_resolution=(10, 5),
    bounding_box=my_corners,
)
tally2 = odw.MeshTally2D(
    tally_type="neutron_effective_dose",
    plane="yz",
    mesh_resolution=(10, 5),
    bounding_box=my_corners,
)
tally3 = odw.MeshTally2D(
    tally_type="neutron_effective_dose",
    plane="xz",
    mesh_resolution=(10, 5),
    bounding_box=my_corners,
)
tally4 = odw.MeshTally2D(
    tally_type="neutron_effective_dose",
    plane="xy",
    mesh_resolution=(10, 10),
    bounding_box=my_corners,
)
tally5 = odw.MeshTally2D(
    tally_type="neutron_effective_dose",
    plane="yz",
    mesh_resolution=(10, 5),
    bounding_box=my_corners,
)
tally6 = odw.MeshTally2D(
    tally_type="neutron_effective_dose",
    plane="xz",
    mesh_resolution=(10, 5),
    bounding_box=my_corners,
)

# tally2 = odw.MeshTally3D(
#     mesh_resolution=(100, 100, 100),
#     bounding_box=my_corners,
#     tally_type="neutron_effective_dose",
# )

tallies = openmc.Tallies(
    [
        tally1,
        tally2,
        tally3,
        tally4,
        tally5,
        tally6,
    ]
)

settings = odw.FusionSettings()
settings.batches = 2
settings.particles = 1000
# assigns a ring source of DT energy neutrons to the source using the
# openmc_plasma_source package
settings.source = ops.FusionPointSource()


my_model = openmc.Model(
    materials=materials, geometry=geometry, settings=settings, tallies=tallies
)
statepoint_file = my_model.run()
