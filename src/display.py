# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

import sys

sys.path.append('..')

import src.chart as schart
import src.cord as scord

TYPE_INFO={
	'stone': '%',
	'wall': '#',
	'void': ' ',
	'0': '+',
	'player': '@',
	'entity': 'E',
	'': '',
}


def str_parser17(s):
	cache=s[:]
	s=[]
	for i in range(len(cache)//17+1):
		s.append(cache[:17])
		cache=cache[17:]
	return s


class ChatDisplay:
	# __PATH_TO_MAP='/home/gbh007/Dropbox/PG/black_engine_python/'

	def __init__(self, PATH_TO_MAP):
		self.__PATH_TO_MAP=PATH_TO_MAP
		self._display=[]
		cache=open(self.__PATH_TO_MAP+'map/chat.log').readlines()
		for i in cache[-20:]:
			for j in str_parser17(i):
				self._display.append(j.strip('\n'))

	def addMessage(self, message):
		for i in str_parser17(message):
			self._display.append(i.strip('\n'))

	def getLast20(self):
		s=self._display[-20:]
		if len(s)<20:
			for i in range(20-len(s)):
				s.insert(0,'')
		return s

	def destructor(self):
		f=open(self.__PATH_TO_MAP+'map/chat.log', 'w')
		for i in self._display:
			print(i, file=f)


class _MainDisplay:
	def __init__(self):
		self._display=[]

	def refreshMap(self, map_data):
		self._display=[]
		self._display=[''.join([TYPE_INFO.get(j, ' ') for j in i]) for i in map_data]
		self._display.reverse()

	def getMap(self):
		return self._display


class MapDisplay(_MainDisplay): pass


class EntityDisplay(_MainDisplay): pass


class MainDisplay:
	def __init__(self):
		self._map_display=MapDisplay()
		self._entity_display=EntityDisplay()

	def refreshEntityMap(self, map_data):
		self._entity_display.refreshMap(map_data)

	def refreshMap(self, map_data):
		self._map_display.refreshMap(map_data)

	def getMap(self):
		cache=self._map_display.getMap()
		cache1=self._entity_display.getMap()
		s=[]
		for i in range(len(cache1)):
			s1=''
			for j in range(len(cache1[i])):
				s1+=cache1[i][j] if cache[i][j]==' ' else cache[i][j]
			s.append(s1)
		return s


class StatDisplay:
	def __init__(self):
		self._display=[]


class Display:
	line_templates={
		'1': '#'*50,
		'2': '#{0:17}#{1:30}#',
		'3': '#'*19+'{0:30}#'
	}

	def __init__(self, PATH_TO_MAP):
		self.__PATH_TO_MAP=PATH_TO_MAP
		self._display=[]
		self._chat_display=ChatDisplay(self.__PATH_TO_MAP)
		# self._map_display=MapDisplay()
		self._main_display=MainDisplay()
		self._stat_dispaly=StatDisplay()

	def refreshMap(self, map_data):
		self._main_display.refreshMap(map_data)

	def refreshEntityMap(self, map_data):
		self._main_display.refreshEntityMap(map_data)

	def addMessage(self, message):
		self._chat_display.addMessage(message)

	def refresh(self):
		self._display=[]
		map_cache=self._main_display.getMap()
		chat_cache=self._chat_display.getLast20()
		for i in range(32):
			if i==0:
				self._display.append(self.line_templates['1'])
			elif i<10:
				self._display.append(self.line_templates['2'].format('', map_cache[i-1]))
			elif i==10:
				self._display.append(self.line_templates['3'].format(map_cache[i-1]))
			elif i<31:
				self._display.append(self.line_templates['2'].format(chat_cache[i-11], map_cache[i-1]))
			else:
				self._display.append(self.line_templates['1'])

	def __str__(self):
		return '\n'.join(self._display)

	def destructor(self):
		self._chat_display.destructor()
		del self._chat_display
		del self._main_display
		del self._stat_dispaly


def main():
	c=scord.Cord()
	d=Display()
	a=schart.Map()
	d.refreshMap(a.getMap(c))
	d.refresh()
	print(d)


# print(a._game_objects)
# b=MapDisplay()
# b.refreshMap(a.getMap(c))
# e=b.getMap()
# print('#'*30)
# for i in e:
# 	print(i+'#')


if __name__=='__main__':
	main()
