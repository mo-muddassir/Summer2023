#!/usr/bin/env python3

from nbody import *
from random import *
import numpy as np
import argparse
from sys import argv
from sys import stderr
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Calculate the binned density profile of the N-body system.')
parser.add_argument('filename',nargs = '*', help='file name to read in')
parser.add_argument('-n', type=int, dest='num_bins', default=100, help='Number of bins')
parser.add_argument('-f', dest = 'outfile', default = 'nbody-velocity-plot.pdf', help = 'Output file name')
parser.add_argument('-t', dest = 'title', default = None, help = 'plot title')
parser.add_argument('-a', dest = 'R', default = 1, help = 'plummer radius scale factor')
args = parser.parse_args()

files = args.filename

s =[]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

r = np.logspace(-3,3)

vr_2 = (1/6)*(1/(1+(r/args.R)**2))**0.5

for i in range(len(files)):
	s.append(System.read(files[i]))


def velocity(sc):
	rmax = sc.rmax + 1e-3
	rmin = sc.rmin
	dr = np.log10(rmax / rmin) / args.num_bins

	print("  r_min = {0:6.3f}, r_max = {1:6.3f}, dr = {2:6.3f}".format(rmin, rmax,dr), file=stderr)

	mean_vr = np.zeros(args.num_bins)

	mean_vr_2 = np.zeros(args.num_bins)

	bin_pop = np.zeros(args.num_bins)

	bin_vr = np.zeros(args.num_bins)

	bin_vr_2 = np.zeros(args.num_bins)
	
	for p in sc: 
	

		r = np.sqrt(np.sum(p['position']**2))

		vr = ((p['position'][0]*p['velocity'][0])+(p['position'][1]*p['velocity'][1])+(p['position'][2]*p['velocity'][2]))/r
	
		pos = int( (np.log10(r) - np.log10(rmin)) / dr)
	
		bin_pop[pos] += 1
	
		bin_vr[pos] += vr
	
		bin_vr_2[pos] += vr**2
	radii = np.zeros(args.num_bins)

	for i in range(args.num_bins):
		radii[i] = np.power(10.0, np.log10(rmin) + 0.5 * dr + dr*i)
	
		mean_vr[i] = bin_vr[i] / bin_pop[i]
	
		mean_vr_2[i] = bin_vr_2[i] / bin_pop[i]
	return radii,mean_vr_2
	
	
	
for i in range(len(s)):
	ax.plot(np.log10(velocity(s[i])[0]),velocity(s[i])[1],'+', label =f't={i}')
	

plt.xlabel("log10(r)")
plt.ylabel("<vr^2>")
plt.title(args.title)
plt.legend()
plt.savefig(args.outfile)
