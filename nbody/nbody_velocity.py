#!/usr/bin/env python3

from nbody import *
from random import *
import numpy as np
import argparse
from sys import argv
from sys import stderr
from os.path import splitext
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description='Calculate the binned density profile of the N-body system.')
parser.add_argument('filename', type=str, help='file name to read in')
parser.add_argument('-n', type=int, dest='num_bins', default=100, help='Number of bins')
parser.add_argument('-f', dest = 'outfile', default = 'nbody-velocity-plot.pdf', help = 'Output file name')
parser.add_argument('-a', dest = 'R', default = 1, help = 'plummer radius scale factor')
args = parser.parse_args()


#Read system details from source file
s = System.read(args.filename)

print("Binning in radial shells with logarithmic spacing", file=stderr)



rmax = s.rmax + 1e-3
rmin = s.rmin
dr = np.log10(rmax / rmin) / args.num_bins

print("  r_min = {0:6.3f}, r_max = {1:6.3f}, dr = {2:6.3f}".format(rmin, rmax,dr), file=stderr)




# Calculate and store mean radial velocities and rms velocities

mean_vr = np.zeros(args.num_bins)

mean_vr_2 = np.zeros(args.num_bins)

bin_pop = np.zeros(args.num_bins)

bin_vr = np.zeros(args.num_bins)

bin_vr_2 = np.zeros(args.num_bins)

for p in s: 
	

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




#Theoretical <vr^2>

r = np.logspace(-3,3)

vr_2 = (1/6)*(1/(1+(r/args.R)**2))**0.5


print(System.angular_momentum(s))
	
#Optional: print values of <vr> and <vr^2> to console
#total_mean = np.sum(mean_vr **2)/args.num_bins

#print(f"<vr> = {mean_vr}")

#print(f"<vr^2> = {mean_vr_2}")

#print(f"<vr^2 system> = {total_mean}")




#Save a plot of log10(r) vs <vr^2>

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(np.log10(r), vr_2,'.',label = 'Theoretical model')
ax.plot(np.log10(radii),mean_vr_2,'+', label = 'Simulation')
ax.set_title(f"<vr^2> for a sample Plummer Sphere with {len(s)} equal mass bodies")
ax.set_xlabel("log10(r)")
ax.set_ylabel("<vr^2>")
ax.legend()
plt.savefig(args.outfile)
#plt.show()
