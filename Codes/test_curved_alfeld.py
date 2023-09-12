from netgen.occ import *
import ngsolve as ngs
import netgen
from petsc4py import PETSc
from mpi4py import MPI

comm = MPI.COMM_WORLD
if comm.rank == 0:
    shape = Rectangle(2,0.41).Circle(0.2,0.2,0.05).Reverse().Face()
    ngmesh = OCCGeometry(shape,dim=2).GenerateMesh(maxh=0.5)
    mesh = ngs.Mesh(ngmesh)
    mesh.SplitElements_Alfeld()
    ngmesh = mesh.ngmesh
else:
    ngmesh = netgen.libngpy._meshing.Mesh(2)
import firedrake as fd
mesh = fd.Mesh(ngmesh)
mesh = fd.Mesh(mesh.curve_field(3))
fd.File("VTK/curvedAlfeld.pvd").write(mesh)