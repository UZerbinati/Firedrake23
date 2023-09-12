import ngsolve as ngs
from netgen.occ import *
import netgen
from mpi4py import MPI

comm = MPI.COMM_WORLD
if comm.rank == 0:
    cyl= Cylinder((0,0,0), Z, r=1, h=3)
    cyl.edges.Max(Z).hpref=1
    geo = OCCGeometry(cyl)
    mesh = ngs.Mesh(geo.GenerateMesh(maxh=0.4))
    mesh.RefineHP(2)
    ngmesh = mesh.ngmesh
else:
    ngmesh = netgen.libngpy._meshing.Mesh(3)
import firedrake as fd
mesh = fd.Mesh(ngmesh,netgen_flags={"purify_to_tets": True})
fd.File("VTK/CylinderEdge.pvd").write(mesh)