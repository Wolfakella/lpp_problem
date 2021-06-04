import Vertex as vtx
import numpy

class Trace():
	def __init__(self, filename):
		self.filename = filename
		self.fd = open(self.filename, 'r')
		self.lines = self.fd.readlines()
		self.fd.close()
	
	def __iter__(self):
		self.index = 0
		self.end = len(self.lines)
		return self
		
	def __next__(self):
		result = 0
		if self.index == self.end:
			raise StopIteration
		elif self.index == self.end-1:
			point  = [float(val) for val in self.lines[self.index].split()]
			finish = point
			result = vtx.Vertex(point, finish)
		else:
			point  = [float(val) for val in self.lines[self.index].split()]
			finish  = [float(val) for val in self.lines[self.index+1].split()]
			result = vtx.Vertex(point, finish)
		self.index += 1
		return result
		