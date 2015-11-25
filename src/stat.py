# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#


class Stat:
	def __init__(self, cur=0, min=0, max=100, name='stat', st=None):  # st=(min,cur,max)
		if st:
			self._min=st[0]
			self._cur=st[1]
			self._max=st[2]
		else:
			self._cur=cur
			self._min=min
			self._max=max
		self._name=name
		self.stab()

	def __str__(self):
		return '{0}|{1}'.format(self._cur, self._max)

	def stab(self):
		if self._min!=None:
			self._cur=max(self._min, self._cur)
		elif self._max!=None:
			self._cur=min(self._max, self._cur)

	def getStat(self):
		return (self._min, self._cur, self._max)

	def getCur(self):
		return self._cur

	def setCur(self, cur):
		self._cur=cur
		self.stab()

	def changeCur(self, dcur):
		self._cur+=dcur
		self.stab()


class Level(Stat):
	def __init__(self, name='Lv', lv_coef=1.12, start_coef=500, lv=None):  # lv=(min.cur.max.xp)
		if lv:
			Stat.__init__(self, name=name, st=lv[:3])
			self._xp=lv[3]
		else:
			Stat.__init__(self, min=1, max=50, name=name)
			self._xp=0
		self._lv_coef=lv_coef
		self._start_coef=start_coef

	def stab(self):
		f=lambda x: self._start_coef*(self._lv_coef**(x))
		xp_max=f(self.getCur()+1)
		if self._xp>=xp_max:
			self._xp-=xp_max
			self.changeCur(1)
			Stat.stab(self)
			self.stab()
		elif self._xp<0:
			self._xp=0

	def getStat(self):
		return Stat.getStat(self)+(self._xp,)

	def getXp(self):
		return self._xp

	def setXp(self, xp):
		self._xp=xp
		self.stab()

	def changeXp(self, dxp):
		self._xp+=dxp
		self.stab()


class StatSet:
	def __init__(self):
		self._stats={}

	def addStat(self, name, stat):
		self._stats[name]=stat

	def getStats(self, queue=None, template=None):
		s=[]
		if not template:
			template='{0}={1}'
		if queue:
			for i in queue:
				try:
					s.append(template.format(i, str(self._stats[i])))
				except KeyError:
					pass
		else:
			for i in self._stats:
				s.append(template.format(i, str(self._stats[i])))
		return s
