from init import e, db
from database_classes import Malt, Hop

# Recipe_Name = input("Hi, welcome to Wuerze.  What would you like to name your beer recipe?  ")

# basically, from here you just do your normal process, change the parameters of Hop() and run add, commit
# we will also need to define a Recipe table and connect the malts / hops it uses to the recipe, along with the
# other imformation the recipe will need. I can help you with this if you get stuck. It's an abstract concept.

hop = Hop(HopName='test', AA=6.9)

db.session.add(hop)
db.session.commit()



"""
My idea for the recipe class:

Recipe:
	name - text
	abv - float
	ibu - float
	batch volume - float
	color - integer (we create lookup table for integer to text)
	
ColorLookup:
	id - general id for the text (premade by sql)
	colorName - name for the color
	colorDescription - description of the color
From here, you will assign Recipe color int to the id of the colorlookup

MaltLookup / HopLookup
	malt/hopid - the id of the malt or hop
	recipeid - the id of the recipe this maps to
This will be the same for both malt and hops
You will have multiple of the same malt and hop but with different recipe id
This allows you to keep malt, hop, and recipe abstract

"""