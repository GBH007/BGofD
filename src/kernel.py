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


class ExitError(Exception): pass
class KernelPanic(Exception): pass


class Kernel:
	# __PATH_TO_MAP='/home/gbh007/Dropbox/PG/black_engine_python/'
	__VERSION='0.0.0.0'

	def __init__(self, PATH_TO_MAP='/home/gbh007/Dropbox/PG/black_engine_python/'):
		self.__PATH_TO_MAP=PATH_TO_MAP
		self._display=sdisplay.Display(self.__PATH_TO_MAP)
		self._entitys=sentity.Entitys(self.__PATH_TO_MAP, z=None)
		self._map=schart.Map(self.__PATH_TO_MAP, z=None)
		self.preCordLoad()
		# self._cord=scord.Cord(0,0,0)
		self._comander=Commander(self)
		self._action=Action(self, self._map, self._entitys)
		self._load()
		self.__commands()

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

	def __commands(self):
		def mf(func):
			def f(argv, fu=func):
				try:
					l=int(argv)
					if l==0:
						l=1
				except ValueError:
					l=1
				for i in range(l):
					fu(0)

			return f

		def home(argv):
			self._cord.setCord((0, 0, 0))

		def lol(argv):
			raise KernelPanic

		self._comander.addComand('go down', mf(self._action.goDown))
		self._comander.addComand('go left', mf(self._action.goLeft))
		self._comander.addComand('go right', mf(self._action.goRight))
		self._comander.addComand('go up', mf(self._action.goUp))
		self._comander.addComand('home', home)
		self._comander.addComand('ultui nahui', lol)

	def command(self, com):  # com строка
		self._comander.command(com)

	def addMessage(self, message):
		self._display.addMessage(message)

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
		self._display.destructor()
		del self._display
		del self._entitys
		del self._map
		del self._action
		del self._comander

	# def __del__(self):
	# 	self.upload()


class Commander:
	def __init__(self, kernel):
		self._kernel=kernel
		self._commands={}

	def command(self, com):  # com строка вида comand1 comand2 comand3 (*argv)
		search=(com.find('('), com.find(')'))
		if com.find('exit')==0:
			raise ExitError
		if search[0]!=-1 and search[1]!=-1:
			argv=com[search[0]+1:search[1]]
			com=[i for i in com[:search[0]].split(' ') if i]
		elif search[0]==-1 and search[1]==-1:
			argv=''
			com=[i for i in com.split(' ') if i]
		self.goCommand(com, argv)

	def addComand(self, command,
				  function):  # command строка вида comand1 comand2 comand3 function обработчик вида func(argv) где argv строка с аргументами
		command=[i for i in command.split(' ') if i]
		com=self._commands
		for i in range(len(command)-1):
			if not command[i] in com:
				com[command[i]]={}
			com=com[command[i]]
		com[command[-1]]=function

	def goCommand(self, command_list, argv):
		try:
			com=self._commands
			for i in command_list:
				com=com[i]
			com(argv)
			return True
		except (KeyError, TypeError):
			self._kernel.addMessage('Commander -> command not found')
			# print()
			return False


class Action:
	def __init__(self, kernel, _map, entitys):
		self._kernel=kernel
		self._map=_map
		self._entitys=entitys

	def goLeft(self, ID):
		cord1=self._entitys.getEntity(ID).getCord()
		cord=cord1.getCord()
		cord=(cord[0]-1, cord[1], cord[2])
		if self._map.getCordType(cord)=='void' and self._entitys.getCordType(cord)=='void':
			cord1.setCord(cord)

	def goRight(self, ID):
		cord1=self._entitys.getEntity(ID).getCord()
		cord=cord1.getCord()
		cord=(cord[0]+1, cord[1], cord[2])
		if self._map.getCordType(cord)=='void' and self._entitys.getCordType(cord)=='void':
			cord1.setCord(cord)

	def goUp(self, ID):
		cord1=self._entitys.getEntity(ID).getCord()
		cord=cord1.getCord()
		cord=(cord[0], cord[1]+1, cord[2])
		if self._map.getCordType(cord)=='void' and self._entitys.getCordType(cord)=='void':
			cord1.setCord(cord)

	def goDown(self, ID):
		cord1=self._entitys.getEntity(ID).getCord()
		cord=cord1.getCord()
		cord=(cord[0], cord[1]-1, cord[2])
		if self._map.getCordType(cord)=='void' and self._entitys.getCordType(cord)=='void':
			cord1.setCord(cord)


def main():
	k=Kernel()
	while 1:
		k.refreshMap()
		k.refreshEntityMap()
		k.refreshDisplay()
		k.printDisplay()
		a=input('->')
		try:
			k.command(a)
		except ExitError:
			break
		# print(k._entitys._entitys[0].getCord())
		# print(k._entitys._entitys[0].getCord())
		# k._action.goDown(0)
		# print(k._entitys._entitys[0].getCord())
	k.destructor()


if __name__=='__main__':
	main()
