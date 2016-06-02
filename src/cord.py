# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#


class Cord:
	def __init__(self, cord=(0, 0, 0)):
		self._x=cord[0]
		self._y=cord[1]
		self._z=cord[2]

	def getCord(self):
		return (self._x, self._y, self._z)

	def setCord(self, cord):
		self._x=cord[0]
		self._y=cord[1]
		self._z=cord[2]

	def changeCord(self, dcord):
		self._x+=dcord[0]
		self._y+=dcord[1]
		self._z+=dcord[2]

	def getZ(self):
		return self._z

	def __len__(self):
		return (self._x**2+self._y**2+self._z**2)

	def __str__(self):
		return '{0:3} {1:3} {2:3}'.format(self._x, self._y, self._z)
