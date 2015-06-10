import pickle
import numpy as np
import pylab as pl
import probdatapoint_v5 as pdp
import matplotlib.pyplot as plt 
import sys 
import scipy.special as ss
from scipy.stats import beta
from matplotlib.backends.backend_pdf import PdfPages

class plot_graph:
	def __init__(self,activity_name,params,taskname,pathName):
		self.params = params
		self.taskname = taskname
		self.activity_name = activity_name
		self. activity_at_distance = ['walking','watching','interacting']
		self.activity_nearby = ['sitting','working','relaxing','reaching']
		self.pathName=pathName
		if activity_name in self.activity_at_distance:
			close_activity = False
			self.xmin = -1
			self.ymin = -1
			self.ymax = 1
			self.xmax = 1
		else:
			close_activity = True
			self.xmin = -1
			self.ymin = -1
			self.ymax = 1
			self.xmax = 1
		self.node, self.activity_count, self.activity_local_prob = self.initnode(close_activity)
		self.plotheatmap()
		# if not close_activity:
		# 	self.plot_beta(params[activity_name]['human']['alpha'],params[activity_name]['human']['beta'])
		# 	pl.xlim(0.0,1.0)
		# 	pl.ylim(0.0,3.0)
		# 	pl.legend()
		# 	pl.show()

	def plot_beta(self,a,b):
		Ly = []
		Lx = []
		mews = np.mgrid[0:1:100j]
		for mew in mews:
			Lx.append(mew)
			Ly.append(beta.pdf(mew,a,b))
		plt.figure(2)
		plt.ylim([0,3.5])
		plt.plot(Lx, Ly, linewidth=8, label=r'$\alpha={0:.3f}\; \beta={1:.3f}$'.format(a,b))
		fname = "betaplot_task_{0}_activity_{1}.pdf".format(self.taskname,self.activity_name)
		plt.legend()
		pp = PdfPages("figs/{0}".format(fname))
		plt.savefig(pp, format='pdf')
		pp.close()

	def plotheatmap(self):
		numsamp = 80
		use_beta = True
		x = np.linspace(self.xmin,self.xmax,numsamp)
		y = np.linspace(self.ymin,self.ymax,numsamp)
		xx, yy = np.meshgrid(x,y)
		zz = np.zeros((numsamp,numsamp))
		for i in range(numsamp):
			for j in range(numsamp):
				data = np.array([xx[i,j],yy[i,j],0])
				running_sum = 0.0
				#for node in nodes:
				von_pdf, t_1, t_2, t_3 = pdp.probdata(self.params,self.node,data,self.activity_count,self.activity_local_prob,use_beta)
				running_sum += von_pdf
				zz[i,j] = running_sum
		plt.figure()
		plt.imshow(zz)
		pathName='figs/'+"heatmap_activity_{0}".format(self.activity_name)+'.png'    
		if self.pathName:
			pathName=self.pathName	
		pl.savefig(pathName,bbox_inches='tight')
		# plt.savefig(pp, format='pdf')
		# pp.close()
		#plt.show()

	def initnode(self, close_activity = False):
		node = {}
		node['activity'] = self.activity_name
		node['distance'] = 1.0
		node['obj1'] = {}
		node['obj2'] = {}
		human_node = {}
		human_node['id'] = 'human_1'
		human_node['name'] = 'human'
		human_node['xaxis'] = np.array([1,0])
		human_node['yaxis'] = np.array([0,1])
		human_node['xyz'] = np.array([0,0,0])
		object_node = {}
		if self.activity_name == 'interacting':
			object_node['id'] = 'human_2'
			object_node['name'] = 'human'
		else:
			object_node['id'] = 'object_1'
			object_node['name'] = 'object'
		object_node['xaxis'] = np.array([-1,0])
		object_node['yaxis'] = np.array([0,-1])
		if close_activity:
			object_node['xyz'] = np.array([0.1,0,0])
		else:
			object_node['xyz'] = np.array([1,0,0])
		node['obj1'] = human_node
		node['obj2'] = object_node
		activity_count = {}
		activity_count[self.activity_name] = 1.0
		activity_local_prob = {}
		activity_local_prob[self.activity_name] = {}
		activity_local_prob[self.activity_name]['prob'] = 1.0
		return node, activity_count, activity_local_prob
		

def funcMain(arg1,arg2,arg3):
	activity_name = arg1
	params_filename = arg2
	taskname = params_filename.split('_')[2]
	with open('{0}'.format(params_filename),'rb') as ff:
		params = pickle.load(ff)
	# print params
	plot_graph(activity_name,params,taskname,arg3)	

if __name__ == "__main__":
	activity_name = sys.argv[1]
	params_filename = sys.argv[2]
	taskname = params_filename.split('_')[2]
	with open('{0}'.format(params_filename),'rb') as ff:
		params = pickle.load(ff)
	# print params
	plot_graph(activity_name,params,taskname,"")	
