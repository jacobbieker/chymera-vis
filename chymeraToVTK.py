__author__ = 'jacob'
import pyvtk, math, os
from glob import glob
import numpy
#import visit_writer

filename = 'chymera_data.vtk'
title = 'Test CHYMERA Output'


NX = 256
NZ = 66
NY = 128


def BlendPoint(A, B, t):
    return [(1. - t) * A[0] + t * B[0], (1. - t) * A[1] + t * B[1], (1. - t) * A[2] + t * B[2]]


def GetMeshPoints(angle, angle2):
    p = []
    for k in range(NZ):
        z = float(k) / float(NZ - 1)
        for j in range(NY):
            y = float(j) / float(NY - 1)
            for i in range(NX):
                x = float(i) / float(NX - 1)
                A = [y * math.cos(angle), y * math.sin(angle), z]
                B = [y * math.cos(angle2), y * math.sin(angle2), z]
                p += BlendPoint(A, B, x)
    return p


def GetMeshConnectivity():
    c = []
    for k in range(NZ - 1):
        for j in range(NY - 1):
            for i in range(NX - 1):
                # Make a hole
                if i == 1 and j == 2:
                    continue

                i0 = k * NY * NX + j * NX + i
                i1 = k * NY * NX + j * NX + (i + 1)
                i2 = k * NY * NX + (j + 1) * NX + (i + 1)
                i3 = k * NY * NX + (j + 1) * NX + i

                i4 = (k + 1) * NY * NX + j * NX + i
                i5 = (k + 1) * NY * NX + j * NX + (i + 1)
                i6 = (k + 1) * NY * NX + (j + 1) * NX + (i + 1)
                i7 = (k + 1) * NY * NX + (j + 1) * NX + i

                c.append([i0, i1, i2, i3, i4, i5, i6, i7])
    return c


def ReadGridData(filename):
    grid_data = []
    with open(filename, 'r') as data_file:
        for line in data_file:
            grid_data.append(float(line))
    return grid_data


def GetGridData():
    '''
    Gets the data from the output of binaryReader
    :return: A list of lists of grid data
    '''
    grid_data = []
    set_of_grids = glob(pathname="./GridData*.txt")
    print("Getting Grid Data")
    for grid in set_of_grids:
        grid_data.append(ReadGridData(grid))
    print("Finished GridData")
    return grid_data


def GetMetaData():
    filename = os.path.join("MetaDataVTK.txt")
    meta_data = ReadGridData(filename=filename)
    return meta_data


def WriteProxyDataset():
    filename = "chymeraData.visit"
    with open(filename, "wt") as all_data:
        all_data.write("!NBLOCKS 360\n")

    #f = open("test.visit", "wt")
    #f.write("!NBLOCKS 360\n")
    # Get the mesh 6 times and add it all up.
    #all_pts = []
    #size_of_grid = NZ*NX*NY
    #connections_size = 8*size_of_grid
    #print(connections_size)
    #points_size = 3*size_of_grid
    # Create memmaps to deal with Python running out of memory
    #all_conn = numpy.memmap(os.path.join("/media/jacob/New Volume/","connections.memmap"), mode="w+", dtype="int", shape=(connections_size, connections_size))
    #all_pts = numpy.memmap("points.memmap", mode="w+", dtype="float16", shape=(points_size, points_size))
    #all_var = []
    #pts_length = 0
    #conn_length = 0
        for i in range(360):
            pts = []
            conn = []
            angle = math.radians(float(i) * 1.)
            angle2 = math.radians(float(i + 1) * 1.)
            pts += GetMeshPoints(angle, angle2)
            conn += GetMeshConnectivity()
            var = []
            grid = pyvtk.UnstructuredGrid(points=pts, hexahedron=conn)
            print("Finished Unstructured Grid")
            # Get the GridData
            values = GetGridData()
            end_point = int(i + (len(pts) - 1 / 3))
            print(int(i + ((len(pts) -1) / 3)))
            celldata = pyvtk.CellData(pyvtk.Scalars(values[0][i:end_point], name="data1"),
                                      pyvtk.Scalars(values[1][i:end_point], name="data2"),
                                      pyvtk.Scalars(values[2][i:end_point], name="data3"),
                                      pyvtk.Scalars(values[3][i:end_point], name="data4"),
                                      pyvtk.Scalars(values[4][i:end_point], name="data5"),)

            vtk = pyvtk.VtkData(grid, celldata, title)
            vtk.tofile("chymera%d.vtk\n" % i)
            all_data.write("chymera%d\n" % i)
            print("Done in i range" + str(i))


WriteProxyDataset()