# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

class GOBJs:
	def __str__(self):
		s=''
		for i, j in self.__dict__.items():
			s+=str(i)+' = '+str(j)+'\n'
		return s


class GOBJr:
	def __repr__(self):
		s=''
		for i, j in self.__dict__.items():
			s+=str(i)+' = '+str(j)+'\n'
		return s
