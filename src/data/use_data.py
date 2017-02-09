import yaml
from yaml import CLoader as Loader, CDumper as Dumper

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def modifiedBinarySearch(alist, item):
	first = 0
	last = len(alist)-1
	found = False

	while first<=last and not found:
		midpoint = (first + last)//2
		if alist[midpoint] >= item and alist[midpoint]-increment <= item:
			found = True
		else:
			if item < alist[midpoint]:
				last = midpoint-1
			else:
				first = midpoint+1

	return midpoint

def f(x):
    return {
    	'x': 0,
        'y': 1,
        'z': 2,
    }[x]

def g(x):
	return ['x','y','z'][x]

def inputs():
	num_of_bins = int(input("How many bins? "))
	joint_index = int(input("Which joint? ")) - 1
	num_of_dimensions = int(input("How many task space dimensions do you wish to plot? "))
	dimensions = list()
	for i in range(num_of_dimensions):
		dimensions.append(f(input("x, y, or z? (enter in lowercase) ")))
	return num_of_bins, joint_index, dimensions



num_of_bins, joint_index, dimensions = inputs()

# Loads data from yaml
stream = file('data.yaml', 'r')
data = yaml.load(stream, Loader=Loader)


while True:

	# Vars
	min_DOF_value = data["DOF_limits"][0][joint_index]
	max_DOF_value = data["DOF_limits"][1][joint_index]
	increment = (max_DOF_value - min_DOF_value) / num_of_bins
	ranges = [increment*(i+1) + min_DOF_value for i in range(num_of_bins)]
	value = list()
	for j in range(len(dimensions)):
		value.append([0 for i in range(num_of_bins)])
	count = [0 for i in range(num_of_bins)]


	# Sorts data
	i = 0
	for DOFs in data["DOFs"]:
		joint_value = DOFs[joint_index]
		bin_index = modifiedBinarySearch(ranges, joint_value)
		for j in range(len(dimensions)):
			value[j][bin_index] += data["Transforms"][i][dimensions[j]][3]
		count[bin_index] += 1	
		i += 1


	# Creates average_value
	average_value = list()
	for num in dimensions:
		average_value.append(list())
	for i in range(num_of_bins):
		if count[i] != 0:
			for j in range(len(dimensions)):
				average_value[j].append(value[j][i] / count[i])


	# Displays data
	dep_vars = np.array(average_value)
	ind_var = np.array(ranges)

	if(len(dep_vars) == 1):
		slope, intercept, r_value, p_value, std_err = stats.linregress(ind_var,dep_vars[0])
		predict_y = intercept + slope * ind_var

		plt.xlabel("Joint Space")
		plt.ylabel("Task Space: {0}".format(g(dimensions[0])))

		plt.plot(ind_var, dep_vars[0], 'o')
		plt.plot(ind_var, predict_y, 'k-')
		plt.show()

	elif(len(dep_vars) == 2):
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')

		predicts = list()
		for i in range(2):
			slope, intercept, r_value, p_value, std_err = stats.linregress(ind_var,dep_vars[i])
			predicts.append(intercept + slope * ind_var)

		plt.xlabel("Joint Space")
		plt.ylabel("Task Space: {0}".format(g(dimensions[0])))
		ax.set_zlabel("Task Space: {0}".format(g(dimensions[1])))

		ax.plot(ind_var, predicts[0], predicts[1])
		ax.scatter(ind_var, dep_vars[0], dep_vars[1])
		plt.show()

	if not input("Continue? (1/0): "):
		break

	num_of_bins, joint_index, dimensions = inputs()