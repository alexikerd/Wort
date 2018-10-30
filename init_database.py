# this should only be run once
import numpy as np
import scipy as sp
import pandas as pd
from scipy import stats

from init import e, db
from database_classes import Hop, Malt

mdt = np.dtype([('Malt', 'U32'), ('Lovibond', 'f8'), ('PPG', 'f8')])
mdata = np.genfromtxt('Malt.txt', delimiter=None, dtype=mdt, usecols=(0,4,5))
maltdata  = np.column_stack((mdata['Malt'], mdata['PPG'] , mdata['Lovibond']))

for item in maltdata:
	malt = Malt(MaltName=item[0], PPG=item[1], Lovibond=item[2])
	db.session.add(malt)

hdt = np.dtype([('Hop', 'U32'), ('AA', 'f8')])
hdata = np.genfromtxt('Hop.txt', delimiter=None, dtype=hdt, usecols=(0,1))
hopdata = np.column_stack((hdata['Hop'], hdata['AA']))

for item in hopdata:
	hop = Hop(HopName=item[0], AA=item[1])
	db.session.add(hop)

db.session.commit()