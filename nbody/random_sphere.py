from struct import unpack, pack
from array import array
from sys import stderr
import time
import copy

import numpy as np
from nbody import System

s = System.sphere_random(2000, 1, 1000)

c = System.cube_random(2000,1,1000)

#print(s._particles)

s.write("random_sphere.dat")

c.write("randome_cube.dat")

#s2=System.read("random_sphere.dat")

#print(s2._particles)
