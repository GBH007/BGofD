# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

import sys

sys.path.append('..')

import src.stat as sstat
import src.tech as stech
import src.cord as scord


class Entity:
	__PATH_TO_MAP='/home/gbh007/Dropbox/PG/black_engine_python/'

	def __init__(self, data):
		self.load(data)

	def load(self, data):
		parser=stech.OneDataParser(data)
		self._id=parser.getInt('id')
		parser2=stech.OneDataParser(open(self.__PATH_TO_MAP+'map/entity_info/'+str(self._id)+'.ent').read())
		self._name=parser.getString('name')
		self._cord=scord.Cord(parser.getMultiInt('cord'))
		# self._hp=sstat.Stat(name='hp', st=parser.getMultiFloat('hp'))
		# self._mp=sstat.Stat(name='mp', st=parser.getMultiFloat('mp'))
		hp=(
			parser2.getFloat('hp_min'),
			parser.getFloat('hp'),
			parser2.getFloat('hp_max')
		)
		mp=(
			parser2.getFloat('mp_min'),
			parser.getFloat('mp'),
			parser2.getFloat('mp_max')
		)
		self._hp=sstat.Stat(name='hp', st=hp)
		self._mp=sstat.Stat(name='mp', st=mp)

	def upload(self):
		data=stech.OneDataConstructor()
		data2=stech.OneDataConstructor()
		data.addData('id', self._id)
		data.addData('name', self._name)
		data.addMultiData('cord', *self._cord.getCord())
		data2.addMultiData('cord', *self._cord.getCord())
		hp=self._hp.getStat()
		mp=self._mp.getStat()
		# data.addMultiData('hp', *self._hp.getStat())
		# data.addMultiData('mp', *self._mp.getStat())
		data.addData('hp', hp[1])
		data2.addData('hp_min', hp[0])
		data2.addData('hp_max', hp[2])
		data.addData('mp', mp[1])
		data2.addData('mp_min', mp[0])
		data2.addData('mp_max', mp[2])
		data.construct()
		data2.construct()
		print(data2.toData(),file=open(self.__PATH_TO_MAP+'map/entity_info/'+str(self._id)+'.ent','w'))
		return data.toData()

	def getId(self):
		return self._id

	def getName(self):
		return self._name

	def getZ(self):
		return self._cord.getZ()

	def getCord(self):
		return self._cord

	# def __str__(self):
	#     s=''
	#     for i,j in self.__dict__.items():
	#         s+=str(i)+' = '+str(j)+'\n'
	#     return s


class Entitys:
	__PATH_TO_MAP='/home/gbh007/Dropbox/PG/black_engine_python/'

	def __init__(self, z=0):
		self._entitys={}
		self.load()
		if z!=None: self.load(z)

	def load(self, level=None):
		if level!=None:
			cache=[i for i in open(self.__PATH_TO_MAP+'map/level'+str(level)+'.ent').read().split('#entity') if i]
		else:
			cache=[i for i in open(self.__PATH_TO_MAP+'map/ERR.ent').read().split('#entity') if i]
		for i in cache:
			e=Entity(i)
			self._entitys[e.getId()]=e

	def upload(self, level=None):
		if level!=None:
			f=open(self.__PATH_TO_MAP+'map/level'+str(level)+'.ent', 'w')
		else:
			f=open(self.__PATH_TO_MAP+'map/ERR.ent', 'w')
		trash=[]
		for i in self._entitys:
			if level==None or self._entitys[i].getZ()==level:
				print('#entity', file=f)
				print(self._entitys[i].upload(), end='', file=f)
				trash.append(i)
			# del self._entitys[i]
		for i in trash:
			del self._entitys[i]

	def getEntity(self,ID):
		return self._entitys[ID]

	def __del__(self):
		self.upload()


def main():
	a=Entitys()
	a.upload(0)


if __name__=='__main__':
	main()
