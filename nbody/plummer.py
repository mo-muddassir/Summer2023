import numpy as np
from nbody import System
from random import random, seed

G =1
R =1
M=1
pi = np.pi

N = 20000

X1 = np.random.uniform(0,1,N)

#print(X1)

r = (pow(X1,-2/3)-1)**(-1/2)

#print(r)

M = (r**3)*pow((1+(r**2)),-3/2)

m = 1/N

#print(M)

X2 = np.random.uniform(0,1,N)
X3 = np.random.uniform(0,1,N)

z = (1-2*X2)*r

x = pow((r**2 - z**2),0.5)*((np.cos(2*pi*X3)))

y = pow((r**2 - z**2),0.5)*((np.sin(2*pi*X3)))

def prop_check(X4,X5):
	g = (X4**2)*((1-X4**2)**(7/2))
	
	if 0.1*X5 < g:
		return True
	else:
		return False
	
i=0

q =[]
	
while i<N:
	var = np.random.uniform(0,0.99)
	var2 = np.random.uniform(0,0.99)
	if prop_check(var,var2) == True:
		q.append(var)
		i+=1

g = np.zeros(N)
for i in range(N):
	g[i] = (q[i]**2)*((1-q[i]**2)**(7/2))

Ve = (2**0.5)*pow((1+r**2),-1/4)

V = q*Ve

X6 = np.random.uniform(0,1,N)
X7 = np.random.uniform(0,1,N)

w = (1-2*X6)*V

u = pow(abs(V**2 - z**2),0.5)*((np.cos(2*pi*X7)))

v = pow(abs(V**2 - z**2),0.5)*((np.sin(2*pi*X7)))	

	
parts = np.zeros(N, dtype=System._particle_type)
parts['mass'] = m

parts['position'] = np.vstack((x.flatten(), y.flatten(), z.flatten())).T
parts['velocity'] = np.vstack((u.flatten(), v.flatten(), w.flatten())).T

plummer_system = System(particles = parts)

print(plummer_system._particles)

plummer_system.write("plummer_sphere.dat")


			
	
	
