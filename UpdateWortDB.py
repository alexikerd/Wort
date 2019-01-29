from sqlalchemy import *
import pandas as pd



e = create_engine('mysql://root:$$$W9241739q@localhost:3306/wort')
conn = e.connect()
cur = conn.connection.cursor()


mdata = pd.read_csv(r"C:\Users\Owner\Desktop\Data Projects\Wort\Malt.txt", delimiter='	', names = ["Malt", "Country", "Ingredient Type", "Malt Type", "PPG", "Lovibond", "Irrelevant"])
cur.execute("DROP TABLE IF EXISTS malt")
mdata.to_sql(name='malt',con=e)

hdata = pd.read_csv(r"C:\Users\Owner\Desktop\Data Projects\Wort\Hop.txt", delimiter='	', names = ["Hop", "Alpha Acid"])
cur.execute("DROP TABLE IF EXISTS hop")
hdata.to_sql(name='hop',con=e)



cur.close()
