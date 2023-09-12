from netgen.geom2d import *
import netgen
from mpi4py import MPI

comm = MPI.COMM_WORLD
if comm.rank == 0:
    geo = CSG2d()
    circle = Circle(center=(1,1), radius=0.1, bc="curve").Maxh(0.01)
    rect = Rectangle(pmin=(0,1), pmax=(1,2), bottom="bottom", left="left", top="top", right="right")
    geo.Add(rect-circle)
    ngmesh = geo.GenerateMesh(maxh=0.2)
else:
    ngmesh = netgen.libngpy._meshing.Mesh(2)
import firedrake as fd
mesh = fd.Mesh(fd.Mesh(ngmesh).curve_field(3))
fd.File("VTK/plate.pvd").write(mesh)