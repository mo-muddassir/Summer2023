import numpy as np
import matplotlib.pyplot as plt
from nbody import System

from astropy.modeling.physical_models import Plummer1D as plm

G=1
M=1
R=1
r = np.logspace(-3,3)
pi = np.pi

plum_den = (3/4/pi)*(M/(R**3))*(pow((1+(r/R)**2),-5/2))

plt.plot(np.log10(r),np.log10(plum_den))
plt.title("Density Profile - Aarseth")
plt.xlabel("log(r)")
plt.ylabel("rho")
plt.savefig("Density Profile-Aarseth.pdf")
plt.show()

plt.plot(np.log10(r),np.log10(plm.evaluate(r,M,R)))
plt.title("Density Profile - Astropy")
plt.xlabel("log(r)")
plt.ylabel("rho")
plt.savefig("Density Profile-Astropy.pdf")
plt.show()

vdp_squared = ((G*M)/6)/(pow((r**2 + R**2),0.5))

vdp = pow(vdp_squared,0.5)

plt.plot(np.log10(r),np.log10(vdp_squared))
plt.title("Velocity Dispersion - sigma squared")
plt.xlabel("log(r)")

plt.ylabel("log(sigma^2)")
plt.savefig("Velocity Dispersion-sigma_sqr.pdf")
plt.show()
		
plt.plot(np.log10(r),np.log10(vdp))
plt.title("Velocity Dispersion - Sigma")
plt.xlabel("log(r)")
plt.ylabel("log(sigma)")

plt.savefig("Velocity Dispersion - sigma.pdf")
plt.show()


