import sys
import configparser
import numpy
import matplotlib.pyplot as plt
import math

def dotproduct(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))

def length(v):
    return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
    return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

def additional_basis(c, e):
    n = len(c)
    V=list()
    V.append([0]*n)
    for k in range(1,n-1):
        v_k=list()
        if c[0] != 0:
            v_k.append(-c[k]/c[0])
        elif c[k] < 0:
            v_k.append(sys.float_info.max)
        else:
            v_k.append(-sys.float_info.max)
        for i in range(1,n-1):
            if i == k:
                v_k.append(1)
            else:
                v_k.append(0)
        v_k.append(0)
        V.append(v_k)
    return V

def R(a, b, theta, n):
    M = list()
    for i in range(n):
        row = list()
        for j in range(n):
            c = 0
            if i==a and j==a:
                c = math.cos(theta)
            elif i==b and j==b:
                c = math.cos(theta)
            elif i==a and j==b:
                c = math.sin(theta)
            elif i==b and j==a:
                c = -math.sin(theta)
            elif i==j:
                c = 1
            row.append(c)
        M.append(row)
    return M

class Retina():
	def __init__(self, config_file):
		config = configparser.ConfigParser()
		config.read("config.ini")

		self.N = config.getint('retina', 'initial_points')
		self.r = config.getfloat('retina', 'radius')
		self.debug_mode = config.getboolean('general', 'debug_mode')
		self.dim = config.getint('general', 'dimensions')
		self.base_filename = config.get('retina', 'base_filename')
		self.common_filename = config.get('retina', 'common_filename')
		self.rotation_matrix = config.get('retina', 'rotation_matrix')
		self.reverse_matrix = config.get('retina', 'reverse_matrix')

		print(self.common_filename)
		
	def createPoints(self):
		self.normal=numpy.array([0., 0., 1.])
		a=(numpy.pi*self.r**2)/self.N
		d=numpy.sqrt(a)
		
		M_r=numpy.floor(self.r/d)
		d_phi=self.r/M_r
		d_theta=a/d_phi
		points = list()
		for m in numpy.arange(M_r):
			phi=self.r*(m+0.5)/M_r
			M_theta=numpy.floor(2*numpy.pi*phi/d_theta)
			for k in numpy.arange(M_theta):
				theta=2*numpy.pi*k/M_theta
				point = list()
				x3=0
				x2=phi*numpy.sin(theta)
				x1=phi*numpy.cos(theta)
				point.append(x1)
				point.append(x2)
				point.append(x3)
				points.append(point)
		self.points = numpy.array(points)
		
	def rotateTo(self, c):
		self.normal=numpy.array(c)
		n = len(c)
		e = numpy.zeros(n)
		e[-1] = 1
		v = additional_basis(c, e)
		M = numpy.identity(n)

		for i in range(1, n-1):
			for j in range(n-1, i-1, -1):
				theta = numpy.arctan2(v[i][j], v[i][j-1])
				m = R(j,j-1,theta,n)
				v = numpy.matmul(v, m)
				M = numpy.matmul(M, m)
		
		straight = M
		rotation = R(n-2, n-1, angle(e,c), n)
		reverse = numpy.linalg.inv(M)

		result = numpy.matmul(straight, rotation)
		result = numpy.matmul(result, reverse)
		
		self.points = numpy.matmul(self.points, result)
	
	def translateTo(self, point):
		self.points = self.points + point
	
	def saveToFile(self):
		file = open(self.common_filename, "w")
		rows = len(self.points)
		for i in range(0, rows):
			file.write("\t".join([str(val) for val in self.points[i]]))
			file.write('\n')
		file.close()
		
	def loadFromCommonFile(self):
		self.points = []
		with open(self.common_filename, 'r') as fd:
			for line in fd:
				self.points.append([float(val) for val in line.split()])
		self.points = numpy.array(self.points)
		
	def plot(self):
		plt.ioff()
		fig=plt.figure(figsize=(12,9))
		ax = fig.add_subplot(111, projection='3d')
		#ax.set_autoscale_on(False)

		ax.scatter(self.points[:,0], self.points[:,1], self.points[:,2], marker='o')

		ax.set_xlabel('x1')
		#ax.set_xlim(-1,1)
		ax.set_ylabel('x2')
		#ax.set_ylim(1,-1)
		ax.set_zlabel('x3')
		#ax.set_zlim(-1,1)
		plt.show()
		plt.close(fig)