__author__ = 'jacob'
import os
from glob import glob

list_of_files = []

for filename in glob('*VTK.txt'):
    list_of_files.append(filename)

