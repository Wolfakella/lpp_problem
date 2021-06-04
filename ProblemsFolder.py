import configparser
import os
import shutil
import time

class ProblemsFolder():
	def __init__(self, config_file='config.ini'):
		self.config = configparser.ConfigParser()
		self.config.read(config_file)
		
		self.trace_filename = self.config.get('generator', 'trace_filename')
		self.problem_filename = self.config.get('generator', 'problem_filename')
		self.solution_filename = self.config.get('generator', 'solution_filename')
		self.foldername = self.config.get('generator', 'lpp_template')
		self.subfolder = self.config.get('generator', 'problems_folder')
		self.problems_folder = os.path.join(os.getcwd(), self.subfolder)
		self.counter = 0
		
	def makeProblemsFolder(self):
		if os.path.isdir(self.subfolder):
			shutil.rmtree(self.problems_folder)
			time.sleep(1)
		os.mkdir(self.subfolder)
		print(self.problems_folder)
		
	def saveProblem(self):
		new_folder = os.path.join(self.problems_folder, self.foldername.format(self.counter))
		os.mkdir(new_folder)
		
		src = os.path.join(os.getcwd(), self.problem_filename)
		dst = os.path.join(new_folder,  self.problem_filename)
		os.replace(src, dst)
		
		src = os.path.join(os.getcwd(), self.trace_filename)
		dst = os.path.join(new_folder,  self.trace_filename)
		os.replace(src, dst)
		
		src = os.path.join(os.getcwd(), self.solution_filename)
		dst = os.path.join(new_folder,  self.solution_filename)
		os.replace(src, dst)
		
		self.counter += 1
		return new_folder
		
	def paths(self):
		folders = os.listdir(self.problems_folder)
		result = [os.path.join(self.problems_folder, folder) for folder in folders]
		return result
		
	def traceFilename(self, index):
		folders = self.paths()
		result = os.path.join(folders[index], self.trace_filename)
		return result
		
	def problemFilename(self, index):
		folders = self.paths()
		result = os.path.join(folders[index], self.problem_filename)
		return result