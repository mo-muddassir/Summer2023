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

r = np.logspace(-1.2,3)



for f in files:

	outfile = splitext(f)[0] + ".pdf"

	os.system(f'nbody_density.py {f}')
	
	os.system(f'nbody_velocity.py {f}')

fig, axs = plt.subplots(2,figsize = (12,12), constrained_layout=True)


vr_2 = (1/6)*(1/(1+(r/args.R)**2))**0.5
plum_den = (3/4/pi)*(args.M/(args.R**3))*(pow((1+(r/args.R)**2),-5/2))

axs[0].plot(np.log10(r),vr_2,label='Theoretical')
axs[1].plot(np.log10(r), np.log10(plum_den),label='Theoretical')


plt.figure(facecolor='black')




for i in range(len(files)):
	
	
	axs[0].set_title('1 Million Particle Analysis',family = 'serif', fontsize = 18)
	plt.rcParams['font.size']=11
	plt.rcParams['font.family'] = 'serif'
	
	axs[0].tick_params(axis='both', which='both', labelsize=14)
	axs[1].tick_params(axis='both', which='both', labelsize=14)
	
	for ax in axs.flat:
		ax.set_xlabel('log10(r)', fontsize=16,font='serif')
		
	axs[0].set_ylabel('<vr^2>',fontsize = 16,family='serif')
	axs[1].set_ylabel('Density',fontsize=16, family = 'serif')
	
	axs[0].set_facecolor('black')
	axs[1].set_facecolor('black')


	vel_data = np.loadtxt(f'{splitext(args.filenames[i])[0]}.vel', unpack=True)
	den_data = np.loadtxt(f'{splitext(args.filenames[i])[0]}.den', unpack=True)

	
	
	axs[0].plot(vel_data[0],vel_data[1],label = splitext(args.filenames[i])[0])
	axs[0].legend()
	
	axs[1].plot(den_data[0],den_data[1],label = splitext(args.filenames[i])[0])
	axs[1].legend()



fig.savefig(f'{args.outfile}.pdf')
	
