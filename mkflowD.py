################################################################################
'''Module "mkflowsD", July 2010, is part of
BETR-Research by Harald von Waldow <hvwaldow@chem.ethz.ch>, which is
based on BETR-Global by Matt MacLeod <matthew.macleod@chem.ethz.ch>

This module calculates D-values for inter-cell transport processes of a
particular model parametrization.'''
################################################################################
from numpy import *
import inspect
from globalz import *
import sys
import copy
import pdb

def mkflowD(model):
    fdict=copy.deepcopy(model.flowdict)
    #If velocity of wind G/A is smaller than 1000m/h, the G/A should be 1000m/h. here, we consider
    #upper and lower air.   by FY
    for [k,v] in list(fdict.items()):
        if k[0]==1 and k[1]==1:
            for i in range (len(v)):
                for j in range(12):
                    # newer numpy requires integers for indexing
                    # v[i][0] is a float, so it must be cast
                    a=int(v[i][0]-1)
                    velocity=v[i][j+2]/(sqrt(model.par['A'][a][j])*model.par['h1'][a][j])
                    if velocity<1000:
                       v[i][j+2]=1000*(sqrt(model.par['A'][a][j])*model.par['h1'][a][j])
        if k[0]==2 and k[1]==2:
            for i in range (len(v)):
                for j in range(12):
                    # newer numpy requires integers for indexing
                    # v[i][0] is a float, so it must be cast
                    a=int(v[i][0]-1)
                    velocity=v[i][j+2]/(sqrt(model.par['A'][a][j])*model.par['h2'][a][j])
                    if velocity<1000:
                       v[i][j+2]=1000*(sqrt(model.par['A'][a][j])*model.par['h2'][a][j])

        if k[0]==8 and k[1]==8:
            for i in range (len(v)):
                for j in range(12):
                    # newer numpy requires integers for indexing
                    # v[i][0] is a float, so it must be cast
                    a=int(v[i][0]-1)
                    velocity=v[i][j+2]/(sqrt(model.par['A'][a][j])*model.par['h1'][a][j])
                    if velocity<1000:
                       v[i][j+2]=1000*(sqrt(model.par['A'][a][j])*model.par['h1'][a][j])*model.par['fcp1'][a][j]
                    else:
                       v[i][j+2]=v[i][j+2]*model.par['fcp1'][a][j]
        if k[0]==9 and k[1]==9:        
            for i in range (len(v)):
                for j in range(12):
                    # newer numpy requires integers for indexing
                    # v[i][0] is a float, so it must be cast
                    a=int(v[i][0]-1)
                    velocity=v[i][j+2]/(sqrt(model.par['A'][a][j])*model.par['h2'][a][j])                    
                    if velocity<1000:
                        v[i][j+2]=1000*(sqrt(model.par['A'][a][j])*model.par['h2'][a][j])*model.par['ffp2'][a][j]
                    else:
                        v[i][j+2]=v[i][j+2]*model.par['ffp2'][a][j]
            zeroffp2=where(sum(model.par['ffp2'], axis=1)==0)[0]
            for ii in range (len(v)):
                for jj in zeroffp2:
                    if (v[ii][1]-1)==jj:
                        v[ii][2:]=v[i][2:]*model.par['ffp2'][jj]                

        if k[0]==10 and k[1]==10:
            for i in range (len(v)):
                for j in range(12):
                    # newer numpy requires integers for indexing
                    # v[i][0] is a float, so it must be cast
                    a=int(v[i][0]-1)
                    velocity=v[i][j+2]/(sqrt(model.par['A'][a][j])*model.par['h2'][a][j])
                    if velocity<1000:
                       v[i][j+2]=1000*(sqrt(model.par['A'][a][j])*model.par['h2'][a][j])*model.par['fcp2'][a][j]
                    else:
                       v[i][j+2]=v[i][j+2]*model.par['fcp2'][a][j]

    #Dflow=GZ
    for f in list(fdict.keys()):        
        fromcells=fdict[f][:,0].astype(int)
        zvals=model.zdict[f[0]]['bulk'][fromcells-1,:]
        vvals=model.vdict[f[0]]['bulk'][fromcells-1,:]   #FY
        fdict[f][:,2:]=fdict[f][:,2:]*zvals             #Old version
        
        # limited time is 2h   by FY
        time=2
        fdict[f][:,2:]=minimum(fdict[f][:,2:]*zvals, vvals*zvals/time)

    return(fdict)
