#!/usr/bin/env python3

import os
import argparse
from os.path import splitext
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='Calculate the binned density profile of the N-body system.')
parser.add_argument('filenames',nargs='*', help='file names to read in')

args = parser.parse_args()

files = args.filenames

for f in files:

	outfile = splitext(f)[0] + ".pdf"

	os.system(f'nbody_density.py {f}')
	
	os.system(f'velocity.py {f}')



for i in range(len(files)):
	fig, axs = plt.subplots(2, constrained_layout=True)
	fig.suptitle(f'Analysis for {args.filenames[i]}')
	
	
	for ax in axs.flat:
		ax.set(xlabel = 'log10(r)')
	axs[0].set_ylabel('<vr^2>')
	axs[1].set_ylabel('Density')


	vel_data = np.loadtxt(f'{splitext(args.filenames[i])[0]}.vel', unpack=True)
	den_data = np.loadtxt(f'{splitext(args.filenames[i])[0]}.den', unpack=True)

	axs[0].plot(vel_data[0],vel_data[1], marker = '.',linestyle = 'None')
	axs[1].plot(den_data[0],den_data[1],marker  = '.',linestyle = 'None')

	plt.savefig(f'{args.filenames[i]}.pdf')
	
	
