#!/usr/bin/env python3

import argparse
import numpy as np
from nbody import System
from random import random, seed
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description = "Create a Plummer System of N particles of equal mass")

parser.add_argument('-N', dest='N', default=100000, type=int, help='Number of particles')

parser.add_argument('-R', dest = 'plum_rad', default = 1, type = int, help ='Plummer radius')

parser.add_argument('-G', dest='G', default=1, type=int, help='Gravitational Constant')

parser.add_argument('-f', dest='outfile', default=None, help='File to output to')

args = parser.parse_args()

def rand(N):
	return np.random.uniform(0,1,N)


#m = 1/args.N
pi=np.pi
i=0
q =[]

X1 = rand(args.N)
X2 = rand(args.N)
X3 = rand(args.N)
X6 = rand(args.N)
X7 = rand(args.N)

r = (pow(X1,-2/3)-1)**(-1/2)

def generate_masses():

    # Inverse transform sampling based on the CDF of the Plummer profile
    M_cdf = (1 + r**2)**(-1.5)
    M_cdf /= np.sum(M_cdf)
    masses = np.interp(X1, np.cumsum(M_cdf), M_cdf)

    # Adjust parameters according to your needs
    mass_scale = 1.0
    masses *= mass_scale

    # Normalize the mass distribution so that the total mass is 1.0
    masses /= np.sum(masses)

    return masses


# Set positions for each particle
	
z = (1-2*X2)*r

x = pow((r**2 - z**2),0.5)*((np.cos(2*pi*X3)))

y = pow((r**2 - z**2),0.5)*((np.sin(2*pi*X3)))


def generate_velocities(N=args.N):

    # Escape velocity
    Ve = np.sqrt(2) * np.power(1 + r**2, -0.25)

    # Gaussian distribution for velocities
    sigma = 0.2  # Adjust the width of the distribution as needed
    velocities = np.random.normal(loc=Ve, scale=sigma, size=N)

    # Ensure that velocities have sufficient resolution in the center
    w = (1 - 2 * X7) * velocities
    u = np.sqrt(np.abs(velocities**2 - w**2)) * np.cos(2 * np.pi * X7)
    v = np.sqrt(np.abs(velocities**2 - w**2)) * np.sin(2 * np.pi * X7)

    return np.vstack((u, v, w)).T	


masses = generate_masses()
print(f'Masses = {masses}')
print(f'total mass = {np.sum(masses)}')

#Create system with N particles, mass 1/N, positions [x,y,z], and velocity[u,v,w]	
parts = np.zeros(args.N, dtype=System._particle_type)
parts['mass'] = masses

parts['position'] = np.vstack((x.flatten(), y.flatten(), z.flatten())).T
parts['velocity'] = generate_velocities()

plummer_system = System(particles = parts)

plummer_system.write(args.outfile)
