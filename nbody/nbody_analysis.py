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

parser.add_argument('-M', dest='M', default=1, type=int, help='total mass')

parser.add_argument('-R', dest = 'R', default = 1, type = int, help ='Plummer radius')

parser.add_argument('-G', dest='G', default=1, type=int, help='Gravitational Constant')

parser.add_argument('-equal', dest = 'equal', action = 'store_true',help = 'Activate for equal mass binning') 

args = parser.parse_args()

files = args.filenames



pi = np.pi

r = np.logspace(-3,3)

for f in files:

	outfile = splitext(f)[0] + ".pdf"

	os.system(f'nbody_density.py {f}')
	
	os.system(f'nbody_velocity.py {f} -equal')

fig, axs = plt.subplots(2,figsize = (15,15), constrained_layout=True)


vr_2 = (1/6)*(1/(1+(r/args.R)**2))**0.5
plum_den = (3/4/pi)*(args.M/(args.R**3))*(pow((1+(r/args.R)**2),-5/2))

axs[0].plot(np.log10(r),vr_2,label='Theoretical')
axs[1].plot(np.log10(r), np.log10(plum_den),label='Theoretical')

for i in range(len(files)):

	s = System.read(args.filenames[i])
	AM = System.angular_momentum(s)
	E = System.potential_energy_shell(s)+System.kinetic_energy(s)
	
	
	
	#fig.suptitle(f'{splitext(args.filenames[i])[0]} AM = {AM} E={E}')
	
	for ax in axs.flat:
		ax.set(xlabel = 'log10(r)')
	axs[0].set_ylabel('<vr^2>')
	axs[1].set_ylabel('Density')


	vel_data = np.loadtxt(f'{splitext(args.filenames[i])[0]}.vel', unpack=True)
	den_data = np.loadtxt(f'{splitext(args.filenames[i])[0]}.den', unpack=True)

	
	
	axs[0].plot(vel_data[0],vel_data[1],label = 'AM='+str(AM)+'E='+str(E))
	
	axs[0].legend()
	
	axs[1].plot(den_data[0],den_data[1],label = 'AM='+str(AM)+'E='+str(E))
	axs[1].legend()



fig.savefig(f'{args.outfile}.pdf')
	
