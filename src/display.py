# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

import sys

sys.path.append('..')

import src.chart as schart
import src.cord as scord
import glob
import os
import tkinter
import tkinter.scrolledtext

class Textures:
	def __init__(self,PATH_TO_MAP):
		self.__PATH_TO_MAP=PATH_TO_MAP
		self.__tx={}
		#~ print(glob.glob(self.__PATH_TO_MAP+'/textures/*.gif'))
		for i in glob.glob(self.__PATH_TO_MAP+'/textures/*.gif'):
			self.__tx[os.path.split(i)[1].split('.')[0]]=tkinter.PhotoImage(file=i)
		#~ print(self.__tx)
	def get(self,name):
		return self.__tx.get(name,None)
		
		

#~ TYPE_INFO={
	#~ 'stone': '%',
	#~ 'wall': '#',
	#~ 'void': ' ',
	#~ '0': '+',
	#~ 'player': '@',
	#~ 'entity': 'E',
	#~ '': '',
#~ }


#~ def str_parser17(s):
	#~ cache=s[:]
	#~ s=[]
	#~ for i in cache.split('\n'):
		#~ if i:
			#~ for j in range(len(i)//17+1):
				#~ s.append(i[:17])
				#~ i=i[17:]
	#~ return s


class ChatDisplay:
	# __PATH_TO_MAP='/home/gbh007/Dropbox/PG/black_engine_python/'

	def __init__(self, PATH_TO_MAP,canvas,kernel):
		self.__PATH_TO_MAP=PATH_TO_MAP
		self.__canvas=canvas
		self.__kernel=kernel
		#~ self.__frame=tkinter.Frame(self.__canvas,width=200,height=400)
		self.__frame=tkinter.Frame(self.__canvas)
		#~ self.__frame=tkinter.Toplevel()
		#~ self.__chat=tkinter.scrolledtext.ScrolledText(self.__frame,width=200,height=400)
		self.__chat=tkinter.scrolledtext.ScrolledText(self.__frame)
		self.__chat.pack()
		self.__com=tkinter.StringVar()
		self.__inp=tkinter.Entry(self.__frame,textvariable=self.__com)
		self.__inp.pack(side=tkinter.LEFT)
		#~ self.__inp.pack()
		self.__but=tkinter.Button(self.__frame,text='GO',command=lambda:(self.__kernel.command(self.__com.get()),self.__kernel.refreshDisplay()))
		#~ self.__inp.bind('<Enter>',lambda *x:(self.__kernel.command(self.__com.get()),self.__kernel.refreshDisplay()))
		self.__but.pack(side=tkinter.RIGHT)
		#~ self.__but.pack()
		self.__canvas.create_window(0,400,window=self.__frame,anchor=tkinter.NW,width=200,height=400)
		#~ self._display=[]
		#~ cache=open(self.__PATH_TO_MAP+'map/chat.log').readlines()
		#~ for i in cache[-20:]:
			#~ for j in str_parser17(i):
				#~ self._display.append(j.strip('\n'))

	def addMessage(self, message):
		self.__chat.insert(tkinter.END,message+'\n')
		self.__chat.yview(tkinter.END)
		#~ for i in str_parser17(message):
			#~ self._display.append(i.strip('\n'))

	def getLast20(self):
		pass
		#~ s=self._display[-20:]
		#~ if len(s)<20:
			#~ for i in range(20-len(s)):
				#~ s.insert(0, '')
		#~ return s

	def destructor(self):
		pass
		#~ f=open(self.__PATH_TO_MAP+'map/chat.log', 'w')
		#~ for i in self._display:
			#~ print(i, file=f)


#~ class _MainDisplay:
	#~ def __init__(self):
		#~ self._display=[]

	#~ def refreshMap(self, map_data):
		#~ self._display=[]
		#~ self._display=[''.join([TYPE_INFO.get(j, ' ') for j in i]) for i in map_data]
		#~ self._display.reverse()

	#~ def getMap(self):
		#~ return self._display


#~ class MapDisplay(_MainDisplay): pass


#~ class EntityDisplay(_MainDisplay): pass


class MainDisplay:
	def __init__(self,canvas,tx):
		self.__canvas=canvas
		self.__entity_trash=[]
		self.__map_trash=[]
		self.__tx=tx
		#~ self.__canvas.pack()
		#~ self._map_display=MapDisplay()
		#~ self._entity_display=EntityDisplay()

	def refreshEntityMap(self, map_data):
		map_data.reverse()
		list(map(self.__canvas.delete,self.__entity_trash))
		for i,e in enumerate(map_data):
			for j,s in enumerate(e):
				if self.__tx.get(s):
					self.__entity_trash.append(self.__canvas.create_image(200+31*j,31*i,image=self.__tx.get(s),anchor=tkinter.NW))
		#~ self._entity_display.refreshMap(map_data)

	def refreshMap(self, map_data):
		map_data.reverse()
		list(map(self.__canvas.delete,self.__map_trash))
		for i,e in enumerate(map_data):
			for j,s in enumerate(e):
				if self.__tx.get(s):
					self.__map_trash.append(self.__canvas.create_image(200+31*j,31*i,image=self.__tx.get(s),anchor=tkinter.NW))
				else:
					self.__map_trash.append(self.__canvas.create_image(200+31*j,31*i,image=self.__tx.get('grass'),anchor=tkinter.NW))
		#~ self._map_display.refreshMap(map_data)

	def getMap(self):
		pass
		#~ cache=self._map_display.getMap()
		#~ cache1=self._entity_display.getMap()
		#~ s=[]
		#~ for i in range(len(cache1)):
			#~ s1=''
			#~ for j in range(len(cache1[i])):
				#~ s1+=cache1[i][j] if cache[i][j]==' ' else cache[i][j]
			#~ s.append(s1)
		#~ return s


class StatDisplay:
	def __init__(self,canvas):
		self.__canvas=canvas
		self.__trash=[]
		#~ self.__canvas.pack()
		#~ self._display=[]

	def refresh(self, entity_stats):
		list(map(self.__canvas.delete,self.__trash))
		#~ print(entity_stats)
		self.__trash=[self.__canvas.create_text(10,i*30+10,text=e,anchor=tkinter.NW) for i,e in enumerate(entity_stats)]
			
		#~ self._display=[]
		#~ for i in entity_stats:
			#~ for j in str_parser17(i):
				#~ self._display.append(j)

	def getStats(self):
		pass
		#~ s=self._display[:10]
		#~ if len(s)<10:
			#~ for i in range(10-len(s)):
				#~ s.append('')
		#~ return s


class Display:
	#~ line_templates={
		#~ '1': '#'*50,
		#~ '2': '#{0:17}#{1:30}#',
		#~ '3': '#'*19+'{0:30}#'
	#~ }

	def __init__(self, PATH_TO_MAP,kernel):
		self.__root=tkinter.Tk()
		self.__kernel=kernel
		self.__tx=Textures(PATH_TO_MAP)
		self.__canvas=tkinter.Canvas(self.__root,width=1130,height=930)
		self.__canvas.pack()
		self.__PATH_TO_MAP=PATH_TO_MAP
		#~ self._display=[]
		self._stat_dispaly=StatDisplay(self.__canvas)
		self._main_display=MainDisplay(self.__canvas,self.__tx)
		self._chat_display=ChatDisplay(self.__PATH_TO_MAP,self.__canvas,self.__kernel)
		self.__root.bind('<Up>',lambda *x:(self.__kernel.command('go up'),self.__kernel.refreshDisplay()))
		self.__root.bind('<Down>',lambda *x:(self.__kernel.command('go down'),self.__kernel.refreshDisplay()))
		self.__root.bind('<Left>',lambda *x:(self.__kernel.command('go left'),self.__kernel.refreshDisplay()))
		self.__root.bind('<Right>',lambda *x:(self.__kernel.command('go right'),self.__kernel.refreshDisplay()))

	def refreshMap(self, map_data):
		self._main_display.refreshMap(map_data)

	def refreshEntityMap(self, map_data):
		self._main_display.refreshEntityMap(map_data)

	def refreshStat(self, entity_stats):
		self._stat_dispaly.refresh(entity_stats)

	def addMessage(self, message):
		self._chat_display.addMessage(message)

	def mainloop(self):
		self.__root.mainloop()
	def refresh(self):
		#~ self.__root.mainloop()
		self.__canvas.update()
		#~ self._display=[]
		#~ map_cache=self._main_display.getMap()
		#~ chat_cache=self._chat_display.getLast20()
		#~ stat_cache=self._stat_dispaly.getStats()
		#~ for i in range(32):
			#~ if i==0:
				#~ self._display.append(self.line_templates['1'])
			#~ elif i<10:
				#~ self._display.append(self.line_templates['2'].format(stat_cache[i-1], map_cache[i-1]))
			#~ elif i==10:
				#~ self._display.append(self.line_templates['3'].format(map_cache[i-1]))
			#~ elif i<31:
				#~ self._display.append(self.line_templates['2'].format(chat_cache[i-11], map_cache[i-1]))
			#~ else:
				#~ self._display.append(self.line_templates['1'])

	def __str__(self):
		pass
		#~ return '\n'.join(self._display)

	def destructor(self):
		self._chat_display.destructor()
		del self._chat_display
		del self._main_display
		del self._stat_dispaly


def main():
	#~ c=scord.Cord()
	d=Display('.')
	d.refresh()
	#~ a=schart.Map()
	#~ d.refreshMap(a.getMap(c))
	#~ d.refresh()
	#~ print(d)


# print(a._game_objects)
# b=MapDisplay()
# b.refreshMap(a.getMap(c))
# e=b.getMap()
# print('#'*30)
# for i in e:
# 	print(i+'#')


if __name__=='__main__':
	main()
