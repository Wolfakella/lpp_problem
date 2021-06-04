import copy
import numpy
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as a3
from mpl_toolkits.mplot3d import Axes3D

class Precedent():
	def __init__(self, problem, retina, vertex):
		self.problem = problem
		self.retina = copy.deepcopy(retina)
		self.vertex = vertex
		#self.retina.translateTo(vertex.point + problem.c * 1.3)
		self.retina.translateTo(vertex.point)
		self.shadow = problem.projection(self.retina.points)
		
	def distances(self):
		pass
		
	def saveToFile(self, filename):
		pass
	
	def plot(self, filename=''):
		plt.ioff()
		fig = plt.figure(figsize=(16,12))
		facets = self.problem.facets()
		pc = a3.art3d.Poly3DCollection(facets, edgecolor="k", alpha=0.3)
		limits = self.axis_lims()
		vertex = self.vertex.point
		
		ax_left = fig.add_subplot(121, projection='3d')
		ax_left.add_collection3d(pc)
		ax_left.scatter(vertex[0], vertex[1], vertex[2], color="red")
		
		ax_left.set_xlabel('x')
		ax_left.set_xlim([0,200])
		ax_left.set_ylabel('y')
		ax_left.set_ylim([200,0])
		ax_left.set_zlabel('z')
		ax_left.set_zlim([0,200])
		
		ax_right = fig.add_subplot(122, projection='3d')
		ax_right.scatter(self.shadow[:,0], self.shadow[:,1], self.shadow[:,2], color="green")
		ax_right.scatter(self.retina.points[:,0], self.retina.points[:,1], self.retina.points[:,2], color="blue")
		ax_right.quiver(
			self.vertex.point[0], 
			self.vertex.point[1], 
			self.vertex.point[2], 
			self.vertex.v[0], 
			self.vertex.v[1], 
			self.vertex.v[2], 
			arrow_length_ratio=0.05, 
			length=2.0, 
			color="red"
		)
		ax_right.set_xlabel('x')
		ax_right.set_xlim(limits[0], limits[1])
		ax_right.set_ylabel('y')
		ax_right.set_ylim(limits[3], limits[2])
		ax_right.set_zlabel('z')
		ax_right.set_zlim(limits[4], limits[5])
		
		if not filename:
			plt.show()
		else:
			plt.savefig(filename)
			print('Saved to ' + filename)
		plt.close(fig)
		
	def axis_lims(self):
		max_Z = max([max(self.shadow[:,2]), max(self.retina.points[:,2]), self.vertex.point[2]])
		min_Z = min([min(self.shadow[:,2]), min(self.retina.points[:,2]), self.vertex.point[2]])

		max_Y = max([max(self.shadow[:,1]), max(self.retina.points[:,1]), self.vertex.point[1]])
		min_Y = min([min(self.shadow[:,1]), min(self.retina.points[:,1]), self.vertex.point[1]])

		max_X = max([max(self.shadow[:,0]), max(self.retina.points[:,0]), self.vertex.point[0]])
		min_X = min([min(self.shadow[:,0]), min(self.retina.points[:,0]), self.vertex.point[0]])

		center_Z = (max_Z + min_Z) / 2
		radius_Z = (max_Z - min_Z) / 2
		center_Y = (max_Y + min_Y) / 2
		radius_Y = (max_Y - min_Y) / 2
		center_X = (max_X + min_X) / 2
		radius_X = (max_X - min_X) / 2

		max_radius = max([radius_Z, radius_Y, radius_X])
		if max_radius > 5 : max_radius = 5
		res = numpy.array([center_X - max_radius, 
						center_X + max_radius,
						center_Y - max_radius, 
						center_Y + max_radius,
						center_Z - max_radius, 
						center_Z + max_radius])
		return res