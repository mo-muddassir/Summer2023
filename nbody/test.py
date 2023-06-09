import os
import argparse
from os.path import splitext

parser = argparse.ArgumentParser(description='Calculate the binned density profile of the N-body system.')
parser.add_argument('filenames',nargs = '*', help='file names to read in')

args = parser.parse_args()

files = args.filenames

for f in files:

	outfile = splitext(f)[0] + ".pdf"

	os.system(f'nbody_velocity.py {f} -f {outfile}')

	os.system(f'nbody_density.py {f}')
	
	
