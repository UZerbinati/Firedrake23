from netgen.occ import *
import netgen
from mpi4py import MPI

comm = MPI.COMM_WORLD
if comm.rank == 0:
    shape = Sphere(Pnt(0,0,0), 1)
    ngmesh = OCCGeometry(shape,dim=3).GenerateMesh(maxh=1.)
else:
    ngmesh = netgen.libngpy._meshing.Mesh(3)
import firedrake as fd
mesh = fd.Mesh(fd.Mesh(ngmesh).curve_field(3))
fd.File("VTK/sphere.pvd").write(mesh)