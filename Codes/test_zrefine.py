from netgen.csg import *
import netgen
from mpi4py import MPI

comm = MPI.COMM_WORLD
if comm.rank == 0:
    geo = CSGeometry()
    box = OrthoBrick(Pnt(0,0,0),Pnt(1,1,1))
    top = Plane(Pnt(0,0,0.52),Vec(0,0,1))
    bot = Plane(Pnt(0,0,0.48),Vec(0,0,-1))
    plate = box * top * bot
    geo.Add((box-top).mat("air"))
    geo.Add(plate.mat("plate"))
    geo.Add((box-bot).mat("air"))
    slices = [2**(-i) for i in reversed(range(1,6))]
    geo.CloseSurfaces(bot,top,slices)
    ngmesh = geo.GenerateMesh(maxh=0.3)
    ZRefinement(ngmesh,geo)
else:
    ngmesh = netgen.libngpy._meshing.Mesh(3)
import firedrake as fd
mesh = fd.Mesh(ngmesh,netgen_flags={"purify_to_tets": True})
fd.File("VTK/ZRefine.pvd").write(mesh)