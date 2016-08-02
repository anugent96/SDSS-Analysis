"""
To find potential unmasked cosmic rays and other imaging errors in SDSS
"""

import sys
image1 = str(sys.argv[1]) # SDSS csv file

"""
Importing the SDSS csv file into a readable python array
"""
import csv

import pandas
df = pandas.read_csv(image1, sep = ',', header=None)

RA = df.values[:,0] #ra
dec = df.values[:,1] #dec

# de Vaucouleurs Fluxes
gDevFlux = df.values[:,2] #g-flux
rDevFlux = df.values[:,3] #r-flux
iDevFlux = df.values[:,4] #i-flux
zDevFlux = df.values[:,5] #z-flux

gDevIvar = df.values[:,6] #g-ivar
rDevIvar = df.values[:,7] #r-ivar
iDevIvar = df.values[:,8] #i-ivar
zDevIvar = df.values[:,9] #z-ivar

# Exponential Fluxes
gExpFlux = df.values[:,10] #g-flux
rExpFlux = df.values[:,11] #r-flux
iExpFlux = df.values[:,12] #i-flux
zExpFlux = df.values[:,13] #z-flux

gExpIvar = df.values[:,14] #g-ivar
rExpIvar = df.values[:,15] #r-ivar
iExpIvar = df.values[:,16] #i-ivar
zExpIvar = df.values[:,17] #z-ivar

# Type (star, galaxy, cosmic ray, etc)
type1 = df.values[:,18]

import numpy as np
#Strings to Floats
ra = [float(x) for x in RA if x != 'ra']
DEC = [float(x) for x in dec if x != 'dec']

gD = np.array([float(x) for x in gDevFlux if x != 'gDEVflux'])
rD = np.array([float(x) for x in rDevFlux if x != 'rDEVflux'])
iD = np.array([float(x) for x in iDevFlux if x != 'iDEVflux'])
zD = np.array([float(x) for x in zDevFlux if x != 'zDEVflux'])

gE = np.array([float(x) for x in gExpFlux if x != 'gEXPflux'])
rE = np.array([float(x) for x in rExpFlux if x != 'rEXPflux'])
iE = np.array([float(x) for x in iExpFlux if x != 'iEXPflux'])
zE = np.array([float(x) for x in zExpFlux if x != 'zEXPflux'])

gDivar = np.array([float(x) for x in gDevIvar if x != 'gDEVivar'])
rDivar = np.array([float(x) for x in rDevIvar if x != 'rDEVivar'])
iDivar = np.array([float(x) for x in iDevIvar if x != 'iDEVivar'])
zDivar = np.array([float(x) for x in zDevIvar if x != 'zDEVivar'])

gEivar = np.array([float(x) for x in gExpIvar if x != 'gEXPivar'])
rEivar = np.array([float(x) for x in rExpIvar if x != 'rEXPivar'])
iEivar = np.array([float(x) for x in iExpIvar if x != 'iEXPivar'])
zEivar = np.array([float(x) for x in zExpIvar if x != 'zEXPivar'])

type2 = [float(x) for x in type1 if x != 'type']

# Flux values with inverse variance
g_D = gD*(gDivar**0.5) 
r_D = rD*(rDivar**0.5)
i_D = iD*(iDivar**0.5)
z_D = zD*(zDivar**0.5)

g_E = gE*(gEivar**0.5) 
r_E = rE*(rEivar**0.5)
i_E = iE*(iEivar**0.5)
z_E = zE*(zEivar**0.5)


# To find potential cosmic rays (de Vaucouleurs, r)
RA_D1 = [x for (x, mask1, mask2) in zip(ra, g_D, r_D) if mask1 < 0 and mask2 > 2]
DEC_D1 = [x for (x, mask1, mask2) in zip(DEC, g_D, r_D) if mask1 < 0 and mask2 > 2]
gD1 = [x for (x, mask1, mask2) in zip(g_D, g_D, r_D) if mask1 < 0 and mask2 > 2]
rD1 = [x for (x, mask1, mask2) in zip(r_D, g_D, r_D) if mask1 < 0 and mask2 > 2]
iD1 = [x for (x, mask1, mask2) in zip(i_D, g_D, r_D) if mask1 < 0 and mask2 > 2]
zD1 = [x for (x, mask1, mask2) in zip(z_D, g_D, r_D) if mask1 < 0 and mask2 > 2]
Type = [x for (x, mask1, mask2) in zip (type2, g_D, r_D) if mask1 < 0 and mask2 > 2]
      
RA_D2 = [x for (x, mask1, mask2) in zip(RA_D1, zD1, iD1) if mask1 < 0 and mask2 < 0]
DEC_D2 = [x for (x, mask1, mask2) in zip(DEC_D1, zD1, iD1) if mask1 < 0 and mask2 < 0]
gD2 = [x for (x, mask1, mask2) in zip(gD1, zD1, iD1) if mask1 < 0 and mask2 < 0]
rD2 = [x for (x, mask1, mask2) in zip(rD1, zD1, iD1) if mask1 < 0 and mask2 < 0]
iD2 = [x for (x, mask1, mask2) in zip(iD1, zD1, iD1 ) if mask1 < 0 and mask2 < 0]
zD2 = [x for (x, mask1, mask2) in zip(zD1, zD1, iD1) if mask1 < 0 and mask2 < 0]
type_D = [x for (x, mask1, mask2) in zip (Type, zD1, iD1) if mask1 < 0 and mask2 < 0]



# To find potential cosmic rays (Exponential, i)
RA_E1 = [x for (x, mask1, mask2) in zip(ra, r_E, i_E) if mask1 < 0 and mask2 > 2]
DEC_E1 = [x for (x, mask1, mask2) in zip(DEC, r_E, i_E) if mask1 < 0 and mask2 > 2]
gE1 = [x for (x, mask1, mask2) in zip(g_E, r_E, i_E) if mask1 < 0 and mask2 > 2]
rE1 = [x for (x, mask1, mask2) in zip(r_E, r_E, i_E) if mask1 < 0 and mask2 > 2]
iE1 = [x for (x, mask1, mask2) in zip(i_E, r_E, i_E) if mask1 < 0 and mask2 > 2]
zE1 = [x for (x, mask1, mask2) in zip(z_E, r_E, i_E) if mask1 < 0 and mask2 > 2]
Type_E = [x for (x, mask1, mask2) in zip (type2, r_E, i_E) if mask1 < 0 and mask2 > 2]
      
RA_E2 = [x for (x, mask1, mask2) in zip(RA_E1, zE1, gE1) if mask1 < 0 and mask2 < 0]
DEC_E2 = [x for (x, mask1, mask2) in zip(DEC_E1, zE1, gE1) if mask1 < 0 and mask2 < 0]
gE2 = [x for (x, mask1, mask2) in zip(gE1, zE1, gE1) if mask1 < 0 and mask2 < 0]
rE2 = [x for (x, mask1, mask2) in zip(rE1, zE1, gE1) if mask1 < 0 and mask2 < 0]
iE2 = [x for (x, mask1, mask2) in zip(iE1, zE1, gE1 ) if mask1 < 0 and mask2 < 0]
zE2 = [x for (x, mask1, mask2) in zip(zE1, zE1, gE1) if mask1 < 0 and mask2 < 0]
type_E = [x for (x, mask1, mask2) in zip (Type, zE1, gE1) if mask1 < 0 and mask2 < 0]

# To find potential cosmic rays (de Vaucouleurs, g)
RA_D3 = [x for (x, mask1, mask2) in zip(ra, r_D, g_D) if mask1 < 0 and mask2 > 2]
DEC_D3 = [x for (x, mask1, mask2) in zip(DEC, r_D, g_D) if mask1 < 0 and mask2 > 2]
gD3 = [x for (x, mask1, mask2) in zip(g_D, r_D, g_D) if mask1 < 0 and mask2 > 2]
rD3 = [x for (x, mask1, mask2) in zip(r_D, r_D, g_D) if mask1 < 0 and mask2 > 2]
iD3 = [x for (x, mask1, mask2) in zip(i_D, r_D, g_D) if mask1 < 0 and mask2 > 2]
zD3 = [x for (x, mask1, mask2) in zip(z_D, r_D, g_D) if mask1 < 0 and mask2 > 2]
Type3 = [x for (x, mask1, mask2) in zip (type2, r_D, g_D) if mask1 < 0 and mask2 > 2]
      
RA_D4 = [x for (x, mask1, mask2) in zip(RA_D3, zD3, iD3) if mask1 < 0 and mask2 < 0]
DEC_D4 = [x for (x, mask1, mask2) in zip(DEC_D3, zD3, iD3) if mask1 < 0 and mask2 < 0]
gD4 = [x for (x, mask1, mask2) in zip(gD3, zD3, iD3) if mask1 < 0 and mask2 < 0]
rD4 = [x for (x, mask1, mask2) in zip(rD3, zD3, iD3) if mask1 < 0 and mask2 < 0]
iD4 = [x for (x, mask1, mask2) in zip(iD3, zD3, iD3) if mask1 < 0 and mask2 < 0]
zD4 = [x for (x, mask1, mask2) in zip(zD3, zD3, iD3) if mask1 < 0 and mask2 < 0]
type_D1 = [x for (x, mask1, mask2) in zip (Type3, zD3, iD3) if mask1 < 0 and mask2 < 0]


# To find potential cosmic rays (Exponential, z)
RA_E3 = [x for (x, mask1, mask2) in zip(ra, r_E, z_E) if mask1 < 0 and mask2 > 2]
DEC_E3 = [x for (x, mask1, mask2) in zip(DEC, r_E, z_E) if mask1 < 0 and mask2 > 2]
gE3 = [x for (x, mask1, mask2) in zip(g_E, r_E, z_E) if mask1 < 0 and mask2 > 2]
rE3 = [x for (x, mask1, mask2) in zip(r_E, r_E, z_E) if mask1 < 0 and mask2 > 2]
iE3 = [x for (x, mask1, mask2) in zip(i_E, r_E, z_E) if mask1 < 0 and mask2 > 2]
zE3 = [x for (x, mask1, mask2) in zip(z_E, r_E, z_E) if mask1 < 0 and mask2 > 2]
Type_E1 = [x for (x, mask1, mask2) in zip (type2, r_E, z_E) if mask1 < 0 and mask2 > 2]
      
RA_E4 = [x for (x, mask1, mask2) in zip(RA_E3, iE3, gE3) if mask1 < 0 and mask2 < 0]
DEC_E4 = [x for (x, mask1, mask2) in zip(DEC_E3, iE3, gE3) if mask1 < 0 and mask2 < 0]
gE4 = [x for (x, mask1, mask2) in zip(gE3, iE3, gE3) if mask1 < 0 and mask2 < 0]
rE4 = [x for (x, mask1, mask2) in zip(rE3, iE3, gE3) if mask1 < 0 and mask2 < 0]
iE4 = [x for (x, mask1, mask2) in zip(iE3, iE3, gE3 ) if mask1 < 0 and mask2 < 0]
zE4 = [x for (x, mask1, mask2) in zip(zE3, iE3, gE3) if mask1 < 0 and mask2 < 0]
type_E1 = [x for (x, mask1, mask2) in zip (Type_E1, iE3, gE3) if mask1 < 0 and mask2 < 0]
"""
print('de Vaucouleurs possible unmasked CRs')
print('RA , DEC, g, r, z, type')
i = 0
while i < len(RA_D2) and i < len(DEC_D2) and i < len(gD2) and i < len(rD2) and i < len(zD2) and i < len(type_D) and i < len(iD2):
    x = RA_D2[i]
    y = DEC_D2[i]
    z = gD2[i]
    w = rD2[i]
    a = zD2[i]
    b = type_D[i]
    c = iD2[i]
    print(x, y, z, w, c, a, b)   
    i +=1

print('Exponential possible unmasked CRs')
print('RA , DEC, g, r, z, type')
p = 0
while p < len(RA_E2) and p < len(DEC_E2) and p < len(gE2) and p < len(rE2) and p < len(zE2) and p < len(type_E) and p < len(iE2):
    x = RA_E2[p]
    y = DEC_E2[p]
    z = gE2[p]
    w = rE2[p]
    a = zE2[p]
    b = type_E[p]
    c = iE2[p]
    print(x, y, z, w, c, a, b)   
    p +=1
"""    
    
print('Num possible unmasked CRs (g, r, i, z)=')
print(len(RA_D4), len(RA_D2), len(RA_E2), len(RA_E4))
