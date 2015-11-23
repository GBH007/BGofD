# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

import sys

sys.path.append('..')

import src.cord as scord
import src.tech as stech
import src.stat as sstat
import src.entity as sentity
import src.chart as schart
import src.display as sdisplay


class Kernel:
	__PATH_TO_MAP='/home/gbh007/Dropbox/PG/black_engine_python/'
	__VERSION='0.0.0.0'

	def __init__(self):
		self._display=sdisplay.Display()
		self._entitys=sentity.Entitys(z=None)
		self._map=schart.Map(z=None)
		self.preCordLoad()
		# self._cord=scord.Cord(0,0,0)
		self._comander=Commander(self)
		self._action=Action(self, self._map, self._entitys)
		self._load()

	def refreshMap(self):
		self._display.refreshMap(self._map.getMap(self._cord))

	def refreshEntityMap(self):
		self._display.refreshEntityMap(self._entitys.getMap(self._cord))

	def refreshDisplay(self):
		self._display.refresh()

	def printDisplay(self):
		print(self._display)

	def preCordLoad(self):
		parser=stech.OneDataParser(open(self.__PATH_TO_MAP+'map/entity_info/0.ent').read())
		self._cord=scord.Cord(parser.getMultiInt('cord'))

	def _load(self):
		self._map.load(self._cord.getZ())
		self._entitys.load(self._cord.getZ())
		self._cord=self._entitys.getEntity(0).getCord()

	def _upload(self):
		self._entitys.upload(self._cord.getZ())
		self._map.upload(self._cord.getZ())

	def destructor(self):
		self._upload()
		self._entitys.destructor()
		self._map.destructor()
		del self._entitys
		del self._map

	# def __del__(self):
	# 	self.upload()


class Commander:
	def __init__(self, kernel):
		self._kernel=kernel

	def command(self, com):
		com=[i for i in com.parse() if i]


class Action:
	def __init__(self, kernel, _map, entitys):
		self._kernel=kernel
		self._map=_map
		self._entitys=entitys

	def goLeft(self, ID):
		cord1=self._entitys.getEntity(ID).getCord()
		cord=cord1.getCord()
		cord=(cord[0]+1, cord[1], cord[2])
		if self._map.getCordType(cord)=='void':
			cord1.setCord(cord)

	def goRight(self, ID):
		cord1=self._entitys.getEntity(ID).getCord()
		cord=cord1.getCord()
		cord=(cord[0]-1, cord[1], cord[2])
		if self._map.getCordType(cord)=='void':
			cord1.setCord(cord)

	def goUp(self, ID):
		cord1=self._entitys.getEntity(ID).getCord()
		cord=cord1.getCord()
		cord=(cord[0], cord[1]+1, cord[2])
		if self._map.getCordType(cord)=='void':
			cord1.setCord(cord)

	def goDown(self, ID):
		cord1=self._entitys.getEntity(ID).getCord()
		cord=cord1.getCord()
		cord=(cord[0], cord[1]-1, cord[2])
		if self._map.getCordType(cord)=='void':
			cord1.setCord(cord)


def main():
	k=Kernel()
	k.refreshMap()
	k.refreshEntityMap()
	k.refreshDisplay()
	k.printDisplay()
	print(k._entitys._entitys[0].getCord())
	k._action.goDown(0)
	print(k._entitys._entitys[0].getCord())
	k.destructor()


if __name__=='__main__':
	main()
