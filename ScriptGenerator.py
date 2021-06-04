import subprocess
import os

def isValid():
	result = subprocess.check_output(['LPP-Validator.exe'])
	result = int(result.decode('utf-8'))
	return result
	
def createSolution():
	result = subprocess.check_output(['LPP-Solution.exe'])
	return result.decode('utf-8')

class ProblemsPacket():
	def __init__(self, filename='packet.txt'):
		self.filename = filename
		process = subprocess.Popen(['LPP-Generator.exe'], stdout=subprocess.PIPE, encoding='utf-8')
		text = process.stdout.read()
		while text:
			print(text)
			text = process.stdout.read()
		os.replace('lpp.txt', self.filename)
	
	def __iter__(self):
		self.fd = open(self.filename, 'r')
		params = self.fd.readline().split()
		self.N = int(params[0])
		self.index = 0
		return self
		
	def __next__(self):
		if self.index == self.N:
			self.fd.close()
			raise StopIteration
		with open('lpp.txt', 'w') as fout:
			line = self.fd.readline()
			fout.write(line)
			#print(line.strip())
			inequalities = int(line.split()[0])
			for i in range(inequalities):
				line = self.fd.readline()
				fout.write(line)
				#print(line.strip())
			line = self.fd.readline()
			fout.write(line)
			#print(line.strip())
			self.index += 1
			return 'lpp.txt'
		
	def __del__(self):
		self.fd.close()