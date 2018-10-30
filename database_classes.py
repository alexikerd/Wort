from init import db

class Malt(db.Model):
	__tablename__ = 'malt'
	id = db.Column(db.Integer, primary_key = True)
	MaltName = db.Column(db.Text)
	PPG = db.Column(db.Float)
	Lovibond = db.Column(db.Float)

	def __init__(self, MaltName, PPG, Lovibond):
		self.MaltName = MaltName
		self.PPG = PPG
		self.Lovibond = Lovibond

class Hop(db.Model):
	__tablename__ = 'hop'
	id = db.Column(db.Integer, primary_key = True)
	HopName = db.Column(db.Text)
	AA = db.Column(db.Float)

	def __init__(self, HopName, AA):
		self.HopName = HopName
		self.AA = AA