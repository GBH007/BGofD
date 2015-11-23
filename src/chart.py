# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

import sys

sys.path.append('..')
import src.cord as scord
import src.tech as stech
from src.GOBJ import GOBJs,GOBJr


# class GameObjectPoint:
# 	def __init__(self, object, cord):
# 		self._object=object
# 		self._cord=scord.Cord(cord)
#
# 	def getCord(self):
# 		return self._cord.getCord()
#
# 	def getObject(self):
# 		return self._object


class GameObject:
	def __init__(self, data):
		# self._gpoints={}
		self._points=[]
		self.load(data)

	def load(self, data):
		parser=stech.OneDataParser(data)
		self._type=parser.getString('type')
		self._form=parser.getString('form')
		self._cord1=scord.Cord(parser.getMultiInt('cord1'))
		self._cord2=scord.Cord(parser.getMultiInt('cord2'))	#cord2 сдвиг относительно cord1 для form=square
		self.postload()

	def postload(self):
		cord1=self._cord1.getCord()
		cord2=self._cord2.getCord()
		for i in range(cord2[0]):
			for j in range(cord2[1]):
				self._points.append((cord1[0]+i, cord1[1]+j, cord1[2]))

	def upload(self):
		data=stech.OneDataConstructor()
		data.addData('type', self._type)
		data.addData('form', self._form)
		data.addMultiData('cord1', *self._cord1.getCord())
		data.addMultiData('cord2', *self._cord2.getCord())
		data.construct()
		return data.toData()

	def getPoints(self):
		return list(self._points)

	def getZ(self):
		return self._cord1.getZ()

	def getType(self):
		return self._type


class Map:
	__PATH_TO_MAP='/home/gbh007/Dropbox/PG/black_engine_python/'
	def __init__(self, z=0):
		self._game_objects={}
		self.load()
		if z!=None:self.load(z)

	def load(self, level=None):
		if level!=None:
			cache=[i for i in open(self.__PATH_TO_MAP+'map/level'+str(level)+'.obj').read().split('#object') if i]
		else:
			cache=[i for i in open(self.__PATH_TO_MAP+'map/ERR.obj').read().split('#object') if i]
		for i in cache:
			g=GameObject(i)
			for i in g.getPoints():
				self._game_objects[i]=g

	def upload(self, level=None):
		if level!=None:
			f=open(self.__PATH_TO_MAP+'map/level'+str(level)+'.obj', 'w')
		else:
			f=open(self.__PATH_TO_MAP+'map/ERR.obj', 'w')
		trash=[]
		trash2=[]
		for i in self._game_objects:
			if level==None or self._game_objects[i].getZ()==level:
				if not self._game_objects[i] in trash2:
					print('#object', file=f)
					print(self._game_objects[i].upload(), end='', file=f)
					trash2.append(self._game_objects[i])
					trash.append(i)
				else:
					trash.append(i)
		for i in trash:
			del self._game_objects[i]

	def getMap(self,center,dx=15,dy=15):
		cord=center.getCord()
		s=[]
		for i in range(dy*2):
			s.append([])
			for j in range(dx*2):
				cache=self._game_objects.get((cord[0]+j-15,cord[1]+i-15,cord[2]))
				if cord[0]+j-15==0 and cord[1]+i-15==0:
					s[i].append('0')
					continue

				if cache:
					s[i].append(cache.getType())
				else:
					s[i].append('void')
		return s

	def getCordType(self,cord=(0,0,0)):
		try:
			return self._game_objects.get(cord).getType()
		except:
			return 'void'

	def __del__(self):
		self.upload()


def main():
	m=Map()
	print(m)


if __name__=='__main__':
	main()
