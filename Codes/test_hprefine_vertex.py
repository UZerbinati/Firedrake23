import ngsolve as ngs
from netgen.occ import *
import netgen
from mpi4py import MPI

comm = MPI.COMM_WORLD
if comm.rank == 0:
    cube = Box((0,0,0), (1,1,1))
    cube.vertices.Max(X+Y+Z).hpref=3
    cube.vertices.Max(X+Y-Z).hpref=3
    geo = OCCGeometry(cube)
    mesh = ngs.Mesh(geo.GenerateMesh(maxh=0.4))
    mesh.RefineHP(2)
    ngmesh = mesh.ngmesh
else:
    ngmesh = netgen.libngpy._meshing.Mesh(3)
import firedrake as fd
mesh = fd.Mesh(ngmesh,netgen_flags={"purify_to_tets": True})
fd.File("VTK/CylinderVertex.pvd").write(mesh)