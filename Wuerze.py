from sqlalchemy import *
import numpy as np
import scipy as sp
import pandas as pd
from scipy import stats
import math as math
import os
from os import path



Beer_Recipes_Path = r'C:\Users\alexi\Desktop\Wuerze\Beer_Recipes'
Recipe_Name = input("Hi, welcome to Wuerze.  What would you like to name your beer recipe?  ")
if path.exists(os.path.join(Beer_Recipes_Path, "{}.txt".format(Recipe_Name))):
	Repeat_Name = input("I'm sorry, you already have a beer recipe with this name, would you like to overwrite it (y or n)?  ")
	if Repeat_Name == "n":
		print('Ok, well try again')
		exit()
	if Repeat_Name == "y":
		os.remove(os.path.join(Beer_Recipes_Path, "{}.txt".format(Recipe_Name)))

#This should be very straightforward so far, but all I'm doing is setting up a folder to store my recipes and making sure I don't have duplicate names.



f= open(os.path.join(Beer_Recipes_Path, "{}.txt".format(Recipe_Name)),"w+")
m= open("{}.txt".format(Recipe_Name + "m"),"w+")
h= open("{}.txt".format(Recipe_Name + "h"),"w+")
e = create_engine('sqlite:///Wuerze.db')
conn = e.connect()
cur = conn.connection.cursor()

#I'm setting up individual files for malt and hops that will be useful later as well as getting the database started.



cur.execute('''DROP TABLE IF EXISTS malt''')
cur.execute('''CREATE TABLE malt (Malt text, PPG real, Lovibond real)''')
mdt = np.dtype([('Malt', 'U32'), ('Lovibond', 'f8'), ('PPG', 'f8')])
mdata = np.genfromtxt('Malt.txt', delimiter=None, dtype=mdt, usecols=(0,4,5))
maltdata  = np.column_stack((mdata['Malt'], mdata['PPG'] , mdata['Lovibond']))
cur.executemany("INSERT INTO malt VALUES (?,?,?)", maltdata)

cur.execute('''DROP TABLE IF EXISTS hop''')
cur.execute('''CREATE TABLE hop (Hop text, AA real)''')
hdt = np.dtype([('Hop', 'U32'), ('AA', 'f8')])
hdata = np.genfromtxt('Hop.txt', delimiter=None, dtype=hdt, usecols=(0,1))
hopdata = np.column_stack((hdata['Hop'], hdata['AA']))
cur.executemany("INSERT INTO hop VALUES (?,?)", hopdata)

#Here I created two tables within the database of Wuerze, one for every malt and one for every hop.  I can then pull from this database for specific recipe calculations.



Malt_Finisher = 'y'
while (Malt_Finisher == 'y'):
	Recipe_Malt = input("What malt would you like to add?  ")
	Recipe_Malt_Amount = input("And how many pounds of " + Recipe_Malt + " do you want to use?  ")
	cur.execute('SELECT * FROM malt WHERE Malt = ?', (Recipe_Malt,))
	for row in cur:
		m.write('{}	{}	{}	{}\n'.format(row[0], row[1], row[2], Recipe_Malt_Amount))
	Malt_Finisher = input("Do you want to add any more malt (y or n)?  ")
m.close()

Hop_Finisher = 'y'
while (Hop_Finisher == 'y'):
	Recipe_Hop = input("What hop would you like to add?  ")
	Recipe_Hop_Amount = input("And how many ounces of " + Recipe_Hop + " do you want to use?  ")
	Recipe_Hop_Boil = input("How many minutes will you boil " + Recipe_Hop + " for?  ")
	cur.execute('SELECT * FROM hop WHERE Hop = ?', (Recipe_Hop,))
	for row in cur:
		h.write('{}	{}	{}	{}\n'.format(row[0], row[1], Recipe_Hop_Amount, Recipe_Hop_Boil))
	Hop_Finisher = input("Do you want to add any more hops (y or n)?  ")
h.close()

cur.close()

#The files created earlier are populated with important information from the user involving the recipe as well as the relevant information for each ingredient in a usable format.  The database then is closed since it is no longer needed.



mdt2 = np.dtype([('Malt', 'U32'), ('PPG', 'f8'), ('Lovibond', 'f8'), ('Weight', 'f8')])
mdata2 = np.genfromtxt("{}.txt".format(Recipe_Name + "m"), delimiter=None, dtype=mdt2, usecols=(0,1,2,3))
maltydata  = np.column_stack((mdata2['Malt'], mdata2['PPG'], mdata2['Lovibond'], mdata2['Weight']))
#I begin with using the malt information as its calculations have an impact on the hop calculations.  I reformatted everything to make it much easier to handle.



Batch_Volume = input("How many gallons will your batch be?  ")
Batch_Volume = float(Batch_Volume)
Plato = sum(mdata2['PPG']*mdata2['Weight'])
SRM = 1.4922*((sum(mdata2['Weight']*mdata2['Lovibond'])/Batch_Volume)**0.6859)
Strike_Volume = 0.3125*(sum(mdata2['Weight']))
Volume_Absorbed = 0.125*(sum(mdata2['Weight']))
Original_Gravity = 1 + Plato/(1000 * Batch_Volume)

#There are three imporant parts of the malt calculations.  There are volume calculations (of which there are2 very important ones), the gravity, and color.  Gravity is much more easily tracked with
#the value 'Plato' as the actual specific gravity changes along with the volume (just look at the formula for Original_Gravity).  Essentially as water boils away the actual particles/sugar of the wort
#that came from the malt do not boil away, so the total amount remains constant.  Color, or SRM is the exact same way.  Volume calculations are significantly more difficult as volume is lost through
#a number of processes.  We have the initial amount of water that the malt is added to (Strike Volume), grain absorbs some of this away but we then pour more water through the grain to increase mash
#efficiency (Sparge Volume).  Wort is then boiled away and what remains needs to be the desired batch volume.  Volume lost due to absorption can be calculated by pure weight of the grain.  This is a
#good enough estimate as barley behaves as barley for the most part and finding a very accurate method accounting for how dry the barley is would be incredibly tedious.  So I will stick with an estimate
#for volume absorbed.  When it comes to Strike Volume, there is a desired grain to water ratio so simply by knowing how much grain we can find the initial volume.  We know the end volume result and once
#we know how much will be boiled away we can solve for Sparge Volume.


Boil_Time = float(input("How long will the boil last for?  "))
bdt = np.dtype([('Capacity_Volume', 'f8'), ('Boil_Volume', 'f8'), ('Final_Volume', 'f8'), ('Radius_Squared', 'f8'), ('Gravity', 'f8')])
bdata = np.genfromtxt('Boil_Experiment.txt', delimiter=None, dtype=bdt, usecols=(0,1,2,3,4), skip_header= 1)
boildata  = np.column_stack((bdata['Capacity_Volume'], 3.78541 * (bdata['Boil_Volume'] - bdata['Final_Volume']) / bdata['Radius_Squared'], bdata['Gravity'], bdata['Radius_Squared']))
boilstats = sp.stats.linregress(boildata[:,2], boildata[:,1])
Capacity = float(input("What's the volume capacity of the pot you'll be using to boil?  "))
brewdata = boildata[np.logical_not(boildata[:,0] != Capacity)]
Volume_Boiled = (boilstats[0] * Original_Gravity + boilstats[1]) * brewdata[0,3] * (Boil_Time/60) / 3.78541 
Sparge_Volume = Batch_Volume + Volume_Boiled - Strike_Volume + Volume_Absorbed
Volume_Preboil = Batch_Volume + Volume_Boiled
Initial_Gravity = 1 + Plato/(1000 * Volume_Preboil)

#There are many small factors that affect the boil off rate that are specific to each brewing setup.  These are too small to realistically measure and determine, but they will be the same
#each time I brew as it is the same set up.  The boil off rate is proportional to the surface area of the pot, temperature, and enthalpy of vaporization of the wort.  I've conducted some experiments
#involving boiling for 60 min that I put into a text file 'Boil_Experiment' that I will continue to add to each time that I brew.  Dividing the change in volume by the radius of the pot squared
#will allow me to determine the relationship between enthalpy of vaporization and volume change as temperature will be constant (or close enough to not impact the results).  The enthalpy of
#vaporization iself is a linear function gravity.  Therefore, I can experimentally determine the volume boiled off in a way that gets more accurate each time I brew.



hdt2 = np.dtype([('Hop', 'U32'), ('AA', 'f8'), ('Weight', 'f8'), ('Boil_Time', 'f8')])
hdata2 = np.genfromtxt("{}.txt".format(Recipe_Name + "h"), delimiter=None, dtype=hdt2, usecols=(0,1,2,3))
hoppydata  = np.column_stack((hdata2['AA']/100, hdata2['Weight'] , hdata2['Boil_Time']))
IBU = sum((1.65 * 0.000125**(Plato/(1000 * Batch_Volume))) * ((1 - np.exp(-0.04 * hoppydata[:,2]))/4.15) * (hoppydata[:,0]*hoppydata[:,1]*7490/(Batch_Volume)))

#hop calculations are significantly easier as all I had to do was determine the IBU using the Tinseth equation.



f.write('{}		{} gallons\n'.format(Recipe_Name, Batch_Volume))
f.write('\nOG:	{}\n'.format(Original_Gravity))
f.write('IBU:	{}\n'.format(IBU))
if SRM < 2:
	f.write('Color:	Pale Straw ({})\n'.format(SRM))
if SRM > 2 and SRM <= 3:
	f.write('Color:	Straw ({})\n'.format(SRM))
if SRM > 3 and SRM <= 4:
	f.write('Color:	Pale Gold ({})\n'.format(SRM))
if SRM > 4 and SRM <= 6:
	f.write('Color:	Deep Gold ({})\n'.format(SRM))
if SRM > 6 and SRM <= 9:
	f.write('Color:	Pale Amber ({})\n'.format(SRM))
if SRM > 9 and SRM <= 12:
	f.write('Color:	Medium Amber ({})\n'.format(SRM))
if SRM > 12 and SRM <= 15:
	f.write('Color:	Deep Amber ({})\n'.format(SRM))
if SRM > 15 and SRM <= 18:
	f.write('Color:	Amber-Brown ({})\n'.format(SRM))
if SRM > 18 and SRM <= 20:
	f.write('Color:	Brown ({})\n'.format(SRM))
if SRM > 20 and SRM <= 24:
	f.write('Color:	Ruby Brown ({})\n'.format(SRM))
if SRM > 24 and SRM <= 30:
	f.write('Color:	Deep Brown ({})\n'.format(SRM))
if SRM > 30:
	f.write('Color:	Black ({})\n'.format(SRM))
f.write('Strike Volume:	{}\n'.format(Strike_Volume))
f.write('Sparge Volume:	{}\n'.format(Sparge_Volume))
f.write('\nMalt				Amount\n')
for row in maltydata:
	f.write("{}				{}\n".format(row[0], row[3]))
f.write('\nHop				Amount				Boil Time')
for row in hdata2:
	f.write("\n{}				{}				{}".format(row[0], row[2], row[3]))
f.close()
os.remove("{}.txt".format(Recipe_Name + "m"))
os.remove("{}.txt".format(Recipe_Name + "h"))

#Also relatively straightforward, I write out the recipe into a very readable format and get rid of the two assistant text files required for calculations.