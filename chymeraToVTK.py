__author__ = 'jacob'
import pyvtk, math, os
from glob import glob

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
    grid_data = []
    set_of_grids = glob(pathname="./GridData*.txt")
    for grid in set_of_grids:
        grid_data.append(ReadGridData(grid))
    return grid_data


def GetMetaData():
    filename = os.path.join("MetaDataVTK.txt")
    meta_data = ReadGridData(filename=filename)
    return meta_data


def WriteProxyDataset():
    filename = "chymeraData.vtk"

    #f = open("test.visit", "wt")
    #f.write("!NBLOCKS 360\n")
    # Get the mesh 6 times and add it all up.
    all_pts = []
    all_conn = []
    all_var = []
    for i in range(360):
        pts = []
        conn = []
        angle = math.radians(float(i) * 1.)
        angle2 = math.radians(float(i + 1) * 1.)
        pts += GetMeshPoints(angle, angle2)
        conn += GetMeshConnectivity()
        all_pts.append(pts)
        all_conn.append(conn)
        var = []
        #print(len(pts) / 3)
        #for j in range(len(pts) / 3):
         #   var.append(math.cos(pts[j * 3]) + math.sin(pts[j * 3 + 1]) + math.sin(pts[j * 3 + 2]))
            # Pass the data to visit_writer
            #vars = [("var", 1, 1, var)]
            #visit_writer.WriteUnstructuredMesh("test%d.vtk" % i, 1, pts, conn, vars)
            #f.write("test%d.vtk\n" % i)
        #all_var.append(var)

    final_pts = []
    final_conn = []
    for index, element in enumerate(len(all_pts)):
        for i, element_pts in enumerate(len(all_pts[index])):
            final_pts.append(element_pts)

    for index, element in enumerate(len(all_conn)):
        for i, element_pts in enumerate(len(all_conn[index])):
            final_conn.append(element_pts)

    grid = pyvtk.UnstructuredGrid(points=final_pts, hexahedron=final_conn)

    # Get the GridData
    values = GetGridData()
    celldata = pyvtk.CellData(pyvtk.Scalars(values[0], name="data1"),
                              pyvtk.Scalars(values[1], name="data2"),
                              pyvtk.Scalars(values[2], name="data3"),
                              pyvtk.Scalars(values[3], name="data4"),
                              pyvtk.Scalars(values[4], name="data5"),)

    vtk = pyvtk.VtkData(grid, celldata, title)
    vtk.tofile(filename)


WriteProxyDataset()