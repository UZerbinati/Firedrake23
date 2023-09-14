from netgen.occ import *
import netgen
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
if comm.rank == 0:
    shape = Sphere(Pnt(0,0,0), 1)
    ngmesh = OCCGeometry(shape,dim=3).GenerateMesh(maxh=1.)
else:
    ngmesh = netgen.libngpy._meshing.Mesh(3)
import firedrake as fd
mesh = fd.Mesh(fd.Mesh(ngmesh).curve_field(3))
fd.File("VTK/sphere.pvd").write(u)
x, y, z = fd.SpatialCoordinate(mesh)
V = fd.FunctionSpace(mesh, "CG", 3)
f = fd.Function(V).interpolate(x)
#Solve the Poisson problem
f.interpolate(1+0*x)
u = fd.TrialFunction(V)
v = fd.TestFunction(V)
a = fd.inner(fd.grad(u), fd.grad(v)) * fd.dx
l = fd.inner(f, v) * fd.dx

print("Problem Seted Up !")
u = fd.Function(V)

bc = fd.DirichletBC (V , 0.0 , [1,2,3,4]) # Boundary condition
print("Assembling ...")
A = fd.assemble (a , bcs = bc)
b = fd.assemble (l)
bc.apply(b)
print("Assembled !")
print("Solving ...")
fd.solve (A, u, b, solver_parameters ={"ksp_type": "cg", "pc_type": "none"})

fd.File("VTK/sphere.pvd").write(u)