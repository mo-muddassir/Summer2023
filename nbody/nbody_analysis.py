#!/usr/bin/env python3

import os
from nbody import *
import argparse
from os.path import splitext
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='Calculate the binned density profile of the N-body system.')
parser.add_argument('filenames',nargs='*', help='file names to read in')
parser.add_argument('-f', dest = 'outfile', default = 'analysis/analysis', help = 'output file name base')

args = parser.parse_args()

files = args.filenames

for f in files:

	outfile = splitext(f)[0] + ".pdf"

	os.system(f'nbody_density.py {f}')
	
	os.system(f'nbody_velocity.py {f}')



for i in range(len(files)):

	s = System.read(f)
	AM = System.angular_momentum(s)
	#E = System.potential_energy(s)+System.kinetic_energy(s)
	
	fig, axs = plt.subplots(2, constrained_layout=True)
	
	fig.suptitle(f'{splitext(args.filenames[i])[0]} AM = {AM} ')
	
	for ax in axs.flat:
		ax.set(xlabel = 'log10(r)')
	axs[0].set_ylabel('<vr^2>')
	axs[1].set_ylabel('Density')


	vel_data = np.loadtxt(f'{splitext(args.filenames[i])[0]}.vel', unpack=True)
	den_data = np.loadtxt(f'{splitext(args.filenames[i])[0]}.den', unpack=True)
	
	
	#r = np.logspace(-3,3)

	#vr_2 = (1/6)*(1/(1+(r/args.R)**2))**0.5

	axs[0].plot(vel_data[0],vel_data[1], marker = '.',linestyle = 'None')
	#axs[0].plot(np.log10(r),vr_2)
	axs[1].plot(den_data[0],den_data[1],marker  = '.',linestyle = 'None')

	plt.savefig(f'{args.outfile}{i}.pdf')
	
