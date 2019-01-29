from sqlalchemy import *
import pandas as pd
from os import path

Wort_Path = path.abspath(path.curdir)

e = create_engine('mysql://root:password@localhost:3306/wort')
conn = e.connect()
cur = conn.connection.cursor()


mdata = pd.read_csv(Wort_Path + r"\Malt.txt", delimiter='	', names = ["Malt", "Country", "Ingredient Type", "Malt Type", "PPG", "Lovibond", "Irrelevant"])
cur.execute("DROP TABLE IF EXISTS malt")
mdata.to_sql(name='malt',con=e)

hdata = pd.read_csv(Wort_Path + r"\Hop.txt", delimiter='	', names = ["Hop", "Alpha_Acid"])
cur.execute("DROP TABLE IF EXISTS hop")
hdata.to_sql(name='hop',con=e)



cur.close()
