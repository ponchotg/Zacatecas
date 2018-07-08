class ChargeCalculator():
	"""docstring for BASE"""
	def __init__(self,hour,quarter,a,ha,b,hb,lost):
		self.hour = hour
		self.quarter = quarter
		self.hrA = int(ha[:2])
		self.mnA = int(ha[3:])
		self.hrB = int(hb[:2])
		self.mnB = int(hb[3:])
		self.yrA = int(a[6:])
		self.mtA = int(a[3:5])
		self.dyA = int(a[:2])
		self.yrB = int(b[6:])
		self.mtB = int(b[3:5])
		self.dyB = int(b[:2])
		
	def theMath(self):
		leapYears = {2016:True, 2017:False,2018:False,2019:False,2020:True,2021:False}
		yeardif = self.yrB - self.yrA
		monthdif = self.mtB - self.mtA
		daydif = self.dyB-self.dyA
		hdif = self.hrB-self.hrA
		mdif = self.mnB-self.mnA
		leap = leapYears[self.yrA]
		yMonth = self.allToMin(yeardif,4,leap)
		mMin = self.allToMin(monthdif + yMonth,3,leap)
		dMin = self.allToMin(daydif,2,leap)
		hMin = self.allToMin(hdif,1,leap)
		tMin = mMin + dMin + hMin + mdif
		if tMin < 60 :
			tHour = 1
			cobroxh = tHour * self.hour
			return cobroxh
		tHour = tMin / 60
		tMin = tMin - (tHour * 60)
		cobroxh = tHour * self.hour
		tQuar = tMin / 15
		tMin = tMin - (tQuar * 15)
		if (tMin > 0):
			tQuar += 1
		cobroxq = tQuar * self.quarter
		total = cobroxh + cobroxq
		#print tHour
		#print cobroxh
		#print tQuar
		#print cobroxq
		#print total
		return total

	def allToMin(self,arg,level,leap):
		daysOfMonth = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
		daysOfMonthL = {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
		if level == 4:
			return arg * 12
		elif level == 3:
			tomult = 31
			if ((leap) and (arg < 2)):
				tomult = daysOfMonthL[self.mtA]
			elif ((leap == False) and (arg < 2)):
				tomult = daysOfMonth[self.mtA]
			tSend = ((arg * tomult) * 24) * 60
			return tSend
		elif level == 2:
			return (arg * 24) * 60
		elif level == 1:
			return arg * 60
		else :
			return 0

def runCharge(hour,quarter,a,ha,b,hb,lost):
	base = ChargeCalculator(hour,quarter,a,ha,b,hb,lost)
	total = base.theMath()
	print total + lost
	return total + lost

if __name__ == '__main__':
	hour = 20
	quarter = 5
	a = "01,02,2016"
	b = "01,02,2016"
	ha = "12:48"
	hb = "19:41"
	lost = 0
	run(hour,quarter,a,ha,b,hb,lost)
	

	
		
	

