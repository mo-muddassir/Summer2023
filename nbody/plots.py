#!/usr/bin/env python3

import argparse
import numpy as np
from nbody import System
from random import random, seed
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description = "Make and save Plummer plots")

parser.add_argument('-M', dest='M', default=1, type=int, help='total mass')

parser.add_argument('-R', dest = 'R', default = 1, type = int, help ='Plummer radius')

parser.add_argument('-G', dest='G', default=1, type=int, help='Gravitational Constant')

parser.add_argument('-f', dest='outfile', default=None, help='File to output to')


args = parser.parse_args()


r = np.logspace(-3,3)
pi = np.pi

plum_den = (3/4/pi)*(args.M/(args.R**3))*(pow((1+(r/args.R)**2),-5/2))

vdp_squared = ((args.G*args.M)/6)/(pow((r**2 + args.R**2),0.5))

fig, axs = plt.subplots(2)
fig.suptitle("Theoretical Plummer Plots")

axs[0].plot(np.log10(r), np.log10(plum_den))
axs[0].set_title("Plummer Density Profile")

axs[1].plot(np.log10(r), np.log10(vdp_squared))
axs[1].set_title("Velocity Dispersion")

fig.tight_layout()

plt.savefig(args.outfile)
