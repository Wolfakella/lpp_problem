import numpy

class Vertex():
	def __init__(self, start, finish):
		self.point = numpy.array(start)
		end = numpy.array(finish)
		self.v = end - self.point
		if self.v.any():
			self.v = self.v / numpy.linalg.norm(self.v)
			
	def __str__(self):
		return "Vertex: {0}, vector={1}".format(self.point, self.v)