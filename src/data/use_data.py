import ast
import yaml
from yaml import CLoader as Loader, CDumper as Dumper
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

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


# Inputs
num_of_bins = int(input("How many bins? "))
joint_index = int(input("Which joint? ")) - 1
dimension = f(input("x, y, or z? (enter in lowercase) "))

# Loads data from yaml
stream = file('data.yaml', 'r')
data = yaml.load(stream, Loader=Loader)


while True:

	# Variable declaration
	min_DOF_value = data["DOF_limits"][0][joint_index]
	max_DOF_value = data["DOF_limits"][1][joint_index]

	increment = (max_DOF_value - min_DOF_value) / num_of_bins
	ranges = [increment*(i+1) + min_DOF_value for i in range(num_of_bins)]
	value = [0 for i in range(num_of_bins)]
	count = [0 for i in range(num_of_bins)]


	i = 0
	for DOFs in data["DOFs"]:
		joint_value = DOFs[joint_index]
		bin_index = modifiedBinarySearch(ranges, joint_value)
		value[bin_index] += data["Transforms"][i][dimension][3]
		count[bin_index] += 1	
		i += 1


	average_value = list()
	for i in range(num_of_bins):
		if count[i] != 0:
			average_value.append(value[i] / count[i])

	y = np.array(average_value)
	x = np.array(ranges)

	slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
	predict_y = intercept + slope * x
	print r_value

	plt.plot(x, y, 'o')
	plt.plot(x, predict_y, 'k-')
	plt.show()


	if not input("Continue? (1/0): "):
		break

	# Inputs
	num_of_bins = int(input("How many bins? "))
	joint_index = int(input("Which joint? ")) - 1
	dimension = f(input("x, y, or z? (enter in lowercase) "))