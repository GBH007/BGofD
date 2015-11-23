# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#


class OneDataParser:
	def __init__(self, data, spliter='\n'):
		self._data=[i for i in data.split(spliter) if i]
		self.hashing()

	def hashing(self, spliter='='):
		self._hesh_data={i.split(spliter)[0].strip(): i.split(spliter)[1].strip() for i in self._data if i}

	def getString(self, index):
		if index in self._hesh_data:
			return self._hesh_data[index]
		else:
			return None

	def getInt(self, index):
		if index in self._hesh_data:
			return int(self._hesh_data[index])
		else:
			return None

	def getFloat(self, index):
		if index in self._hesh_data:
			return float(self._hesh_data[index])
		else:
			return None

	def getMultiString(self, index, spliter=','):
		if index in self._hesh_data:
			return [i for i in self._hesh_data[index].split(spliter) if i]
		else:
			return None

	def getMultiInt(self, index, spliter=','):
		if index in self._hesh_data:
			return [int(i.strip()) for i in self._hesh_data[index].split(spliter) if i]
		else:
			return None

	def getMultiFloat(self, index, spliter=','):
		if index in self._hesh_data:
			return [float(i.strip()) for i in self._hesh_data[index].split(spliter) if i]
		else:
			return None

	def __len__(self):
		return len(self._data)


class OneDataConstructor:
	def __init__(self):
		self._hash_data={}

	def addData(self, index, data):
		self._hash_data[index]=str(data)

	def addMultiData(self, index, *data, spliter=','):
		s=''
		for i in data:
			s+=str(i)+spliter
		self._hash_data[index]=s

	def construct(self, spliter='='):
		self._data=[(i+spliter+j) for i, j in self._hash_data.items()]

	def toData(self, spliter='\n'):
		data=''
		for i in self._data:
			data+=i+spliter
		return data


def main():
	# a=OneDataParser('asdas=asdsad\n')
	a=OneDataParser(open('../entitys/entity#0.ent').read())
	a.hashing()
	print(a.getMultiInt('cord'))


if __name__=='__main__':
	main()
