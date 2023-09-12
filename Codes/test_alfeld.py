from netgen.occ import *
import netgen
from petsc4py import PETSc
from mpi4py import MPI

comm = MPI.COMM_WORLD
if comm.rank == 0:
    shape = Rectangle(2,0.41).Circle(0.2,0.2,0.05).Reverse().Face()
    ngmesh = OCCGeometry(shape,dim=2).GenerateMesh(maxh=0.5)
else:
    ngmesh = netgen.libngpy._meshing.Mesh(2)
import firedrake as fd
transform = PETSc.DMPlexTransform().create(comm=PETSc.COMM_WORLD)
transform.setType(PETSc.DMPlexTransformType.REFINEALFELD)
mesh = fd.Mesh(ngmesh,netgen_flags={"transform":transform})
mesh = fd.Mesh(mesh.curve_field(3))
fd.File("VTK/alfeld.pvd").write(mesh)