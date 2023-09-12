from netgen.occ import *
import netgen
from mpi4py import MPI

comm = MPI.COMM_WORLD
wp = WorkPlane()
if comm.rank == 0:
    for i in range(6):
        wp.Line(0.6).Arc(0.4, 60)
    shape = wp.Face()
    ngmesh = OCCGeometry(shape,dim=2).GenerateMesh(maxh=1.)
else:
    ngmesh = netgen.libngpy._meshing.Mesh(2)
import firedrake as fd
mesh = fd.Mesh(fd.Mesh(ngmesh).curve_field(3))
fd.File("VTK/wp.pvd").write(mesh)