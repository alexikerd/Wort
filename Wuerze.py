#from sqlalchemy import create_engine
#import os
import numpy as np

#mdt = np.dtype([('Malt', 'U32'), ('Country', 'U16'), ('Grain', 'U5'), ('Malt_Type', 'U16'), ('PPG', 'i4'), ('Lovibond', 'i4'), ('#_of_Recipes','i4')])
mdt = np.dtype([('Malt', 'U32'), ('PPG', 'i4'), ('Lovibond', 'i4')])

mdata = np.genfromtxt('Malt.txt', delimiter=None, dtype=mdt, usecols=(0,4,5))

hdt = np.dtype([('Hop', 'U32'), ('AA', 'f8')])

hdata = np.genfromtxt('Hop.txt', delimiter=None, dtype=hdt, usecols=(0,1))

#print(sum(mdata['Lovibond']))
#print(mdata["PPG"]*2)
#print(sum(mdata['PPG']*mdata['Lovibond']))
#print(mdata[3]['Malt'])
#print(mdata['Amber'][:])isn't working?

Batch_Volume = input("Hi, welcome to Wuerze.  What size batch are you wanting to make?  ")
print("So it's a", Batch_Volume, "gallon batch")
type(Batch_Volume)

#So, the volume lost due to boiling is relatively difficult to accurately calculate as it relies on properties of the wort and
#the radius of the pot.  Later I'm going to go back to determine experimentally this equation but until then I'm going to use the
#typical estimate that I've seemed to notice when I've brewed which is ~1 gallon per hour 

#Strike volume is dependent on the total weight of grain since we want an optimal density in order to break down the starches

#Volume absorbed is going to have to be calculated experimentally but I'm pretty sure that this will be fairly accurate
#to the given value of 0.125*(total weight of grain) as there are not nearly as much hidden factors here

Recipe_Name = input("What would you like to name your beer recipe?  ")
f= open("{}.txt".format(Recipe_Name),"w+")
m= open("{}.txt".format(Recipe_Name + "m"),"w+")
h= open("{}.txt".format(Recipe_Name + "h"),"w+")

Recipe_Malt = input("What malt would you like to add?  ")
Recipe_Malt_Amount = input("And how much of " + Recipe_Malt + " do you want to use?  ")
malt_generator = (item for item in mdata if item[0] == Recipe_Malt)
malt_props = list(malt_generator)[0]
m.write('{}	{}	{}	{}'.format(*malt_props, Recipe_Malt_Amount))


Malt_Finisher = input("Do you want to add any more malt (y or n)?  ")
while (Malt_Finisher == "y"):
	Recipe_Malt = input("What malt would you like to add?  ")
	Recipe_Malt_Amount = input("And how much of " + Recipe_Malt + " do you want to use?  ")
	malt_generator = (item for item in mdata if item[0] == Recipe_Malt)
	malt_props = list(malt_generator)[0]
	m.write('\n{}	{}	{}	{}'.format(*malt_props, Recipe_Malt_Amount))
	Malt_Finisher = input("Do you want to add any more malt (y or n)?  ")

print("hell yeah")

Recipe_Hop = input("What hops are ya lookin' to add?  ")
Recipe_Hop_Amount = input("And how many ounces of " + Recipe_Hop + " do you want to add?  ")
Recipe_Hop_Boil = input("How many minutes will " + Recipe_Hop + " boil for?  ")
hop_generator = (item for item in hdata if item[0] == Recipe_Hop)
hop_props = list(hop_generator)[0]
h.write('{}	{}	{}	{}'.format(*hop_props, Recipe_Hop_Amount, Recipe_Hop_Boil))

Hop_Finisher = input("Do you want to add any more hops (y or n)?  ")
while (Hop_Finisher == "y"):
	Recipe_Hop = input("What hop would you like to add?  ")
	Recipe_Hop_Amount = input("And how much of " + Recipe_Hop + " do you want to use?  ")
	Recipe_Hop_Boil = input("How many minutes will " + Recipe_Hop + " boil for?  ")
	hop_generator = (item for item in mdata if item[0] == Recipe_Hop)
	hop_props = list(hop_generator)[0]
	h.write('\n{}	{}	{}	{}'.format(*hop_props, Recipe_Hop_Amount, Recipe_Hop_Boil))
	Hop_Finisher = input("Do you want to add any more hops (y or n)?  ")